#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Tests for :py:mod:`hawat.charts`.
"""


import unittest
import datetime
import pandas as pd

from hawat.test import HawatTestCase
from hawat.test.runner import TestRunnerMixin
from hawat import charts, chart_const

class ChartsTestCase(TestRunnerMixin, HawatTestCase):
    """
    Class for testing :py:class:`hawat.charts`.
    """

    def test_get_datetime_format_function_utc_10min_step(self):
        """
        Test the function :py:func:`hawat.utils.get_datetime_format_function`.
        """
        timeline_cfg = {
            'dt_from': datetime.datetime(2020, 1, 1, 0, 0, 0),
            'dt_to': datetime.datetime(2020, 1, 1, 13, 0, 0),
            'step': datetime.timedelta(minutes=10)
        }
        f = charts.get_datetime_format_function(timeline_cfg, timezone='UTC')

        self.assertEqual(
            f(datetime.datetime(2020, 1, 1, 0, 0, 0)),
            '00:00'
        )
        self.assertEqual(
            f(datetime.datetime(2020, 1, 1, 0, 10, 0)),
            '00:10'
        )
        self.assertEqual(
            f(datetime.datetime(2020, 1, 1, 12, 10, 0)),
            '12:10'
        )

    def test_get_datetime_format_function_utc_10sec_step(self):
        """
        Test the function :py:func:`hawat.utils.get_datetime_format_function`.
        """
        timeline_cfg = {
            'dt_from': datetime.datetime(2020, 1, 1, 0, 0, 0),
            'dt_to': datetime.datetime(2020, 1, 1, 13, 0, 0),
            'step': datetime.timedelta(seconds=10)
        }
        f = charts.get_datetime_format_function(timeline_cfg, timezone='UTC')

        self.assertEqual(
            f(datetime.datetime(2020, 1, 1, 0, 0, 0)),
            '00:00'
        )
        self.assertEqual(
            f(datetime.datetime(2020, 1, 1, 0, 10, 20)),
            '00:10:20'
        )
        self.assertEqual(
            f(datetime.datetime(2020, 1, 1, 12, 10, 20)),
            '12:10:20'
        )

    def test_get_datetime_format_function_utc_05sec_step(self):
        """
        Test the function :py:func:`hawat.utils.get_datetime_format_function`.
        """
        timeline_cfg = {
            'dt_from': datetime.datetime(2020, 1, 1, 0, 0, 0),
            'dt_to': datetime.datetime(2020, 1, 1, 13, 0, 0),
            'step': datetime.timedelta(milliseconds=500)
        }
        f = charts.get_datetime_format_function(timeline_cfg, timezone='UTC')

        self.assertEqual(
            f(datetime.datetime(2020, 1, 1, 0, 0, 0)),
            '00:00.000000'
        )
        self.assertEqual(
            f(datetime.datetime(2020, 1, 1, 0, 10, 20, 500000)),
            '10:20.500000'
        )
        self.assertEqual(
            f(datetime.datetime(2020, 1, 1, 12, 10, 20, 500000)),
            '10:20.500000'
        )

    def test_get_datetime_format_function_utc_2day_step(self):
        """
        Test the function :py:func:`hawat.utils.get_datetime_format_function`.
        """
        timeline_cfg = {
            'dt_from': datetime.datetime(2020, 1, 1, 0, 0, 0),
            'dt_to': datetime.datetime(2020, 1, 20, 0, 0, 0),
            'step': datetime.timedelta(days=2)
        }
        f = charts.get_datetime_format_function(timeline_cfg, timezone='UTC')

        self.assertEqual(
            f(datetime.datetime(2020, 1, 1, 0, 0, 0)),
            '2020-01-01'
        )
        self.assertEqual(
            f(datetime.datetime(2020, 1, 3, 0, 0, 0)),
            '2020-01-03'
        )
        self.assertEqual(
            f(datetime.datetime(2020, 1, 11, 0, 0, 0)),
            '2020-01-11'
        )

    def test_get_datetime_format_function_npt_10min_step(self):
        """
        Test the function :py:func:`hawat.utils.get_datetime_format_function`.
        """
        timeline_cfg = {
            'dt_from': datetime.datetime(2020, 1, 1, 0, 0, 0),
            'dt_to': datetime.datetime(2020, 1, 1, 13, 0, 0),
            'step': datetime.timedelta(minutes=10)
        }
        f = charts.get_datetime_format_function(timeline_cfg, timezone='Asia/Kathmandu')

        self.assertEqual(
            f(datetime.datetime(2020, 1, 1, 0, 0, 0)),
            '05:45'
        )
        self.assertEqual(
            f(datetime.datetime(2020, 1, 1, 0, 10, 0)),
            '05:55'
        )
        self.assertEqual(
            f(datetime.datetime(2020, 1, 1, 12, 20, 0)),
            '18:05'
        )

    def test_get_datetime_format_function_npt_10sec_step(self):
        """
        Test the function :py:func:`hawat.utils.get_datetime_format_function`.
        """
        timeline_cfg = {
            'dt_from': datetime.datetime(2020, 1, 1, 0, 0, 0),
            'dt_to': datetime.datetime(2020, 1, 1, 13, 0, 0),
            'step': datetime.timedelta(seconds=10)
        }
        f = charts.get_datetime_format_function(timeline_cfg, timezone='Asia/Kathmandu')

        self.assertEqual(
            f(datetime.datetime(2020, 1, 1, 0, 0, 0)),
            '05:45'
        )
        self.assertEqual(
            f(datetime.datetime(2020, 1, 1, 0, 10, 20)),
            '05:55:20'
        )
        self.assertEqual(
            f(datetime.datetime(2020, 1, 1, 12, 15, 20)),
            '18:00:20'
        )

    def test_get_datetime_format_function_npt_05sec_step(self):
        """
        Test the function :py:func:`hawat.utils.get_datetime_format_function`.
        """
        timeline_cfg = {
            'dt_from': datetime.datetime(2020, 1, 1, 0, 0, 0),
            'dt_to': datetime.datetime(2020, 1, 1, 13, 0, 0),
            'step': datetime.timedelta(milliseconds=500)
        }
        f = charts.get_datetime_format_function(timeline_cfg, timezone='Asia/Kathmandu')

        self.assertEqual(
            f(datetime.datetime(2020, 1, 1, 0, 0, 0)),
            '45:00.000000'
        )
        self.assertEqual(
            f(datetime.datetime(2020, 1, 1, 0, 10, 20, 500000)),
            '55:20.500000'
        )
        self.assertEqual(
            f(datetime.datetime(2020, 1, 1, 12, 20, 20, 500000)),
            '05:20.500000'
        )

    def test_get_datetime_format_function_npt_2day_step(self):
        """
        Test the function :py:func:`hawat.utils.get_datetime_format_function`.
        """
        timeline_cfg = {
            'dt_from': datetime.datetime(2020, 1, 1, 0, 0, 0),
            'dt_to': datetime.datetime(2020, 1, 20, 0, 0, 0),
            'step': datetime.timedelta(days=2)
        }
        f = charts.get_datetime_format_function(timeline_cfg, timezone='Asia/Kathmandu')

        self.assertEqual(
            f(datetime.datetime(2020, 1, 1, 0, 0, 0)),
            '2020-01-01'
        )
        self.assertEqual(
            f(datetime.datetime(2020, 1, 3, 0, 0, 0)),
            '2020-01-03'
        )
        self.assertEqual(
            f(datetime.datetime(2020, 1, 11, 20, 0, 0)),
            '2020-01-12'
        )

    def test_get_secondary_chart_and_table_dataframe(self):
        """
        Test the function :py:func:`hawat.charts.get_secondary_chart_and_table_dataframe`.
        """
        chart, table = charts.get_secondary_chart_and_table_data_frame(
            {'test_chart': {'b': 2, 'a': 1, 'c': 3}},
            chart_const.ChartSection(
                'test_chart',
                'Test chart label',
                None,
                None,
                chart_const.DataComplexity.MULTI,
                'Test chart column name',
            ),
            chart_const.InputDataFormat.WIDE_COMPLEX
        )
        self.assertIsInstance(chart, dict)
        expected = pd.DataFrame(
            [
                {'set': 'b', 'count': 2, '__SHARE__': 2/6},
                {'set': 'a', 'count': 1, '__SHARE__': 1/6},
                {'set': 'c', 'count': 3, '__SHARE__': 3/6}
            ]
        )
        self.assertTrue(
            (table.reset_index() == expected).all().all(),
            f"Expected:\n{repr(expected)}\nbut found:\n{repr(table.reset_index())}",
        )

    def test_get_secondary_chart_and_table_dataframe_sort(self):
        """
        Test the function :py:func:`hawat.charts.get_secondary_chart_and_table_dataframe`.
        """
        chart, table = charts.get_secondary_chart_and_table_data_frame(
            {'test_chart': {'b': 2, 'a': 1, 'c': 3}},
            chart_const.ChartSection(
                'test_chart',
                'Test chart label',
                None,
                None,
                chart_const.DataComplexity.MULTI,
                'Test chart column name',
            ),
            chart_const.InputDataFormat.WIDE_COMPLEX,
            sort=True
        )
        self.assertIsInstance(chart, dict)
        expected = pd.DataFrame(
            [
                {'set': 'c', 'count': 3, '__SHARE__': 3/6},
                {'set': 'b', 'count': 2, '__SHARE__': 2/6},
                {'set': 'a', 'count': 1, '__SHARE__': 1/6}
            ]
        )
        self.assertTrue(
            (table.reset_index() == expected).all().all(),
            f"Expected:\n{repr(expected)}\nbut found:\n{repr(table.reset_index())}",
        )

    def test_get_secondary_chart_and_table_dataframe_rest1(self):
        """
        Test the function :py:func:`hawat.charts.get_secondary_chart_and_table_dataframe`.
        """
        chart, table = charts.get_secondary_chart_and_table_data_frame(
            {'test_chart': {'b': 2, 'a': 1, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9,
                            'j': 10, 'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15, 'p': 16, 'q': 17,
                            'r': 18, 's': 19, 't': 20}},
            chart_const.ChartSection(
                'test_chart',
                'Test chart label',
                None,
                None,
                chart_const.DataComplexity.MULTI,
                'Test chart column name',
            ),
            chart_const.InputDataFormat.WIDE_COMPLEX,
            sort=True
        )
        self.assertIsInstance(chart, dict)
        expected = pd.DataFrame(
            [
                {'set': 't', 'count': 20, '__SHARE__': 20 / 210},
                {'set': 's', 'count': 19, '__SHARE__': 19 / 210},
                {'set': 'r', 'count': 18, '__SHARE__': 18 / 210},
                {'set': 'q', 'count': 17, '__SHARE__': 17 / 210},
                {'set': 'p', 'count': 16, '__SHARE__': 16 / 210},
                {'set': 'o', 'count': 15, '__SHARE__': 15 / 210},
                {'set': 'n', 'count': 14, '__SHARE__': 14 / 210},
                {'set': 'm', 'count': 13, '__SHARE__': 13 / 210},
                {'set': 'l', 'count': 12, '__SHARE__': 12 / 210},
                {'set': 'k', 'count': 11, '__SHARE__': 11 / 210},
                {'set': 'j', 'count': 10, '__SHARE__': 10 / 210},
                {'set': 'i', 'count': 9, '__SHARE__': 9 / 210},
                {'set': 'h', 'count': 8, '__SHARE__': 8 / 210},
                {'set': 'g', 'count': 7, '__SHARE__': 7 / 210},
                {'set': 'f', 'count': 6, '__SHARE__': 6 / 210},
                {'set': 'e', 'count': 5, '__SHARE__': 5 / 210},
                {'set': 'd', 'count': 4, '__SHARE__': 4 / 210},
                {'set': 'c', 'count': 3, '__SHARE__': 3 / 210},
                {'set': 'b', 'count': 2, '__SHARE__': 2 / 210},
                {'set': 'a', 'count': 1, '__SHARE__': 1 / 210}
            ]
        )
        self.assertTrue(
            (table.reset_index() == expected).all().all(),
            f"Expected:\n{repr(expected)}\nbut found:\n{repr(table.reset_index())}",
        )

    def test_get_secondary_chart_and_table_dataframe_rest2(self):
        """
        Test the function :py:func:`hawat.charts.get_secondary_chart_and_table_dataframe`.
        """
        chart, table = charts.get_secondary_chart_and_table_data_frame(
            {'test_chart': {'b': 2, 'a': 1, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9,
                            'j': 10, 'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15, 'p': 16, 'q': 17,
                            'r': 18, 's': 19, 't': 20, 'u': 21}},
            chart_const.ChartSection(
                'test_chart',
                'Test chart label',
                None,
                None,
                chart_const.DataComplexity.SINGLE,
                'Test chart column name',
            ),
            chart_const.InputDataFormat.WIDE_COMPLEX,
            add_rest=True,
            sort=True
        )
        self.assertIsInstance(chart, dict)
        expected = pd.DataFrame(
            [
                {'set': 'u', 'count': 21, '__SHARE__': 21 / 231},
                {'set': 't', 'count': 20, '__SHARE__': 20 / 231},
                {'set': 's', 'count': 19, '__SHARE__': 19 / 231},
                {'set': 'r', 'count': 18, '__SHARE__': 18 / 231},
                {'set': 'q', 'count': 17, '__SHARE__': 17 / 231},
                {'set': 'p', 'count': 16, '__SHARE__': 16 / 231},
                {'set': 'o', 'count': 15, '__SHARE__': 15 / 231},
                {'set': 'n', 'count': 14, '__SHARE__': 14 / 231},
                {'set': 'm', 'count': 13, '__SHARE__': 13 / 231},
                {'set': 'l', 'count': 12, '__SHARE__': 12 / 231},
                {'set': 'k', 'count': 11, '__SHARE__': 11 / 231},
                {'set': 'j', 'count': 10, '__SHARE__': 10 / 231},
                {'set': 'i', 'count': 9, '__SHARE__': 9 / 231},
                {'set': 'h', 'count': 8, '__SHARE__': 8 / 231},
                {'set': 'g', 'count': 7, '__SHARE__': 7 / 231},
                {'set': 'f', 'count': 6, '__SHARE__': 6 / 231},
                {'set': 'e', 'count': 5, '__SHARE__': 5 / 231},
                {'set': 'd', 'count': 4, '__SHARE__': 4 / 231},
                {'set': 'c', 'count': 3, '__SHARE__': 3 / 231},
                {'set': '__REST__', 'count': 3, '__SHARE__': 3 / 231}
            ]
        )
        self.assertTrue(
            (table.reset_index() == expected).all().all(),
            f"Expected:\n{repr(expected)}\nBut found:\n{repr(table.reset_index())}",
        )

    def test_get_secondary_chart_and_table_dataframe_wide_simple(self):
        """
        Test the function :py:func:`hawat.charts.get_secondary_chart_and_table_dataframe`.
        """
        chart, table = charts.get_secondary_chart_and_table_data_frame(
            {'b': 2, 'a': 1, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9,
             'j': 10, 'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15, 'p': 16, 'q': 17,
             'r': 18, 's': 19, 't': 20, 'u': 21},
            chart_const.ChartSection(
                'test_chart',
                'Test chart label',
                None,
                None,
                chart_const.DataComplexity.MULTI,
                'Test chart column name',
                data_keys=[
                    chart_const.DataKey('a', 'Key A'),
                    chart_const.DataKey('u', 'Key U')
                ]
            ),
            chart_const.InputDataFormat.WIDE_SIMPLE,
            add_rest=True,
            sort=True
        )
        self.assertIsInstance(chart, dict)
        expected = pd.DataFrame(
            [
                {'set': 'Key U', 'count': 21, '__SHARE__': 21 / 22},
                {'set': 'Key A', 'count': 1, '__SHARE__': 1 / 22}
            ]
        )
        self.assertTrue(
            (table.reset_index() == expected).all().all(),
            f"Expected:\n{repr(expected)}\nBut found:\n{repr(table.reset_index())}",
        )

    def test_get_secondary_chart_and_table_dataframe_wide_simple_datakey_empty(self):
        """
        Test the function :py:func:`hawat.charts.get_secondary_chart_and_table_dataframe`.
        """
        chart, table = charts.get_secondary_chart_and_table_data_frame(
            {'b': 2, 'a': 1, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9,
             'j': 10, 'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15, 'p': 16, 'q': 17,
             'r': 18, 's': 19, 't': 20, 'u': 21},
            chart_const.ChartSection(
                'test_chart',
                'Test chart label',
                None,
                None,
                chart_const.DataComplexity.MULTI,
                'Test chart column name',
                data_keys=[]
            ),
            chart_const.InputDataFormat.WIDE_SIMPLE,
            add_rest=True,
            sort=True
        )
        self.assertIsInstance(chart, dict)
        self.assertTrue(
            table.reset_index().empty,
            f"Expected:\nAn empty DataFrame\nBut found:\n{repr(table.reset_index())}",
        )

    def test_get_timeline_chart_and_table_data_frame_wide_simple(self):
        chart, table = charts.get_timeline_chart_and_table_data_frame(
            [
                [datetime.datetime(1970, 1, 1, 0, 0), {
                    'cnt_events': 42,
                    'cnt_events_filtered': 4,
                    'cnt_events_thresholded': 2
                }],
                [datetime.datetime(1970, 1, 2, 0, 0), {
                    'cnt_events': 40,
                    'cnt_events_filtered': 4,
                    'cnt_events_thresholded': 0
                }],
                [datetime.datetime(1970, 1, 3, 0, 0), {
                    'cnt_events': 51,
                    'cnt_events_filtered': 1,
                    'cnt_events_thresholded': 0
                }]
            ],
            chsection=chart_const.ChartSection(
                'test_chart',
                'Test chart label',
                None,
                None,
                chart_const.DataComplexity.MULTI,
                'Test chart column name',
                data_keys=[
                    chart_const.DataKey('cnt_events', 'reported'),
                    chart_const.DataKey('cnt_events_filtered', 'filtered'),
                    chart_const.DataKey('cnt_events_thresholded', 'thresholded')
                ]
            ),
            timeline_cfg={
                'dt_from': datetime.datetime(1970, 1, 1, 0, 0),
                'dt_to': datetime.datetime(1970, 1, 4, 23, 59),
                'step': datetime.timedelta(days=1)
            },
            data_format=chart_const.InputDataFormat.WIDE_SIMPLE,
            forced_timezone='UTC'
        )
        self.assertIsInstance(chart, dict)
        expected = pd.DataFrame(
            [
                {
                    'bucket': datetime.datetime(1970, 1, 1, 0, 0),
                    'reported': 42,
                    'filtered': 4,
                    'thresholded': 2,
                    '__SUM__': 48
                },
                {
                    'bucket': datetime.datetime(1970, 1, 2, 0, 0),
                    'reported': 40,
                    'filtered': 4,
                    'thresholded': 0,
                    '__SUM__': 44
                },
                {
                    'bucket': datetime.datetime(1970, 1, 3, 0, 0),
                    'reported': 51,
                    'filtered': 1,
                    'thresholded': 0,
                    '__SUM__': 52
                }
            ]
        )
        self.assertTrue(
            (table.reset_index() == expected).all().all(),
            f"Expected:\nAn empty DataFrame\nBut found:\n{repr(table.reset_index())}",
        )

    def test_get_timeline_chart_and_table_data_frame_wide_complex(self):
        chart, table = charts.get_timeline_chart_and_table_data_frame(
            [
                [datetime.datetime(1970, 1, 1, 0, 0), {
                    'sources': {
                        '192.168.0.4': 21,
                        '2001:718:1:a200::11:3': 24
                    }
                }],
                [datetime.datetime(1970, 1, 2, 0, 0), {
                    'sources': {
                        '192.168.0.4': 15,
                        '2001:718:1:a200::11:3': 18
                    }
                }],
                [datetime.datetime(1970, 1, 3, 0, 0), {
                    'sources': {
                        '192.168.0.4': 10,
                        '2001:718:1:a200::11:3': 12
                    }
                }]
            ],
            chsection=chart_const.ChartSection(
                'sources',
                'Test chart label',
                None,
                None,
                chart_const.DataComplexity.MULTI,
                'Test chart column name',
            ),
            timeline_cfg={
                'dt_from': datetime.datetime(1970, 1, 1, 0, 0),
                'dt_to': datetime.datetime(1970, 1, 4, 23, 59),
                'step': datetime.timedelta(days=1)
            },
            data_format=chart_const.InputDataFormat.WIDE_COMPLEX,
            forced_timezone='UTC'
        )
        self.assertIsInstance(chart, dict)
        expected = pd.DataFrame(
            [
                {
                    'bucket': datetime.datetime(1970, 1, 1, 0, 0),
                    '192.168.0.4': 21,
                    '2001:718:1:a200::11:3': 24,
                    '__SUM__': 45
                },
                {
                    'bucket': datetime.datetime(1970, 1, 2, 0, 0),
                    '192.168.0.4': 15,
                    '2001:718:1:a200::11:3': 18,
                    '__SUM__': 33
                },
                {
                    'bucket': datetime.datetime(1970, 1, 3, 0, 0),
                    '192.168.0.4': 10,
                    '2001:718:1:a200::11:3': 12,
                    '__SUM__': 22
                }
            ]
        )
        self.assertTrue(
            (table.reset_index() == expected).all().all(),
            f"Expected:\n{repr(expected)}\nBut found:\n{repr(table.reset_index())}",
        )

    def test_get_timeline_chart_and_table_data_frame_long_simple(self):
        chart, table = charts.get_timeline_chart_and_table_data_frame(
            [
                {'bucket': datetime.datetime(1970, 1, 1, 0, 0), 'count': 123},
                {'bucket': datetime.datetime(1970, 1, 2, 0, 0), 'count': 0},
                {'bucket': datetime.datetime(1970, 1, 3, 0, 0), 'count': 456},
            ],
            chsection=chart_const.ChartSection(
                'sources',
                'Test chart label',
                None,
                None,
                chart_const.DataComplexity.NONE,
                'Test chart column name',
            ),
            timeline_cfg={
                'dt_from': datetime.datetime(1970, 1, 1, 0, 0),
                'dt_to': datetime.datetime(1970, 1, 4, 23, 59),
                'step': datetime.timedelta(days=1)
            },
            data_format=chart_const.InputDataFormat.LONG_SIMPLE,
            forced_timezone='UTC'
        )
        self.assertIsInstance(chart, dict)
        expected = pd.DataFrame(
            [
                {
                    'bucket': datetime.datetime(1970, 1, 1, 0, 0),
                    'Test chart column name': 123,
                    '__SUM__': 123
                },
                {
                    'bucket': datetime.datetime(1970, 1, 2, 0, 0),
                    'Test chart column name': 0,
                    '__SUM__': 0
                },
                {
                    'bucket': datetime.datetime(1970, 1, 3, 0, 0),
                    'Test chart column name': 456,
                    '__SUM__': 456
                }
            ]
        )
        self.assertTrue(
            (table.reset_index() == expected).all().all(),
            f"Expected:\n{repr(expected)}\nBut found:\n{repr(table.reset_index())}",
        )

    def test_get_timeline_chart_and_table_data_frame_long_complex(self):
        chart, table = charts.get_timeline_chart_and_table_data_frame(
            [
                {
                    'bucket': datetime.datetime(1970, 1, 1, 0, 0),
                    'set': '192.168.0.4',
                    'count': 123
                },
                {
                    'bucket': datetime.datetime(1970, 1, 1, 0, 0),
                    'set': '2001:718:1:a200::11:3',
                    'count': 23
                },
                {
                    'bucket': datetime.datetime(1970, 1, 2, 0, 0),
                    'set': '192.168.0.4',
                    'count': 234
                },
                {
                    'bucket': datetime.datetime(1970, 1, 2, 0, 0),
                    'set': '2001:718:1:a200::11:3',
                    'count': 0
                },
                {
                    'bucket': datetime.datetime(1970, 1, 3, 0, 0),
                    'set': '192.168.0.4',
                    'count': 0
                },
                {
                    'bucket': datetime.datetime(1970, 1, 3, 0, 0),
                    'set': '2001:718:1:a200::11:3',
                    'count': 0
                },
            ],
            chsection=chart_const.ChartSection(
                'sources',
                'Test chart label',
                None,
                None,
                chart_const.DataComplexity.SINGLE,
                'Test chart column name',
            ),
            timeline_cfg={
                'dt_from': datetime.datetime(1970, 1, 1, 0, 0),
                'dt_to': datetime.datetime(1970, 1, 4, 23, 59),
                'step': datetime.timedelta(days=1)
            },
            data_format=chart_const.InputDataFormat.LONG_COMPLEX,
            forced_timezone='UTC'
        )
        self.assertIsInstance(chart, dict)
        expected = pd.DataFrame(
            [
                {
                    'bucket': datetime.datetime(1970, 1, 1, 0, 0),
                    '192.168.0.4': 123,
                    '2001:718:1:a200::11:3': 23,
                    '__SUM__': 146
                },
                {
                    'bucket': datetime.datetime(1970, 1, 2, 0, 0),
                    '192.168.0.4': 234,
                    '2001:718:1:a200::11:3': 0,
                    '__SUM__': 234
                },
                {
                    'bucket': datetime.datetime(1970, 1, 3, 0, 0),
                    '192.168.0.4': 0,
                    '2001:718:1:a200::11:3': 0,
                    '__SUM__': 0
                }
            ]
        )
        self.assertTrue(
            (table.reset_index() == expected).all().all(),
            f"Expected:\n{repr(expected)}\nBut found:\n{repr(table.reset_index())}",
        )


#-------------------------------------------------------------------------------


if __name__ == "__main__":
    unittest.main()
