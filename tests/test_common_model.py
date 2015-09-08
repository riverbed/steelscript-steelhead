# Copyright (c) 2015 Riverbed Technology, Inc.
#
# This software is licensed under the terms and conditions of the MIT License
# accompanying the software ("License").  This software is distributed "AS IS"
# as set forth in the License.

from __future__ import (unicode_literals, print_function, division,
                        absolute_import)

import mock
import pytest

from steelscript.steelhead.features.common.v8_5.model import CommonModel


SHOW_VERSION_OUTPUT = """
Product name:      rbt_sh
Product release:   9.0.0-rc
Build ID:          #12
Build date:        2014-11-19 17:07:32
Build arch:        x86_64
Built by:          mockbuild@bannow-worker1

Uptime:            14d 17h 8m 48s

Product model:     2050
System memory:     7925 MB used / 71 MB free / 7997 MB total
Number of CPUs:    4
CPU load averages: 0.71 / 0.77 / 0.79
"""
SHOW_VERSION_PARSED = {
    'product name': 'rbt_sh',
    'product release': '9.0.0-rc',
    'build id': '#12',
    'build arch': 'x86_64',
    'built by': 'mockbuild@bannow-worker1',
    'product model': '2050',
    'number of cpus': 4,
}


@pytest.yield_fixture
def mock_cli():
    with mock.patch('steelscript.common.interaction.model.Model.cli') as cli:
        yield cli


def test_show_interfaces_configured(mock_cli):
    model = CommonModel(mock.Mock(), cli=mock_cli)
    mock_cli.exec_command.return_value = SHOW_VERSION_OUTPUT
    return_dict = model.show_version()
    assert return_dict == SHOW_VERSION_PARSED
