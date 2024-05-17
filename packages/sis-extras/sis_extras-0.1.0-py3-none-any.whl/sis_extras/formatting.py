from __future__ import annotations

import hashlib
from contextlib import contextmanager

import altair as alt
import pandas as pd
import snowflake.snowpark as sp
import streamlit as st
from plotly.graph_objs._figure import Figure

from .connection import format_sql, format_sql_from_df, get_pandas_df


@contextmanager
def tile_ctx(
    df: sp.DataFrame | pd.DataFrame,
    description: str,
    sql: str | None = None,
    chart: alt.Chart | alt.LayerChart | Figure | None = None,
    skip_chart: bool = False,
):
    """Create a tile with a chart, a dataframe preview, the SQL query and a description.
    This is the context manager version that can be used to add more notes to the
    chart tab in the tile.

    Examples:
    >>> with tile(df, "Description", "SELECT * FROM ...", chart=chart):
            st.write("I want to add more notes here under the chart.")

    >>> with tile(df, "Description", "SELECT * FROM ...", chart=None):
            st.write("I want to add more notes here above the chart.")
            st.plotly_chart(chart, use_container_width=True)

    Args:
        df (spark.DataFrame | pd.DataFrame): Data.
        description (str): Description of the what the tile is about.
        sql (str | None, optional): Underlying SQL query. Defaults to None.
        chart (alt.Chart | Figure | None, optional): Optional chart. Defaults to None.

    Raises:
        ValueError: Whenever chart is not an altair or plotly chart.
    """

    data = get_pandas_df(df) if isinstance(df, sp.DataFrame) else df

    if not skip_chart:
        t1, t2, t3, t4, t5 = st.tabs(
            ["Chart", "Data Preview", "SQL", "Description", "Download Data"]
        )
    else:
        t2, t3, t4, t5 = st.tabs(
            ["Data Preview", "SQL", "Description", "Download Data"]
        )
        if chart is not None:
            raise ValueError("Chart cannot be passed when skip_chart is True. ")

    t4.markdown(description)

    if chart is not None:
        if isinstance(chart, (alt.Chart, alt.LayerChart)):
            t1.altair_chart(chart, use_container_width=True)
        elif isinstance(chart, Figure):
            t1.plotly_chart(
                chart, use_container_width=True, config={"displayModeBar": False}
            )
        else:
            raise ValueError("Chart must be an altair or plotly chart.")

    if data.empty:
        t2.error("No data")
    else:
        t2.dataframe(data, use_container_width=True)

        with t5:
            data_hash = hashlib.sha256(
                pd.util.hash_pandas_object(data).values
            ).hexdigest()

            st.download_button(
                "Download data as csv",
                data.to_csv(index=False),
                "data.csv",
                mime="text/csv",
                key=data_hash,
            )

    # When dataframe is a Snowpark dataframe, the SQL query is not explicitly passed
    # Instead, the query is found in the dataframe's metadata.
    if sql is None and isinstance(df, sp.DataFrame):
        sql = format_sql_from_df(df)
        t3.code(format_sql(sql))
    elif sql is None:
        t3.caption("No SQL query was provided.")
    else:
        t3.code(format_sql(sql))

    if skip_chart:
        yield
    else:
        with t1:
            if data.empty:
                st.error("No data")
            yield


def tile(
    df: sp.DataFrame | pd.DataFrame,
    description: str,
    chart: alt.Chart | alt.LayerChart | Figure | None = None,
    sql: str | None = None,
    skip_chart: bool = False,
) -> None:
    """Create a tile with a chart, a dataframe preview, the SQL query and a description.

    Args:
        df (spark.DataFrame | pd.DataFrame): Data.
        description (str): Description of the what the tile is about.
        chart (alt.Chart | Figure | None, optional): Chart.
        sql (str | None, optional): Underlying SQL query. Defaults to None.
        skip_chart (bool, optional): Whether to skip the chart tab. Defaults to False.

    Examples:
    >>> chart = alt.Chart(df).mark_bar().encode(...)
        tile(df, "Description", "SELECT * FROM ...", chart=chart)
    """

    with tile_ctx(df, description, sql, chart, skip_chart):
        pass


def altair_time_series(
    data: pd.DataFrame,
    x: str,
    y: str,
    x_title: str,
    y_title: str,
    y_axis_format: str = ".0f",
    line_color="blue",
    color_var="variable",
) -> alt.Chart | None:
    """Plot a time series using Altair
    Args:
        data (pd.DataFrame): Original dataframe
        x (str): Column to use for x
        y (str): Column to use for y
    """
    # If the data is empty, return an empty chart
    if data.empty:
        return None

    data = data.copy()
    data[x] = data[x] + pd.Timedelta(days=1)

    # Label data that has an average in the column name
    data["is_avg"] = data[color_var].str.contains("_avg_")

    # Some data may require a differently formatted tooltip,
    # like average values or scientific notation. In order to
    # allow this, we need to create two charts (one for each tooltip)
    # and combine them
    if any(data["is_avg"]):
        data_noavg = data[~data["is_avg"]]
        data_avg = data[data["is_avg"]]
        data_list = [data_noavg, data_avg]
        format_list = [y_axis_format, ".2f"]
    else:
        data_list = [data]
        format_list = [y_axis_format]

    # Iterate through the dataframes and create the charts
    chart_list = []
    for df, format in zip(data_list, format_list):
        # Move the min tick step
        tick_min_step = 0 if df[y].max() < 1 else 1

        base = alt.Chart(df).mark_line(color=line_color, point=True)
        domain = [0, float(df[y].max()) * 1.2]
        chart = base.encode(
            x=alt.X(f"yearmonthdate({x}):O", axis=alt.Axis(title=x_title)),
            y=alt.Y(
                y,
                axis=alt.Axis(
                    title=y_title,
                    format=format,
                    tickMinStep=tick_min_step,
                ),
                scale=alt.Scale(domain=domain),
            ),
            color=alt.Color(color_var, title="Variable"),
            tooltip=[
                f"yearmonthdate({x}):O",
                alt.Tooltip(y, format=format),
                color_var,
            ],
        )
        chart_list.append(chart)

    # Combine the charts if necessary
    chart = alt.layer(*chart_list) if len(chart_list) > 1 else chart_list[0]

    return chart.configure_legend(orient="bottom")
