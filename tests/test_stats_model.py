# Copyright (c) 2015 Riverbed Technology, Inc.
#
# This software is licensed under the terms and conditions of the MIT License
# accompanying the software ("License").  This software is distributed "AS IS"
# as set forth in the License.

from __future__ import (absolute_import, unicode_literals, print_function,
                        division)

import mock
import pytest

from steelscript.steelhead.features.stats.v8_5.model import StatsModel\
    as CommonStats


SHOW_STATS_ALL_OUTPUT = """\
WAN Data:                 4.2 MB
LAN Data:                 66 MB
Data Reduction:           93 %
Data Reduction Peak:      98 %
Data Reduction Peak Time: 2014/12/09 08:39:35
Capacity Increase:        15.4 X
"""

SHOW_STATS_ALL_PARSED_DICT = {
    'wan data': '4.2 MB',
    'lan data': '66 MB',
    'data reduction': 93,
    'data reduction peak': 98,
    'data reduction peak time': '2014/12/09 08:39:35',
    'capacity increase': 15.4
}


@pytest.yield_fixture
def mock_cli(request):
    with mock.patch('steelscript.common.interaction.model.Model.cli') as cli:
        yield cli


def test_show_stats(mock_cli):
    model = CommonStats(mock.Mock(), cli=mock_cli)
    mock_cli.exec_command.return_value = SHOW_STATS_ALL_OUTPUT
    result = model.show_stats_bandwidth('all', 'bi-directional', '5min')
    assert result == SHOW_STATS_ALL_PARSED_DICT
