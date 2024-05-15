# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

import logging
from typing import Any, Dict
from unittest import main

from mlcvzoo_base.api.data.box import Box
from mlcvzoo_base.api.data.class_identifier import ClassIdentifier
from mlcvzoo_base.api.data.segmentation import Segmentation
from mlcvzoo_base.tests.unit_tests.test_template import TestTemplate

logger = logging.getLogger(__name__)


class TestAPISegmentation(TestTemplate):
    @staticmethod
    def __create_dummy_segmentation(with_box: bool = True) -> Segmentation:
        if with_box:
            box = Box(xmin=0, ymin=0, xmax=100, ymax=100)
        else:
            box = None
        return Segmentation(
            polygon=[(0, 0), (100, 0), (100, 100), (0, 100)],
            box=box,
            class_identifier=ClassIdentifier(class_id=0, class_name="test"),
            model_class_identifier=ClassIdentifier(class_id=0, class_name="test"),
            score=1,
            difficult=False,
            occluded=False,
            background=False,
            content="",
        )

    def test_to_dict(self) -> None:
        dummy_segmentation: Segmentation = self.__create_dummy_segmentation()
        expected_dict: Dict = {
            "box": {"xmax": 100, "xmin": 0, "ymax": 100, "ymin": 0},
            "class_identifier": {"class_id": 0, "class_name": "test"},
            "content": "",
            "difficult": False,
            "model_class_identifier": {"class_id": 0, "class_name": "test"},
            "occluded": False,
            "background": False,
            "polygon": [(0, 0), (100, 0), (100, 100), (0, 100)],
            "score": 1,
        }

        assert dummy_segmentation.to_dict() == expected_dict

    def test_to_dict_without_box(self) -> None:
        dummy_segmentation: Segmentation = self.__create_dummy_segmentation(with_box=False)
        expected_dict: Dict = {
            "box": None,
            "class_identifier": {"class_id": 0, "class_name": "test"},
            "content": "",
            "difficult": False,
            "model_class_identifier": {"class_id": 0, "class_name": "test"},
            "occluded": False,
            "background": False,
            "polygon": [(0, 0), (100, 0), (100, 100), (0, 100)],
            "score": 1,
        }

        assert dummy_segmentation.to_dict() == expected_dict

    def test_to_dict_raw(self) -> None:
        dummy_segmentation: Segmentation = self.__create_dummy_segmentation()
        expected_dict: Dict = {
            "box": Box(xmin=0, ymin=0, xmax=100, ymax=100),
            "class_identifier": dummy_segmentation.class_identifier,
            "content": "",
            "difficult": False,
            "model_class_identifier": dummy_segmentation.model_class_identifier,
            "occluded": False,
            "background": False,
            "polygon": [(0, 0), (100, 0), (100, 100), (0, 100)],
            "score": 1,
        }

        assert dummy_segmentation.to_dict(raw_type=True) == expected_dict

    def test_to_dict_reduced(self) -> None:
        dummy_segmentation: Segmentation = self.__create_dummy_segmentation()
        expected_dict: Dict = {
            "box": {"xmax": 100, "xmin": 0, "ymax": 100, "ymin": 0},
            "class_id": 0,
            "class_name": "test",
            "model_class_id": 0,
            "model_class_name": "test",
            "polygon": [(0, 0), (100, 0), (100, 100), (0, 100)],
            "score": 1,
        }

        assert dummy_segmentation.to_dict(reduced=True) == expected_dict

    def test_to_dict_raw_reduced(self) -> None:
        dummy_segmentation: Segmentation = self.__create_dummy_segmentation()
        expected_dict: Dict = {
            "box": Box(xmin=0, ymin=0, xmax=100, ymax=100),
            "class_id": 0,
            "class_name": "test",
            "model_class_id": 0,
            "model_class_name": "test",
            "polygon": [(0, 0), (100, 0), (100, 100), (0, 100)],
            "score": 1,
        }

        assert dummy_segmentation.to_dict(raw_type=True, reduced=True) == expected_dict

    def test_from_dict(self) -> None:
        segmentation_dict: Dict = {
            "box": {"xmax": 100, "xmin": 0, "ymax": 100, "ymin": 0},
            "class_identifier": {"class_id": 0, "class_name": "test"},
            "content": "",
            "difficult": False,
            "model_class_identifier": {"class_id": 0, "class_name": "test"},
            "occluded": False,
            "background": False,
            "polygon": [(0, 0), (100, 0), (100, 100), (0, 100)],
            "score": 1,
        }
        segmentation: Segmentation = Segmentation.from_dict(segmentation_dict)

        assert segmentation == self.__create_dummy_segmentation()

    def test_from_dict_reduced(self) -> None:
        segmentation_dict: Dict = {
            "box": {"xmax": 100, "xmin": 0, "ymax": 100, "ymin": 0},
            "class_id": 0,
            "class_name": "test",
            "model_class_id": 0,
            "model_class_name": "test",
            "polygon": [(0, 0), (100, 0), (100, 100), (0, 100)],
            "score": 1,
        }
        segmentation: Segmentation = Segmentation.from_dict(segmentation_dict, reduced=True)

        assert segmentation == self.__create_dummy_segmentation()

    def test_to_json(self) -> None:
        dummy_segmentation: Segmentation = self.__create_dummy_segmentation()
        segmentation_json: Any = dummy_segmentation.to_json()
        expected_json = {
            "box": {"xmax": 100, "xmin": 0, "ymax": 100, "ymin": 0},
            "class_identifier": {"class_id": 0, "class_name": "test"},
            "content": "",
            "difficult": False,
            "model_class_identifier": {"class_id": 0, "class_name": "test"},
            "occluded": False,
            "background": False,
            "polygon": [(0, 0), (100, 0), (100, 100), (0, 100)],
            "score": 1,
        }
        print(type(segmentation_json))
        assert segmentation_json == expected_json


if __name__ == "__main__":
    main()
