# Copyright 2016 Red Hat, Inc.
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
Test management of KeyboardInterrupt in stratisd.
"""

# isort: LOCAL
import stratis_cli

from .._misc import SimTestCase


class KeyboardInterruptTestCase(SimTestCase):
    """
    Test behavior of stratis on KeyboardInterrupt.
    """

    def test_catch_keyboard_exception(self):
        """
        Verify that the KeyboardInterrupt is propagated by the run() method.
        ./bin/stratis contains a try block at the outermost level which
        then catches the KeyboardInterrupt and exits with an error message.
        The KeyboardInterrupt is most likely raised in the dbus-python
        method which is actually communicating on the D-Bus, but it is
        fairly difficult to get at that method. Instead settle for getting
        at the calling method generated by dbus-python-client-gen.
        """

        def raise_keyboard_interrupt(_):
            """
            Just raise the interrupt.
            """
            raise KeyboardInterrupt()

        from stratis_cli._actions import _data

        # pylint: disable=protected-access
        stratis_cli._actions._data.Manager.Properties.Version.Get = (
            raise_keyboard_interrupt
        )

        with self.assertRaises(KeyboardInterrupt):
            stratis_cli.run()(["daemon", "version"])
