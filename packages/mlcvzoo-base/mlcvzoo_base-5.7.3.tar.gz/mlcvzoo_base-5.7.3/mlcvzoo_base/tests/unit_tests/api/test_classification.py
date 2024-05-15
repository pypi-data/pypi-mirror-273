# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

import logging
from typing import Dict
from unittest import main

from mlcvzoo_base.api.data.class_identifier import ClassIdentifier
from mlcvzoo_base.api.data.classification import Classification
from mlcvzoo_base.tests.unit_tests.test_template import TestTemplate

logger = logging.getLogger(__name__)


class TestAPIClassification(TestTemplate):
    @staticmethod
    def __create_dummy_classification__() -> Classification:
        return Classification(
            class_identifier=ClassIdentifier(class_id=0, class_name="test"),
            score=1,
            model_class_identifier=ClassIdentifier(class_id=0, class_name="test"),
        )

    def test_to_dict(self) -> None:
        dummy_classification: Classification = self.__create_dummy_classification__()
        expected_dict: Dict = {
            "class_identifier": {"class_id": 0, "class_name": "test"},
            "model_class_identifier": {"class_id": 0, "class_name": "test"},
            "score": 1,
        }

        assert dummy_classification.to_dict() == expected_dict

    def test_to_dict_raw(self) -> None:
        dummy_classification: Classification = self.__create_dummy_classification__()
        expected_dict: Dict = {
            "class_identifier": dummy_classification.class_identifier,
            "model_class_identifier": dummy_classification.model_class_identifier,
            "score": 1,
        }

        assert dummy_classification.to_dict(raw_type=True) == expected_dict

    def test_to_dict_reduced(self) -> None:
        dummy_classification: Classification = self.__create_dummy_classification__()
        expected_dict: Dict = {
            "class_id": 0,
            "class_name": "test",
            "model_class_id": 0,
            "model_class_name": "test",
            "score": 1,
        }

        assert dummy_classification.to_dict(reduced=True) == expected_dict

    def test_to_dict_raw_reduced(self) -> None:
        dummy_classification: Classification = self.__create_dummy_classification__()

        expected_dict: Dict = {
            "class_id": 0,
            "class_name": "test",
            "model_class_id": 0,
            "model_class_name": "test",
            "score": 1,
        }

        assert dummy_classification.to_dict(raw_type=True, reduced=True) == expected_dict

    def test_from_dict(self) -> None:
        classification_dict: Dict = {
            "class_identifier": {"class_id": 0, "class_name": "test"},
            "model_class_identifier": {"class_id": 0, "class_name": "test"},
            "score": 1,
        }
        classification: Classification = Classification.from_dict(classification_dict)

        assert classification == self.__create_dummy_classification__()

    def test_from_dict_reduced(self) -> None:
        classification_dict: Dict = {
            "class_id": 0,
            "class_name": "test",
            "model_class_id": 0,
            "model_class_name": "test",
            "score": 1,
        }
        classification: Classification = Classification.from_dict(
            classification_dict, reduced=True
        )

        assert classification == self.__create_dummy_classification__()


if __name__ == "__main__":
    main()
