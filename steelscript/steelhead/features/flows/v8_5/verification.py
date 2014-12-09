# -*- coding: utf-8 -*-
#
# Copyright 2014 Riverbed Technology, Inc.
# All Rights Reserved. Confidential.

from __future__ import (unicode_literals, print_function, division,
                        absolute_import)

from pq_fwk.verification import verification, Verification
from pq_fwk import uidelegation


@verification
class Kauai(Verification):
    """
    Kauai Reporting Verifications for SteelHead product
    """


class CLI(uidelegation.CLI):
    """
    Kauai Reporting CLI Delegatee
    """
    pass
