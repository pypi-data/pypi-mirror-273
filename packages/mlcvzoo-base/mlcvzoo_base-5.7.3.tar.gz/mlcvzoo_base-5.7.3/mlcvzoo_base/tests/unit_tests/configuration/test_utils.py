# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

import logging
from argparse import ArgumentTypeError

from mlcvzoo_base.configuration.utils import str2bool
from mlcvzoo_base.tests.unit_tests.test_template import TestTemplate

logger = logging.getLogger(__name__)


# TODO: add test that surrounding box is written to csv files


class TestUtils(TestTemplate):
    def test_str_to_bool(self):
        # check that actual boolean values are accepted
        assert str2bool(True) is True
        assert str2bool(False) is False

        # check spelling variants of 'yes' are accepted
        assert str2bool("yes") is True
        assert str2bool("yeS") is True
        assert str2bool("yEs") is True
        assert str2bool("yES") is True
        assert str2bool("Yes") is True
        assert str2bool("YeS") is True
        assert str2bool("YEs") is True
        assert str2bool("YES") is True

        # check spelling variants of 'no' are accepted
        assert str2bool("no") is False
        assert str2bool("nO") is False
        assert str2bool("No") is False
        assert str2bool("NO") is False

        # check for single letter 't' for 'true'
        assert str2bool("t") is True
        assert str2bool("T") is True
        # check for single letter 'f' for 'false
        assert str2bool("f") is False
        assert str2bool("F") is False

        # check for single letter 'y' for 'yes'
        assert str2bool("y") is True
        assert str2bool("Y") is True
        # check for single letter 'n' for 'no'
        assert str2bool("n") is False
        assert str2bool("N") is False

        # check number representation of true
        assert str2bool("1") is True
        assert str2bool("1.0") is True

        # check number representations of false
        assert str2bool("0") is False
        assert str2bool("0.0") is False

        self.assertRaises(ArgumentTypeError, str2bool, "test")
