# Copyright 2020 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Test 'stratis report'.
"""

# isort: STDLIB
import os
import unittest

# isort: LOCAL
from stratis_cli import StratisCliErrorCodes
from stratis_cli._stratisd_constants import ReportKey

from .._misc import TEST_RUNNER, SimTestCase

_ERROR = StratisCliErrorCodes.ERROR


class ReportTestCase(SimTestCase):
    """
    Test getting the stopped pool, engine state, and a nonexistent report
    """

    _MENU = ["--propagate", "report"]

    @unittest.skipIf(
        os.getenv("STRATIS_SKIP_UNSTABLE_TEST") is not None,
        "This test relies on the Report interface's GetReport method which "
        "does not guarantee the stability, between minor versions of stratisd, "
        "of the report key arguments that it supports.",
    )
    def test_report(self):
        """
        Test getting stopped pool report.
        """
        TEST_RUNNER(self._MENU + [str(ReportKey.STOPPED_POOLS)])

    def test_report_no_name(self):
        """
        Test getting engine state report when no name specified.
        """
        TEST_RUNNER(self._MENU)

    def test_engine_state_report(self):
        """
        Test getting engine state report.
        """
        TEST_RUNNER(self._MENU + [str(ReportKey.ENGINE_STATE)])

    def test_managed_objects_report(self):
        """
        Test getting managed_objects report.
        """
        TEST_RUNNER(self._MENU + [str(ReportKey.MANAGED_OBJECTS)])
