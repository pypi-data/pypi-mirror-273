#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
# -------------------------------------------------------------------------------


"""
This file contains utility functions for transforming data and getting
the json representation of plot.ly charts required by various Mentat modules.
"""

import datetime
from math import ceil
import json

import plotly.express as px
import plotly.graph_objects as pgo
import flask
from flask_babel import gettext
import pandas as pd
import pytz
from typing import Callable, Iterator, Optional, Tuple, Union
from numbers import Number

import hawat.utils
from mentat.stats.idea import ST_SKEY_REST
from hawat.chart_const import (
    ChartJSONType,
    ChartSection,
    DataComplexity,
    DataKey,
    DataRowType,
    DataWideType,
    DataLongType,
    InputDataFormat,
    StatisticsDataType,
    TimelineCfgType
)
from hawat import chart_const


BLUEPRINT_NAME = 'charts'


def get_datetime_format_function(
    timeline_cfg: TimelineCfgType,
    timezone: Optional[str] = None
) -> Callable[[datetime.datetime], str]:
    """
    Returns a function that formats datetime objects according to the provided timeline configuration.
    """
    tz = pytz.timezone(timezone or flask.session.get('timezone', 'UTC'))

    timeline_timespan = timeline_cfg['dt_to'] - timeline_cfg['dt_from']

    if timeline_timespan > datetime.timedelta(days=1):
        def dt_format_function(dt: datetime.datetime):
            dt_utc = dt.replace(tzinfo=datetime.timezone.utc)
            return dt_utc.astimezone(tz).strftime('%Y-%m-%d')
    else:
        def dt_format_function(dt: datetime.datetime):
            dt_utc = dt.replace(tzinfo=datetime.timezone.utc)
            localized = dt_utc.astimezone(tz)
            if timeline_cfg['step'] < datetime.timedelta(seconds=1):
                return localized.strftime('%M:%S.%f')
            if localized.second > 0:
                return localized.strftime('%H:%M:%S')
            return localized.strftime('%H:%M')

    return dt_format_function


def from_long_simple_timeline(data: DataLongType, chsection: ChartSection) -> pd.DataFrame:
    """
    Converts from `InputDataFormat.LONG_SIMPLE` to a unified pandas DataFrame for timeline.
    """
    df = pd.DataFrame(data)
    df.set_index('bucket', inplace=True)
    df.rename(columns={'count': str(chsection.column_name)}, inplace=True)
    return df


def from_long_complex_timeline(data: DataLongType) -> pd.DataFrame:
    """
    Converts from `InputDataFormat.LONG_COMPLEX` to a unified pandas DataFrame for timeline.
    """
    df = pd.DataFrame(data)

    # Similar to:
    # df = pd.DataFrame(data).pivot(
    #     columns='set',
    #     index='bucket',
    #     values='count'
    # )
    # But retains the order of columns
    return df.groupby(
        ['bucket', 'set'],
        sort=False
    )['count'].sum().unstack()


def _iter_data_keys(chsection: ChartSection) -> Iterator[DataKey]:
    if chsection.data_keys is not None:
        yield from chsection.data_keys
    else:
        yield DataKey(chsection.key, chsection.column_name)


def _iter_wide_simple_data(
    data: DataWideType,
    chsection: ChartSection
) -> Iterator[DataRowType]:
    for bucket, stat in data:
        row = {'bucket': bucket}
        for data_key in _iter_data_keys(chsection):
            row[str(data_key.display_name)] = stat.get(data_key.key, 0)
        yield row


def from_wide_simple_timeline(data: DataWideType, chsection: ChartSection) -> pd.DataFrame:
    """
    Converts from `InputDataFormat.WIDE_SIMPLE` to a unified pandas DataFrame for timeline.
    """
    df = pd.DataFrame(_iter_wide_simple_data(data, chsection))
    df.set_index('bucket', inplace=True)
    return df


def _iter_wide_complex_data(
    data: DataWideType,
    chsection: ChartSection
) -> Iterator[DataRowType]:
    for bucket, stat in data:
        yield {'bucket': bucket, **stat.get(chsection.key, {})}


def from_wide_complex_timeline(data: DataWideType, chsection: ChartSection) -> pd.DataFrame:
    """
    Converts from `InputDataFormat.WIDE_COMPLEX` to a unified pandas DataFrame for timeline.
    """
    df = pd.DataFrame(_iter_wide_complex_data(data, chsection))
    df.fillna(0, inplace=True)
    df.set_index('bucket', inplace=True)
    return df


def add_timeline_rest(df: pd.DataFrame) -> pd.DataFrame:
    """
    Abridges the dataframe for secondary charts to contain only `chart_const.MAX_VALUE_COUNT` columns,
    and stores the rest under `__REST__` column.
    """
    if df.shape[1] > chart_const.MAX_VALUE_COUNT:
        kept_columns = df.iloc[:, :chart_const.MAX_VALUE_COUNT - 1]
        df[ST_SKEY_REST] = df.iloc[:, chart_const.MAX_VALUE_COUNT - 1:].sum(axis=1)
        return pd.concat([kept_columns, df[[ST_SKEY_REST]]], axis=1)

    return df


def get_timeline_chart_and_table_data_frame(
        data: Union[DataWideType, DataLongType],
        chsection: ChartSection,
        timeline_cfg: TimelineCfgType,
        data_format: InputDataFormat,
        add_rest: bool = False,
        forced_timezone: Optional[str] = None
) -> Tuple[ChartJSONType, pd.DataFrame]:
    """
    For the provided statistics and chart section returns a JSON object for rendering a timeline
    chart, and the data frame used to generate accompanying table, and exportable csv and json
    data.

    Expects `data` to be sorted by bucket in ascending order.

    if add_rest is true, the data is modified so it only contains `chart_const.MAX_VALUE_COUNT`
    columns, and the rest will be stored under `__REST__` (Useful, when the source statistics do not
    already contain `__REST__`, and need to be abridged)
    """
    if data_format == InputDataFormat.LONG_SIMPLE and chsection.data_complexity != DataComplexity.NONE:
        raise ValueError('LONG_SIMPLE data format can only support data complexity of NONE')

    if data_format == InputDataFormat.WIDE_SIMPLE:
        df = from_wide_simple_timeline(data, chsection)
    elif data_format == InputDataFormat.WIDE_COMPLEX:
        df = from_wide_complex_timeline(data, chsection)
    elif data_format == InputDataFormat.LONG_SIMPLE:
        df = from_long_simple_timeline(data, chsection)
    elif data_format == InputDataFormat.LONG_COMPLEX:
        df = from_long_complex_timeline(data)

    if add_rest:
        df = add_timeline_rest(df)

    if df.empty:
        chart = get_chart_no_data_json()
    else:
        chart = get_timeline_chart_json(df, chsection, timeline_cfg, forced_timezone=forced_timezone)

    df[chart_const.KEY_SUM] = df.sum(axis=1)  # add sum of each bucket as a last column
    return chart, df


def add_secondary_rest(df: pd.DataFrame) -> pd.DataFrame:
    """
    Abridges the dataframe for secondary charts to contain only `chart_const.MAX_VALUE_COUNT` rows,
    and stores the rest under `__REST__`.
    """
    if df.shape[0] > chart_const.MAX_VALUE_COUNT:
        kept_rows = df.iloc[:chart_const.MAX_VALUE_COUNT - 1]
        rest_sum = df.iloc[chart_const.MAX_VALUE_COUNT - 1:]['count'].sum()
        sum_row = pd.DataFrame({'set': [ST_SKEY_REST], 'count': [rest_sum]})
        return pd.concat([kept_rows, sum_row])
    return df


def get_secondary_chart_and_table_data_frame(
    statistics: StatisticsDataType,
    chsection: ChartSection,
    data_format: InputDataFormat,
    total_count: Optional[Number] = None,
    add_rest: bool = False,
    sort: bool = False,
) -> Tuple[ChartJSONType, pd.DataFrame]:
    """
    For the provided statistics and chart section returns a JSON object for rendering a secondary
    chart, and the data frame used to generate accompanying table, and exportable csv and json
    data.

    if total count not provided, it is calculated as the sum of all counts in the data frame.

    if add_rest is true, the data is modified so it only contains `chart_const.MAX_VALUE_COUNT`
    rows, and the rest will be stored under `__REST__` (Useful, when the source statistics do not
    already contain `__REST__`, and need to be abridged)

    sort should be set to True, if the source data is not yet sorted.
    """

    if chsection.data_complexity == DataComplexity.NONE:
        raise ValueError('Cannot generate a secondary chart for DataComplexity.NONE')

    if data_format == InputDataFormat.WIDE_SIMPLE:
        data_iter = (
            {'set': str(data_key.display_name), 'count': statistics.get(data_key.key)}
            for data_key in _iter_data_keys(chsection)
        )
    elif chsection.key in statistics:
        data_iter = ({'set': key, 'count': val} for key, val in statistics[chsection.key].items())
    else:
        data_iter = []

    df = pd.DataFrame(data_iter)

    if sort and not df.empty:
        df = df.sort_values(by='count', ascending=False)

    if add_rest:
        df = add_secondary_rest(df)

    if df.empty:
        chart = get_chart_no_data_json()
    elif chsection.data_complexity == DataComplexity.SINGLE:
        chart = get_pie_chart_json(df, chsection)
    elif chsection.data_complexity == DataComplexity.MULTI:
        chart = get_bar_chart_json(df, chsection)

    if total_count is None and 'count' in df.columns:
        total_count = df['count'].sum()

    if total_count != 0 and 'count' in df.columns:
        df[chart_const.KEY_SHARE] = df['count'] / total_count

    if 'set' in df.columns:
        df.set_index('set', inplace=True)

    return chart, df


# -------------------------------------CHART CONFIGURATION-----------------------------------------


def _chart_set_config_and_get_dict(fig: pgo.Figure) -> ChartJSONType:
    """
    Get JSON encodable dict representation of chart,
    disable rendering of mode bar, and make the chart responsive.

    The default dict export method for plotly figure is not json encodable,
    and there is no other way to set config than directly modifying the dict object.
    """
    fig_dict = ChartJSONType(json.loads(fig.to_json()))

    config = fig_dict.setdefault('config', {})
    config['displayModeBar'] = False
    config['responsive'] = True

    return fig_dict


def get_chart_no_data_json() -> ChartJSONType:
    """
    Generate a JSON object for rendering a chart to be rendered when no data is available.
    """
    fig = px.scatter([])
    fig.update_layout(
        annotations=[
            {
                "text": gettext("There is no data to be displayed"),
                "showarrow": False,
                "xref": "paper",
                "yref": "paper",
                "x": 0.5,
                "y": 0.5,
                "font": {"size": 20},
            }
        ],
        xaxis=pgo.layout.XAxis(
            visible=False,
            fixedrange=True  # Disable zooming of the chart
        ),
        yaxis=pgo.layout.YAxis(
            visible=False,
            fixedrange=True  # Disable zooming of the chart
        ),
        autosize=True,
        plot_bgcolor=chart_const.TRANSPARENT,
        paper_bgcolor=chart_const.TRANSPARENT
    )
    return _chart_set_config_and_get_dict(fig)


def get_timeline_chart_json(
    df: pd.DataFrame,
    chsection: ChartSection,
    timeline_cfg: TimelineCfgType,
    forced_timezone: Optional[str] = None
) -> ChartJSONType:
    """
    Generate a timeline chart as a JSON object for rendering using plotly.
    """

    bucket_format_function = hawat.utils.fallback_formatter(
        get_datetime_format_function(timeline_cfg, timezone=forced_timezone)
    )
    column_name = str(chsection.column_name)
    value_name = str(chsection.value_formats.column_name)

    if chsection.data_complexity == DataComplexity.NONE:
        hover_data = {'variable': False}
        column_labels = {'value': column_name}
    else:
        hover_data = {}
        column_labels = {
            'set': column_name,
            'variable': column_name,
            'value': value_name
        }

    fig = px.bar(
        df,
        y = df.columns,
        labels={
            'bucket': gettext('Time'),
            **column_labels
        },
        color_discrete_sequence=chart_const.COLOR_LIST,
        hover_data=hover_data
    )

    buckets = fig.data[0].x
    tick_values = buckets[::ceil(len(buckets) / chart_const.NUMBER_OF_LABELED_TICKS)]
    ticks_formatted = list(map(bucket_format_function, tick_values))

    fig.update_layout(
        xaxis=pgo.layout.XAxis(
            type='category',  # Otherwise, when the first bucket is misaligned, the x-axis is scaled improperly
            linecolor=chart_const.AXIS_LINE_COLOR,
            tickmode="array",          # tickmode, tickvals, and ticktext are set due to plot.ly not allowing
            tickvals=tick_values,      # a sane method for automatically formatting tick labels.
            ticktext=ticks_formatted,  # (tickformat does not allow for custom timezone formatting)
            fixedrange=True,  # Disable zooming of the chart
            title_text=gettext('detect time')
        ),
        yaxis=pgo.layout.YAxis(
            linecolor=chart_const.AXIS_LINE_COLOR,
            gridcolor=chart_const.GRID_COLOR,
            fixedrange=True,  # Disable zooming of the chart
            title_text=gettext('count')
        ),
        legend=pgo.layout.Legend(
            orientation="h",
            yanchor="bottom",
            y=1,
            xanchor="right",
            x=1
        ),
        autosize=True,
        plot_bgcolor=chart_const.TRANSPARENT,
        paper_bgcolor=chart_const.TRANSPARENT
    )

    return _chart_set_config_and_get_dict(fig)


def get_pie_chart_json(df: pd.DataFrame, chsection: ChartSection) -> ChartJSONType:
    """
    Generate a pie chart as a JSON object for rendering using plotly.
    """
    fig = px.pie(
        df,
        values='count',
        names='set',
        labels={
            'set': str(chsection.column_name),
            'count': str(chsection.value_formats.column_name)
        },
        color_discrete_sequence=chart_const.COLOR_LIST,
        hole=0.5,
        hover_data={
            'count': chsection.value_formats.d3_format
        }
    )
    fig.update_layout(
        showlegend=False
    )
    return _chart_set_config_and_get_dict(fig)


def get_bar_chart_json(df: pd.DataFrame, chsection: ChartSection) -> ChartJSONType:
    """
    Generate a bar chart as a JSON object for rendering using plotly.
    """
    fig = px.bar(
        df,
        orientation='h',
        x='count',
        y='set',
        labels={
            'set': str(chsection.column_name),
            'count': str(chsection.value_formats.column_name)
        },
    )
    fig.update_layout(
        xaxis=pgo.layout.XAxis(
            linecolor=chart_const.AXIS_LINE_COLOR,
            gridcolor=chart_const.GRID_COLOR,
            fixedrange=True,  # Disable zooming of the chart
            title_text=gettext('count')
        ),
        yaxis=pgo.layout.YAxis(
            linecolor=chart_const.AXIS_LINE_COLOR,
            fixedrange=True,  # Disable zooming of the chart
            autorange="reversed"  # Show highest counts first
        ),
        autosize=True,
        plot_bgcolor=chart_const.TRANSPARENT,
        paper_bgcolor=chart_const.TRANSPARENT
    )

    return _chart_set_config_and_get_dict(fig)
