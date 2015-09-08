# Copyright (c) 2015 Riverbed Technology, Inc.
#
# This software is licensed under the terms and conditions of the MIT License
# accompanying the software ("License").  This software is distributed "AS IS"
# as set forth in the License.

"""
This module contains the SteelHead class - the main interface to a SteelHead
appliance.
"""

from __future__ import (absolute_import, unicode_literals, print_function,
                        division)

from steelscript.cmdline.cli import rvbd_cli


class CLIAuth(object):
    """
    This class is used for username/password based authentication for
    command-line access.
    """

    def __init__(self, username, password):
        """
        Authentication method using `username` and `password`.
        """
        self.username = username
        self.password = password

    def __repr__(self):
        return '<CLIAuth username: %s password: *****>' % self.username


class SteelHead(object):
    """
    The SteelHead class if the main interface to interact with a SteelHead
    appliance.
    """

    def __init__(self, host, auth=None):
        """
        Establishes a connection to a SteelHead appliance.

        :param str host:  Name or IP address of the SteelHead.
        :param auth:  Defines the credentials to use to access the SteelHead.
            It should be an instance of
            :py:class:`CLIAuth<steelscript.steelhead.core.steelhead.CLIAuth>`
        """
        self.host = host

        if not isinstance(auth, CLIAuth):
            raise TypeError("'auth' must be a CLIAuth object")
        self.auth = auth

        self._cli = None

    @property
    def cli(self):
        """
        Grabs a cached CLI object, opening a new one if none exists.
        """
        if self._cli is None:
            # TODO: Use CLICache
            self._cli = rvbd_cli.RVBD_CLI(hostname=self.host,
                                          username=self.auth.username,
                                          password=self.auth.password)
            self._cli.start()
        return self._cli

    @property
    def version(self):
        raise NotImplementedError()
