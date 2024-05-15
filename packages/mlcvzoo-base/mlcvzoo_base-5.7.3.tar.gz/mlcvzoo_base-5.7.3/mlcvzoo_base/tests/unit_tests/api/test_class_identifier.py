# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

import logging
from typing import Any, Dict
from unittest import main

from mlcvzoo_base.api.data.class_identifier import ClassIdentifier
from mlcvzoo_base.tests.unit_tests.test_template import TestTemplate

logger = logging.getLogger(__name__)


class TestAPIClassIdentifier(TestTemplate):
    def test_to_dict(self) -> None:
        dummy_class_identifier: ClassIdentifier = ClassIdentifier(class_id=0, class_name="test")
        expected_dict: Dict = {"class_id": 0, "class_name": "test"}

        assert dummy_class_identifier.to_dict() == expected_dict

    def test_to_json(self) -> None:
        dummy_class_identifier: ClassIdentifier = ClassIdentifier(class_id=0, class_name="test")
        expected_json: Any = {"class_id": 0, "class_name": "test"}

        assert dummy_class_identifier.to_json() == expected_json


if __name__ == "__main__":
    main()
