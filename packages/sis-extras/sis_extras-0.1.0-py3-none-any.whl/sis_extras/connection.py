from __future__ import annotations

import re
import time
from functools import reduce
from typing import Mapping, cast

import pandas as pd
import streamlit as st
from snowflake.snowpark import Column, DataFrame, Session, Table
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.exceptions import (
    SnowparkFetchDataException,
    SnowparkSessionException,
    SnowparkSQLException,
)
from streamlit.runtime.scriptrunner import get_script_run_ctx


def _deep_get(dictionary, keys, default=None):
    """
    deep_get can can iterate through nested dictionaries, used to get credentials in the
    case of a multi-level secrets.toml hierarchy
    """
    if default is None:
        default = {}

    return reduce(
        lambda d, key: d.get(key, default) if isinstance(d, Mapping) else default,
        keys.split("."),
        dictionary,
    )


class SnowparkConnection:
    # Initialize the connection; optionally provide the connection_name
    # (used to look up credentials in secrets.toml when run locally)
    #
    # For now this just provides a convenience connect() method to get an underlying
    # Snowpark session; it could also be extended to handle caching and other
    # functionality!
    def __init__(self, connection_name="connections.snowflake"):
        self.connection_name = connection_name

    # connect() returns a snowpark session object; in SiS it gets the active session
    # on local, it checks session state for an existing object and tries to initialize
    # one if not yet created. It checks secrets.toml for credentials and provides a
    # more descriptive error if credentials are missing or path is misconfigured
    # (otherwise you get a "User is empty" error)
    def connect(self):
        try:
            return get_active_session()
        except SnowparkSessionException:
            ctx = get_script_run_ctx()

            session_state = {} if ctx is None else st.session_state

            if "snowpark_session" not in session_state:
                creds = _deep_get(st.secrets, self.connection_name)

                if not creds:
                    st.exception(
                        ValueError(
                            "Unable to initialize connection to Snowflake, did not "
                            "find expected credentials in secret "
                            f"{self.connection_name}. "
                            "Try updating your secrets.toml"
                        )
                    )
                    st.stop()
                session = Session.builder.configs(creds).create()
                session_state["snowpark_session"] = session
            return session_state["snowpark_session"]


def get_data_frame_from_raw_sql(
    sql,
    connection: SnowparkConnection | None = None,
    lowercase_columns: bool = False,
    show_sql: bool = False,
    show_time: bool = False,
    data_name: str = "data",
) -> pd.DataFrame:
    start_time = time.time()

    if show_sql:
        with st.expander("Show the SQL query that generated this data"):
            st.code(
                format_sql(sql),
                language="sql",
            )

    @st.cache_data(ttl=60 * 60 * 6, show_spinner=False)
    def get_data(sql: str, lowercase_columns: bool, _connection: SnowparkConnection):
        session = _connection.connect()
        dataframe = session.sql(sql).to_pandas()
        if lowercase_columns:
            dataframe.columns = [column.lower() for column in dataframe.columns]
        return dataframe

    with st.spinner(f"⌛ Loading {data_name}..."):
        if connection is None:
            connection = SnowparkConnection()
        dataframe = get_data(
            sql, lowercase_columns=lowercase_columns, _connection=connection
        )

    if show_time:
        st.info(f"⏱️ Data loaded in {time.time() - start_time:.2f} seconds")
    return dataframe


@st.cache_data(ttl=60 * 60 * 6)
def _get_df(
    _df: DataFrame,
    queries_str: str,
) -> pd.DataFrame:
    """Converts a Snowpark DataFrame to Pandas DataFrame

    Args:
        _df (DataFrame): Snowpark DataFrame
        queries_str (str): SQL query to get this dataframe.
                           The argument is not used in the function, but it is used
                           to effectively invalidate the cache when the query changes.

    Returns:
        pd.DataFrame: Pandas DataFrame
    """
    _ = queries_str  # This line is here to avoid a warning about an unused argument

    return _df.to_pandas()


def get_pandas_df(
    df: DataFrame,
    lowercase_columns: bool = False,
    show_sql: bool = False,
    show_time: bool = False,
) -> pd.DataFrame:
    """Converts a Snowpark DataFrame to Pandas DataFrame

    Args:
        df (DataFrame): Snowpark DataFrame

    Returns:
        pd.DataFrame: Pandas DataFrame
    """
    queries = str(df._plan.queries[0].sql)
    # Filter out temp tables so that they don't mess up the cache
    filtered = re.sub("SNOWPARK_TEMP_TABLE_[A-Z0-9]+", "TEMP_TABLE", queries)
    filtered = re.sub("query_id_place_holder_[a-zA-Z0-9]+", "query_id", filtered)
    filtered = re.sub('"[l|r]_[a-zA-Z0-9]{4}_', "join_id_", filtered)

    start = time.time()

    try:
        pd_df = _get_df(_df=df, queries_str=filtered)
    except (SnowparkSQLException, SnowparkFetchDataException):
        st.expander("Show the SQL query that caused the error").code(
            format_sql_from_df(df),
            language="sql",
        )
        raise

    if lowercase_columns:
        pd_df.columns = [column.lower() for column in pd_df.columns]

    if show_sql:
        with st.expander("Show the SQL query that generated this data"):
            st.code(
                format_sql_from_df(df),
                language="sql",
            )

    if show_time:
        st.info(f"⏱️ Data loaded in {time.time() - start:.2f} seconds")

    return pd_df


@st.cache_resource
def get_table(table_name: str, _session: Session | None = None) -> Table:
    if _session is None:
        _session = cast(Session, SnowparkConnection().connect())
    return _session.table(table_name)


def join_cached(
    df1: DataFrame,
    df2: DataFrame,
    on: str | Column | None = None,
    how: str | None = None,
    *,
    lsuffix: str = "",
    rsuffix: str = "",
    **kwargs,
) -> DataFrame:
    """
    This function serves as a cached alternative to Snowpark's `join` method.

    For example, instead of df1.join(df1, ...) you can do `join_cached(df1, df2, ...)`

    This works by constructing a unique key based on the SQL queries that generated by
    the two dataframes + the `on` condition.

    The dataframes are converted into the underling sql query, and the `on` condition is
    either a Column (like `col('a')` or `(col('a') == col('b'))`), or a string (like
    `'a'`), so combining all those strings should uniquely identify the join.
    """

    @st.cache_resource
    def _join_cached(_df1, _df2, _on, how, lsuffix, rsuffix, meta_query, **kwargs):  # noqa: ARG001
        """
        Ignore df1, df2 and on, because those are not cachable, and instead just depend
        on how, lsuffix, rsuffix, and meta_query
        """
        return _df1.join(
            _df2, on=_on, how=how, lsuffix=lsuffix, rsuffix=rsuffix, **kwargs
        )

    meta_query = df1._plan.queries[0].sql + df2._plan.queries[0].sql

    if isinstance(on, Column):
        meta_query += str(on._expression)
    elif isinstance(on, str):
        meta_query += on

    return _join_cached(df1, df2, on, how, lsuffix, rsuffix, meta_query, **kwargs)


def format_sql(sql: str) -> str:
    try:
        import sqlparse
    except ImportError:
        return sql

    return sqlparse.format(sql, reindent=True, keyword_case="lower")


def format_sql_from_df(df: DataFrame, use_header: bool = True) -> str:
    header = "-- This query was generated by Snowpark\n" if use_header else ""
    return header + format_sql(str(df._plan.queries[0].sql))
