# Copyright (c) 2014 Riverbed Technology, Inc.
#
# This software is licensed under the terms and conditions of the MIT License
# accompanying the software ("License").  This software is distributed "AS IS"
# as set forth in the License.

from __future__ import (unicode_literals, print_function, division,
                        absolute_import)

import mock
import pytest

from steelscript.common.interaction.action import Action


SHOW_VERSION_PARSED = {
    'product name': 'rbt_sh',
    'product release': '9.0.0-rc',
    'build id': '#12',
    'build arch': 'x86_64',
    'built by': 'mockbuild@bannow-worker1',
    'product model': '2050',
    'number of cpus': 4,
}
PRODUCT_INFO = {
    'name': 'SteelHead',
    'model': '2050',
    'release': '9.0.0-rc',
}


@pytest.fixture
def actor(mock_model):
    return Action.get(mock.Mock(), feature='common')


@pytest.yield_fixture
def mock_model():
    with mock.patch('steelscript.common.interaction.uidelegation.'
                    'CLIDelegatee.model') as mock_model:
        yield mock_model


def test_get_product_info(actor, mock_model):
    mock_model.show_version.return_value = SHOW_VERSION_PARSED
    assert actor.get_product_info() == PRODUCT_INFO
