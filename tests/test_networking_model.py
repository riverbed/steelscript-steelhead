# Copyright (c) 2015 Riverbed Technology, Inc.
#
# This software is licensed under the terms and conditions of the MIT License
# accompanying the software ("License").  This software is distributed "AS IS"
# as set forth in the License.

from __future__ import (unicode_literals, print_function, division,
                        absolute_import)

import datetime
import ipaddress
import netaddr
import pytest
from unittest import mock

from steelscript.steelhead.features.networking.v8_5.model import \
    NetworkingModel


SHOW_INTERFACES_BRIEF_OUTPUT = """
Interface aux state
   Up:                 yes
   Interface type:     ethernet
   IP address:         10.3.2.54
   Netmask:            255.255.248.0
   IPv6 link-local address: fe80::20e:b6ff:fe5a:ca99/64
   Speed:              100Mb/s (auto)
   Duplex:             full (auto)
   MTU:                1500
   HW address:         00:0E:B6:5A:CA:99
   Link:               yes
   Counters cleared date:  2014/11/19 16:31:12

Interface inpath0_0 state
   Up:                 yes
   Interface type:     ethernet
   IP address:         10.11.100.4
   Netmask:            255.255.255.0
   IPv6 link-local address: fe80::5054:ff:fe10:3fe9/64
   MTU:                1500
   HW address:         52:54:00:10:3F:E9
   Traffic status:     Normal
   HW blockable:       no
   Counters cleared date:  2014/01/31 14:28:28
"""
SHOW_INTERFACES_BRIEF_PARSED = [
    {'name': 'aux',
     'up': True,
     'interface type': 'ethernet',
     'ip address': ipaddress.ip_interface('10.3.2.54/21'),
     'ipv6 link-local address':
        ipaddress.ip_interface('fe80::20e:b6ff:fe5a:ca99/64'),
     'speed': '100Mb/s (auto)',
     'duplex': 'full (auto)',
     'mtu': 1500,
     'hw address': netaddr.EUI('00:0E:B6:5A:CA:99'),
     'link': True,
     'counters cleared date': datetime.datetime(2014, 11, 19, 16, 31, 12)},
    {'name': 'inpath0_0',
     'up': True,
     'interface type': 'ethernet',
     'ip address': ipaddress.ip_interface('10.11.100.4/24'),
     'ipv6 link-local address':
        ipaddress.ip_interface('fe80::5054:ff:fe10:3fe9/64'),
     'mtu': 1500,
     'hw address': netaddr.EUI('52:54:00:10:3F:E9'),
     'traffic status': 'Normal',
     'hw blockable': False,
     'counters cleared date': datetime.datetime(2014, 1, 31, 14, 28, 28)},
]

SHOW_INTERFACE_OUTPUT = """
Interface primary state
   Up:                 yes
   Interface type:     ethernet
   IP address:         10.11.140.3
   Netmask:            255.255.0.0
   IPv6 link-local address: fe80::20e:b6ff:fe03:6b18/64
   Speed:              1000Mb/s (auto)
   Duplex:             full (auto)
   MTU:                1500
   HW address:         00:0E:B6:03:6B:18
   Link:               yes
   Counters cleared date:  2014/05/07 17:27:19

   RX bytes:           2298366
   RX packets:         27027
   RX mcast packets:   0
   RX discards:        0
   RX errors:          0
   RX overruns:        0
   RX frame:           0

   TX bytes:           516
   TX packets:         6
   TX discards:        0
   TX errors:          0
   TX overruns:        0
   TX carrier:         0
   TX collisions:      0
"""
SHOW_INTERFACE_PARSED = [{
    'name': 'primary',
    'up': True,
    'interface type': 'ethernet',
    'ip address': ipaddress.ip_interface('10.11.140.3/16'),
    'ipv6 link-local address':
        ipaddress.ip_interface('fe80::20e:b6ff:fe03:6b18/64'),
    'speed': '1000Mb/s (auto)',
    'duplex': 'full (auto)',
    'mtu': 1500,
    'hw address': netaddr.EUI('00:0E:B6:03:6B:18'),
    'link': True,
    'counters cleared date': datetime.datetime(2014, 5, 7, 17, 27, 19),
    'rx bytes': 2298366,
    'rx packets': 27027,
    'rx mcast packets': 0,
    'rx discards': 0,
    'rx errors': 0,
    'rx overruns': 0,
    'rx frame': 0,
    'tx bytes': 516,
    'tx packets': 6,
    'tx discards': 0,
    'tx errors': 0,
    'tx overruns': 0,
    'tx carrier': 0,
    'tx collisions': 0,
}]

SHOW_INTERFACE_CONFIGURED = """
Interface aux configuration
   Enabled:            yes
   DHCP:               no
   Dynamic DNS DHCP:   no
   DHCPv6:             no
   Dynamic DNS DHCPv6: no
   IP address:         10.3.2.54
   Netmask:            255.255.248.0
   IPv6 address:
   Speed:              auto
   Duplex:             auto
   MTU:                1500
   Counters cleared date:  2014/11/19 16:31:12
"""
SHOW_INTERFACE_CONFIGURED_PARSED = [{
    'name': 'aux',
    'enabled': True,
    'dhcp': False,
    'dynamic dns dhcp': False,
    'dhcpv6': False,
    'dynamic dns dhcpv6': False,
    'ip address': ipaddress.ip_interface('10.3.2.54/21'),
    'ipv6 address': None,
    'speed': 'auto',
    'duplex': 'auto',
    'mtu': 1500,
    'counters cleared date': datetime.datetime(2014, 11, 19, 16, 31, 12),
}]


@pytest.yield_fixture
def mock_cli():
    with mock.patch('steelscript.common.interaction.model.Model.cli') as cli:
        yield cli


@pytest.mark.parametrize(('output', 'parsed', 'brief'), [
    (SHOW_INTERFACE_OUTPUT, SHOW_INTERFACE_PARSED, True),
    (SHOW_INTERFACES_BRIEF_OUTPUT, SHOW_INTERFACES_BRIEF_PARSED, False),
])
def test_show_interfaces(mock_cli, output, parsed, brief):
    model = NetworkingModel(mock.Mock(), cli=mock_cli)
    mock_cli.exec_command.return_value = output
    return_dict = model.show_interfaces(brief=brief)
    assert return_dict == parsed


def test_show_interfaces_configured(mock_cli):
    model = NetworkingModel(mock.Mock(), cli=mock_cli)
    mock_cli.exec_command.return_value = SHOW_INTERFACE_CONFIGURED
    return_dict = model.show_interfaces_configured()
    assert return_dict == SHOW_INTERFACE_CONFIGURED_PARSED
