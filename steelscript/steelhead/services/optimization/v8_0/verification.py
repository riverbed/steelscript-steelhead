###########TODO############



# -*- coding: utf-8 -*-
#
# Copyright 2014 Riverbed Technology, Inc.
# All Rights Reserved. Confidential.

from __future__ import (unicode_literals, print_function, division,
                        absolute_import)

from pq_fwk import uidelegation
from pq_fwk.verification import verification, Verification
from pq_runtime import polling
from pq_runtime.exceptions import VerificationError


@verification
class Kauai(Verification):
    """
    Kauai Optimization Verifications for SteelHead product
    """


class CLI(uidelegation.CLI):
    """
    Kauai Optimization CLI Delegatee
    """

    def wait_for_intercept_ready(self, max_retries=20, min_interval=3):
        """
        Wait for the Intercept module to be ready.

        :param max_retries: Number of retries to check if sport
                            intercept module is ready. Defaults to 20.
        :type max_retries: int
        :param min_interval: Min seconds between polls.
                             Defaults to 3 seconds.
        :type min_interval: int

        :raises VerificationError: If intercept module isn't ready in time.
        """
        result = any(x['intercept module ready'] for x in polling.do_poll(
            self.model.show_sport_intercept,
            max_poll_retries=max_retries,
            min_poll_interval=min_interval))
        if not result:
            raise VerificationError(
                description="Intercept module was not ready by the end of the "
                            "polling period",
                expected=True, actual=False)


class REST(uidelegation.REST):
    """
    Kauai Optimization REST Delegatee
    Not implemented since Kauai doesn't have any RESTful features
    """
    pass
