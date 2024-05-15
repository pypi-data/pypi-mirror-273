# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

import logging
from typing import Any, Dict
from unittest import main

from mlcvzoo_base.api.data.bounding_box import BoundingBox
from mlcvzoo_base.api.data.box import Box
from mlcvzoo_base.api.data.class_identifier import ClassIdentifier
from mlcvzoo_base.tests.unit_tests.test_template import TestTemplate

logger = logging.getLogger(__name__)


class TestAPIBoundingBox(TestTemplate):
    @staticmethod
    def __create_dummy_bbox__() -> BoundingBox:
        return BoundingBox(
            box=Box(xmin=0, ymin=0, xmax=100, ymax=100),
            class_identifier=ClassIdentifier(
                class_id=0,
                class_name="test",
            ),
            score=1,
            difficult=False,
            occluded=False,
            background=False,
            content="",
            model_class_identifier=ClassIdentifier(
                class_id=0,
                class_name="test",
            ),
        )

    def test_to_dict(self) -> None:
        dummy_bounding_box: BoundingBox = self.__create_dummy_bbox__()
        bounding_box_dict: Dict = dummy_bounding_box.to_dict(reduced=False)
        expected_dict: Dict = {
            "box": {"xmin": 0, "ymin": 0, "xmax": 100, "ymax": 100},
            "class_identifier": {"class_id": 0, "class_name": "test"},
            "model_class_identifier": {"class_id": 0, "class_name": "test"},
            "score": 1,
            "difficult": False,
            "occluded": False,
            "background": False,
            "content": "",
        }

        assert bounding_box_dict == expected_dict

    def test_to_dict_raw(self) -> None:
        dummy_bounding_box: BoundingBox = self.__create_dummy_bbox__()
        bounding_box_dict: Dict = dummy_bounding_box.to_dict(raw_type=True, reduced=False)
        expected_dict: Dict = {
            "box": Box(xmin=0, ymin=0, xmax=100, ymax=100),
            "class_identifier": dummy_bounding_box.class_identifier,
            "model_class_identifier": dummy_bounding_box.model_class_identifier,
            "score": 1,
            "difficult": False,
            "occluded": False,
            "background": False,
            "content": "",
        }

        assert bounding_box_dict == expected_dict

    def test_to_dict_reduced(self) -> None:
        dummy_bounding_box: BoundingBox = self.__create_dummy_bbox__()
        bounding_box_dict: Dict = dummy_bounding_box.to_dict(reduced=True)
        expected_dict: Dict = {
            "box": {"xmin": 0, "ymin": 0, "xmax": 100, "ymax": 100},
            "class_id": 0,
            "class_name": "test",
            "model_class_id": 0,
            "model_class_name": "test",
            "score": 1,
        }

        assert bounding_box_dict == expected_dict

    def test_to_dict_raw_reduced(self) -> None:
        dummy_bounding_box: BoundingBox = self.__create_dummy_bbox__()
        bounding_box_dict: Dict = dummy_bounding_box.to_dict(raw_type=True, reduced=True)
        expected_dict: Dict = {
            "box": Box(xmin=0, ymin=0, xmax=100, ymax=100),
            "class_id": 0,
            "class_name": "test",
            "model_class_id": 0,
            "model_class_name": "test",
            "score": 1,
        }

        assert bounding_box_dict == expected_dict

    def test_from_dict(self) -> None:
        bounding_box_dict: Dict = {
            "box": {"xmin": 0, "ymin": 0, "xmax": 100, "ymax": 100},
            "class_identifier": {"class_id": 0, "class_name": "test"},
            "model_class_identifier": {"class_id": 0, "class_name": "test"},
            "score": 1,
            "difficult": False,
            "occluded": False,
            "background": False,
            "content": "",
        }

        bounding_box: BoundingBox = BoundingBox.from_dict(bounding_box_dict)

        expected_bounding_box: BoundingBox = self.__create_dummy_bbox__()

        assert bounding_box == expected_bounding_box

    def test_from_dict_reduced(self) -> None:
        bounding_box_dict: Dict = {
            "box": {"xmin": 0, "ymin": 0, "xmax": 100, "ymax": 100},
            "class_id": 0,
            "class_name": "test",
            "model_class_id": 0,
            "model_class_name": "test",
            "score": 1,
        }

        bounding_box: BoundingBox = BoundingBox.from_dict(bounding_box_dict, reduced=True)

        expected_bounding_box: BoundingBox = self.__create_dummy_bbox__()

        assert bounding_box == expected_bounding_box

    def test_to_json(self) -> None:
        dummy_bounding_box: BoundingBox = self.__create_dummy_bbox__()
        bounding_box_json: Any = dummy_bounding_box.to_json()
        expected_json: Dict = {
            "box": {"xmin": 0, "ymin": 0, "xmax": 100, "ymax": 100},
            "class_identifier": {"class_id": 0, "class_name": "test"},
            "model_class_identifier": {"class_id": 0, "class_name": "test"},
            "score": 1,
            "difficult": False,
            "occluded": False,
            "background": False,
            "content": "",
        }

        assert bounding_box_json == expected_json


if __name__ == "__main__":
    main()
