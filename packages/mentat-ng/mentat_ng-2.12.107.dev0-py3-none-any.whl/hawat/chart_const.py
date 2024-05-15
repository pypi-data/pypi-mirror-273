import datetime
from enum import Enum
from numbers import Number
from typing import Any, Dict, NamedTuple, NewType, Optional, Callable, Tuple, Union, List

from flask_babel import lazy_gettext, format_decimal
from flask_babel.speaklater import LazyString
from mentat.stats import idea
import hawat.utils


KEY_CHARTS = 'charts'
KEY_TABLE_DATA = 'table_data'

KEY_CHART_TIMELINE = 'timeline'
KEY_CHART_SECONDARY = 'secondary'

KEY_SUM = '__SUM__'
KEY_SHARE = '__SHARE__'

# Colors taken from d3.scale.category20()
CATEGORY20_COLORS = [
    '#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78',
    '#2ca02c', '#98df8a', '#d62728', '#ff9896',
    '#9467bd', '#c5b0d5', '#8c564b', '#c49c94',
    '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7',
    '#bcbd22', '#dbdb8d', '#17becf', '#9edae5'
]

COLOR_LIST = CATEGORY20_COLORS
"""Used colors for the charts and tables."""

AXIS_LINE_COLOR = 'black'
GRID_COLOR = 'lightgray'
TRANSPARENT = 'rgb(255, 255, 255, 0)'

NUMBER_OF_LABELED_TICKS = 12
MAX_VALUE_COUNT = 20

CHART_PX_HEIGHT = 700

CHART_CSS_DIMENSIONS = f'width: 100%; height: {CHART_PX_HEIGHT}px;'

DataRowType = Dict[str, Union[datetime.datetime, Number]]
ChartJSONType = NewType('ChartJSONType', Dict[str, Any])

StatisticsDataType = Dict[str, Union[Number, Dict[str, Number]]]
DataWideType = List[Tuple[datetime.datetime, StatisticsDataType]]
DataLongType = List[DataRowType]

TimelineCfgType = Dict[str, Union[int, datetime.datetime, datetime.timedelta]]


class InputDataFormat(Enum):
    """
    There are several data formats used in mentat, and each enum is assigned to a
    data format which is then unified to a single-format pandas dataframes for generating charts
    and rendering tables.
    """

    WIDE_SIMPLE = 'wide_simple'
    """
        Provided keys should be a list of tuples, where the first element is the key and second
        element is the translation string, which will appear in the charts and tables.
        Under each key in the provided data is only a single number expected.
        example:
            key: [
                ('cnt_events', 'reported'),
                ('cnt_events_filtered', 'filtered'),
                ('cnt_events_thresholded', 'thresholded')
            ]
            data: [
                [datetime(1970, 1, 1, 0, 0), {
                    'cnt_events': 42,
                    'cnt_events_filtered': 4,
                    'cnt_events_thresholded': 2,
                    **other_aggregations
                }],
                [datetime(1970, 1, 2, 0, 0), {
                    'cnt_events': 40,
                    'cnt_events_filtered': 4,
                    'cnt_events_thresholded': 0,
                    **other_aggregations
                }],
                *rest_of_the_timeline
            ]
    """

    WIDE_COMPLEX = 'wide_complex'
    """
    Keys of dictionary stored under the provided key are used as columns in the dataframe.
    example:
        key: 'sources'
        data: [
            [datetime(1970, 1, 1, 0, 0), {
                'sources': {
                    '192.168.0.4': 21,
                    '2001:718:1:a200::11:3': 24,
                    **other_ip_counts,
                }
                **other_aggregations
            }],
            *rest_of_the_timeline
        ]
    """

    LONG_SIMPLE = 'long_simple'
    """
    Key is only used to obtain the correct translation if the chart section named tuple is not
    provided.

    The only difference from the complex variant is that it does not have the 'set' column and
    therefore, each bucket timestamp occurs only once in the data.
    This means it is impossible to support other data complexity than NONE.

    example:
        key: 'sources',
        data: [
            {'bucket': datetime(1970, 1, 1, 0, 0), 'count': 123},
            {'bucket': datetime(1970, 1, 2, 0, 0), 'count': 0},
            *rest_of_the_timeline
        ]
    """


    LONG_COMPLEX = 'long_complex'
    """
    Key is only used to obtain the correct translation if the chart section named tuple is not
    provided. And each value name is in the column 'set'. The rows are sorted by buckets, and
    rows with the same bucket are also sorted by the count values.

    example:
        key: 'sources',
        data: [
            {'bucket': datetime(1970, 1, 1, 0, 0), 'set': '192.168.0.4', 'count': 123},
            {'bucket': datetime(1970, 1, 1, 0, 0), 'set': '2001:718:1:a200::11:3', 'count': 23},
            {'bucket': datetime(1970, 1, 2, 0, 0), 'set': '192.168.0.4', 'count': 234},
            {'bucket': datetime(1970, 1, 2, 0, 0), 'set': '2001:718:1:a200::11:3', 'count': 0},
            *rest_of_the_timeline
        ]
    """


class DataKey(NamedTuple):
    key: str
    display_name: Union[LazyString, str]


class DataComplexity(Enum):
    NONE = 'none'
    """Only a single number per each timeline bucket. Does not generate a secondary chart"""

    SINGLE = 'single'
    """Each event has at most 1 possible value assigned to it. Generates a pie chart"""

    MULTI = 'multi'
    """Each event has a list of values assigned to it. Generates a bar chart"""


class ValueFormats(NamedTuple):
    column_name: Union[LazyString, str] = lazy_gettext('Count')
    """Name for the column containing the value. Shown in tables and charts on hover."""

    format_function: Callable = format_decimal
    """Function to be used for formatting values under 'count' in tables."""

    d3_format: Union[str, bool] = True
    """
    D3 format string to be used for formatting values in hover text for charts.
    If True, the plotly default format is used. If False, value is omitted.
    """


class ChartSection(NamedTuple):
    key: str
    """Key, under which chart and table date is expected to be stored in the response context."""

    label: Union[LazyString, str]
    """Name shown on the tab label."""

    short_description: Union[LazyString, str, None]
    """Text shown as the header of the tab."""

    description: Union[LazyString, str, None]
    """Long, descriptive text shown right under the header of the tab."""

    data_complexity: DataComplexity
    """Used to differentiate which secondary chart to use."""

    column_name: Union[LazyString, str]
    """
    Name for column containing the aggregated categories.
    Shown in charts on hover, and the rendered table.
    """

    value_formats: ValueFormats = ValueFormats()
    """Formats for the values in the tables and charts."""

    csag_group: Optional[str] = None
    """
    Context search group the aggregated categories belong to.
    If unset, `key` is used.
    """

    allow_table_aggregation: Optional[bool] = None
    """
    Enables/disables aggregation footers in the chart tables.
    If unset, timeline charts, and pie charts will contain aggregation footer,
    secondary bar charts will not.
    """

    data_keys: Optional[List[DataKey]] = None
    """
    Keys which store the data for visualization in WIDE SIMPLE data format.
    If the data format is not WIDE_SIPMLE, this is ignored.
    If None, only the single key stored in `key` will be used.
    """


CHART_SECTIONS = [
    ChartSection(
        idea.ST_SKEY_ABUSES,
        lazy_gettext('abuses'),
        lazy_gettext('Number of events per abuse'),
        lazy_gettext(
            'This view shows total numbers of IDEA events aggregated according to a source '
            '<em>abuse group</em>. The source <em>abuse group</em> is assigned according to all '
            'source addresses contained in the event, multiple source <em>abuse groups</em> can '
            'therefore be assigned to the event and the total numbers in these charts may differ '
            'from the total number of events displayed in the table above.'
        ),
        DataComplexity.MULTI,
        lazy_gettext('Abuse group')
    ),
    ChartSection(
        idea.ST_SKEY_ANALYZERS,
        lazy_gettext('analyzers'),
        lazy_gettext('Number of events per analyzer'),
        lazy_gettext(
            'This view shows total numbers of IDEA events aggregated according to an '
            '<em>analyzer</em>. In the context of Mentat system and IDEA events the '
            '<em>analyzer</em> is a name of a software that detected or emited the IDEA event. '
            'Multiple <em>analyzers</em> can be assigned to the event and therefore the total '
            'numbers in these charts may differ from the total number of events displayed in the '
            'table above.'
        ),
        DataComplexity.MULTI,
        lazy_gettext('Analyzer')
    ),
    ChartSection(
        idea.ST_SKEY_ASNS,
        lazy_gettext('ASNs'),
        lazy_gettext('Number of events per ASN'),
        lazy_gettext(
            'This view shows total numbers of IDEA events aggregated according to a source '
            '<em>autonomous system number</em> (<abbr>ASN</abbr>). The source <em>ASN</em> is '
            'assigned according to all source addresses contained in the event, multiple source '
            '<em>ASNs</em> can therefore be assigned to the event and the total numbers in these '
            'charts may differ from the total number of events displayed in the table above.'
        ),
        DataComplexity.MULTI,
        lazy_gettext('ASN')
    ),
    ChartSection(
        idea.ST_SKEY_CATEGORIES,
        lazy_gettext('categories'),
        lazy_gettext('Number of events per category'),
        lazy_gettext(
            'This view shows total numbers of IDEA events aggregated according to a '
            '<em>category</em>. Multiple <em>categories</em> can be assigned to the event and '
            'therefore the total numbers in these charts may differ from the total number of '
            'events displayed in the table above.'
        ),
        DataComplexity.MULTI,
        lazy_gettext('Category')
    ),
    ChartSection(
        idea.ST_SKEY_CATEGSETS,
        lazy_gettext('category sets'),
        lazy_gettext('Number of events per category set'),
        lazy_gettext(
            'This view shows total numbers of IDEA events aggregated according to a <em>category '
            'set</em>. The <em>category set</em> is a string concatenation of alphabetically '
            'ordered unique set of all event categories and so it provides different grouped view '
            'of the event category statistics.'
        ),
        DataComplexity.SINGLE,
        lazy_gettext('Category set')
    ),
    ChartSection(
        idea.ST_SKEY_COUNTRIES,
        lazy_gettext('countries'),
        lazy_gettext('Number of events per country'),
        lazy_gettext(
            'This view shows total numbers of IDEA events aggregated according to a source '
            '<em>country</em>. The source <em>country</em> is assigned according to all source '
            'addresses contained in the event, multiple source <em>countries</em> can therefore '
            'be assigned to the event and the total numbers in these charts may differ from the '
            'total number of events displayed in the table above.'
        ),
        DataComplexity.MULTI,
        lazy_gettext('Country')
    ),
    ChartSection(
        idea.ST_SKEY_DETECTORS,
        lazy_gettext('detectors'),
        lazy_gettext('Number of events per detector'),
        lazy_gettext(
            'This view shows total numbers of IDEA events aggregated according to a '
            '<em>detector</em>. In the context of Mentat system and IDEA events the '
            '<em>detector</em> is an unique name of the node on which the IDEA event was detected '
            'or emited.'
        ),
        DataComplexity.SINGLE,
        lazy_gettext('Detector')
    ),
    ChartSection(
        idea.ST_SKEY_DETECTORSWS,
        lazy_gettext('detector software'),
        lazy_gettext('Number of events per detector software'),
        lazy_gettext(
            'This view shows total numbers of IDEA events aggregated according to a <em>detector '
            'software</em>. The <em>detector software</em> is a string concatenation of detector '
            'and analyzer names. Because an event may contain multiple analyzer names, multiple '
            '<em>detector software</em> strings can be produced for each event and the total '
            'numbers in these charts may differ from the total number of events displayed in the '
            'table above.'
        ),
        DataComplexity.MULTI,
        lazy_gettext('Detector software')
        ),
    ChartSection(
        idea.ST_SKEY_DETECTORTPS,
        lazy_gettext('detector tags'),
        lazy_gettext('Number of events per detector type'),
        lazy_gettext(
            'This view shows total numbers of IDEA events aggregated according to a <em>detector '
            'type</em>. In the context of Mentat system and IDEA events each <em>detector</em> is '
            'an unique name of the node on which the IDEA event was detected or emited and each '
            'may be assigned one or more tags to describe its type. Because an event may contain '
            'multiple <em>detector type tags</em>, the total numbers in these charts may differ '
            'from the total number of events displayed in the table above.'
        ),
        DataComplexity.MULTI,
        lazy_gettext('Detector type')
    ),
    ChartSection(
        idea.ST_SKEY_SOURCES,
        lazy_gettext('sources'),
        lazy_gettext('Number of events per source IP'),
        lazy_gettext(
            'This view shows total numbers of IDEA events aggregated according to a <em>source IP '
            'address</em>. Because an event may contain multiple <em>source IP addresses</em>, '
            'the total numbers in these charts may differ from the total number of events '
            'displayed in the table above.'
        ),
        DataComplexity.MULTI,
        lazy_gettext('Source IP'),
        csag_group='ips'
    ),
    ChartSection(
        idea.ST_SKEY_TARGETS,
        lazy_gettext('targets'),
        lazy_gettext('Number of events per target IP'),
        lazy_gettext(
            'This view shows total numbers of IDEA events aggregated according to a <em>target IP '
            'address</em>. Because an event may contain multiple <em>target IP addresses</em>, '
            'the total numbers in these charts may differ from the total number of events '
            'displayed in the table above.'
        ),
        DataComplexity.MULTI,
        lazy_gettext('Target IP'),
        csag_group='ips'
    ),
    ChartSection(
        idea.ST_SKEY_SRCPORTS,
        lazy_gettext('source ports'),
        lazy_gettext('Number of events per source port'),
        lazy_gettext(
            'This view shows total numbers of IDEA events aggregated according to a <em>source '
            'port</em>. Because an event may contain multiple <em>source ports</em>, the total '
            'numbers in these charts may differ from the total number of events displayed in the '
            'table above.'
        ),
        DataComplexity.MULTI,
        lazy_gettext('Source port'),
        csag_group='ports'
    ),
    ChartSection(
        idea.ST_SKEY_TGTPORTS,
        lazy_gettext('target ports'),
        lazy_gettext('Number of events per target port'),
        lazy_gettext(
            'This view shows total numbers of IDEA events aggregated according to a <em>target '
            'port</em>. Because an event may contain multiple <em>target ports</em>, the total '
            'numbers in these charts may differ from the total number of events displayed in the '
            'table above.'
        ),
        DataComplexity.MULTI,
        lazy_gettext('Target port'),
        csag_group='ports'
    ),
    ChartSection(
        idea.ST_SKEY_PROTOCOLS,
        lazy_gettext('protocols'),
        lazy_gettext('Number of events per protocol/service'),
        lazy_gettext(
            'This view shows total numbers of IDEA events aggregated according to a <em>protocol '
            'or service</em>. Because an event may contain multiple <em>protocols</em>, the total '
            'numbers in these charts may differ from the total number of events displayed in the '
            'table above.'
        ),
        DataComplexity.MULTI,
        lazy_gettext('Protocol')
    ),
    ChartSection(
        idea.ST_SKEY_SRCTYPES,
        lazy_gettext('source types'),
        lazy_gettext('Number of events per source type'),
        lazy_gettext(
            'This view shows total numbers of IDEA events aggregated according to a <em>source '
            'type</em>. Because an event may contain multiple <em>source type tags</em>, the '
            'total numbers in these charts may differ from the total number of events displayed '
            'in the table above.'
        ),
        DataComplexity.MULTI,
        lazy_gettext('Source type')
    ),
    ChartSection(
        idea.ST_SKEY_TGTTYPES,
        lazy_gettext('target types'),
        lazy_gettext('Number of events per target type'),
        lazy_gettext(
            'This view shows total numbers of IDEA events aggregated according to a <em>target '
            'type</em>. Because an event may contain multiple <em>target type tags</em>, the '
            'total numbers in these charts may differ from the total number of events displayed '
            'in the table above.'
        ),
        DataComplexity.MULTI,
        lazy_gettext('Target type')
    ),
    ChartSection(
        idea.ST_SKEY_CLASSES,
        lazy_gettext('classes'),
        lazy_gettext('Number of events per class'),
        lazy_gettext(
            'This view shows total numbers of IDEA events aggregated according to an event '
            '<em>classification</em>. The event <em>class</em> is a catalogization mechanism '
            'similar to the categories. It is however internal only to Mentat system and attempts '
            'to group different events describing the same type of incidents.'
        ),
        DataComplexity.SINGLE,
        lazy_gettext('Event class')
    ),
    ChartSection(
        idea.ST_SKEY_SEVERITIES,
        lazy_gettext('severities'),
        lazy_gettext('Number of events per severity'),
        lazy_gettext(
            'This view shows total numbers of IDEA events aggregated according to an event '
            '<em>severity</em>. The event <em>severity</em> is internal only to Mentat system and '
            'is assigned by predefined set of rules based on the event classification.'
        ),
        DataComplexity.SINGLE,
        lazy_gettext('Severity')
    )
]

CHART_SECTION_MAP = {chs.key: chs for chs in CHART_SECTIONS}


class TableAggregation(NamedTuple):
    func: Union[Callable, str]  # function to be used for aggregation, or its name in pandas,
    icon_name: str
    name: Union[LazyString, str]
    tooltip: Union[LazyString, str]
    format_func: Callable = hawat.utils.fallback_formatter(format_decimal)


TABLE_AGGREGATIONS = [
    TableAggregation(
        'sum',
        'sum',
        lazy_gettext('Sum'),
        lazy_gettext('Sum of all values')
    ),
    TableAggregation(
        'min',
        'min',
        lazy_gettext('Minimum'),
        lazy_gettext('Minimal value')
    ),
    TableAggregation(
        'max',
        'max',
        lazy_gettext('Maximum'),
        lazy_gettext('Maximal value'),
    ),
    TableAggregation(
        'mean',
        'avg',
        lazy_gettext('Average'),
        lazy_gettext('Average value')
    ),
    TableAggregation(
        'median',
        'med',
        lazy_gettext('Median'),
        lazy_gettext('Median value')
    ),
    TableAggregation(
        'count',
        'cnt',
        lazy_gettext('Count'),
        lazy_gettext('Count of all values')
    )
]
