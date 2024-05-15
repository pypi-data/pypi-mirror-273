# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3
import logging
import os
from typing import List
from unittest import main

import cv2

from mlcvzoo_base.api.data.box import Box
from mlcvzoo_base.api.data.class_identifier import ClassIdentifier
from mlcvzoo_base.api.data.segmentation import Segmentation
from mlcvzoo_base.models.model_registry import ModelRegistry
from mlcvzoo_base.models.read_from_file.model import ReadFromFileSegmentationModel
from mlcvzoo_base.tests.unit_tests.test_template import TestTemplate

logger = logging.getLogger(__name__)


class TestReadFromFileSegmentationModel(TestTemplate):
    @staticmethod
    def __is_correct_segmentation(
        ground_truth_segmentation: Segmentation,
        predicted_segmentation: Segmentation,
    ) -> bool:
        polygon_equal: bool = True

        for polygon_point, other_polygon_point in zip(
            ground_truth_segmentation.polygon, predicted_segmentation.polygon
        ):
            point_equal = (
                abs(polygon_point[0] - other_polygon_point[0]) < 1e9
                and abs(polygon_point[1] - other_polygon_point[1]) < 1e9
            )

            if point_equal:
                polygon_equal = polygon_equal and point_equal
            else:
                polygon_equal = False
                break

        is_correct: bool = (
            ground_truth_segmentation.class_id == predicted_segmentation.class_id
            and ground_truth_segmentation.class_name == predicted_segmentation.class_name
            and ground_truth_segmentation.box == predicted_segmentation.box
            and polygon_equal
        )

        return is_correct

    @staticmethod
    def __check_coco_segmentations(
        segmentations: List[Segmentation],
    ) -> None:
        expected_segmentation_0 = Segmentation(
            box=Box(xmin=139, ymin=267, xmax=287, ymax=355),
            class_identifier=ClassIdentifier(
                class_id=0,
                class_name="person",
            ),
            score=0.0,
            polygon=[(139.3, 267.8), (287.3, 273.8), (259.7, 355.3), (172.2, 354.8)],
            difficult=False,
            occluded=False,
            background=False,
            content="",
        )

        expected_segmentation_1 = Segmentation(
            box=Box(xmin=309, ymin=348, xmax=318, ymax=353),
            class_identifier=ClassIdentifier(
                class_id=3,
                class_name="lp",
            ),
            score=0.0,
            polygon=[(309.8, 353.2), (309.8, 348.4), (318.5, 348.1), (318.6, 353.3)],
            difficult=False,
            occluded=False,
            background=False,
            content="test_LP_42",
        )

        expected_segmentation_2 = Segmentation(
            box=Box(xmin=309, ymin=348, xmax=318, ymax=353),
            class_identifier=ClassIdentifier(
                class_id=3,
                class_name="lp",
            ),
            score=0.0,
            polygon=[(309.8, 353.2), (309.8, 348.4), (318.5, 348.1), (318.6, 353.3)],
            difficult=True,
            occluded=False,
            background=False,
            content="test_LP_42",
        )

        expected_segmentation_3 = Segmentation(
            box=Box(xmin=309, ymin=348, xmax=318, ymax=353),
            class_identifier=ClassIdentifier(
                class_id=3,
                class_name="lp",
            ),
            score=0.0,
            polygon=[(309.8, 353.2), (309.8, 348.4), (318.5, 348.1), (318.6, 353.3)],
            difficult=False,
            occluded=True,
            background=False,
            content="test_LP_42",
        )

        expected_segmentations = [
            expected_segmentation_0,
            expected_segmentation_1,
            expected_segmentation_2,
            expected_segmentation_3,
        ]

        for i in range(4):
            is_correct = TestReadFromFileSegmentationModel.__is_correct_segmentation(
                ground_truth_segmentation=expected_segmentations[i],
                predicted_segmentation=segmentations[i],
            )

            if not is_correct:
                logger.error(
                    "Found wrong segmentation: \n"
                    f"  Expected:  {expected_segmentations[i]}\n"
                    f"  Predicted: {segmentations[i]}\n"
                )

                logger.error("All segmentations: \n" f"{segmentations}")

                raise ValueError("Output is not valid!")

    def test_read_from_file_segmentation_registry(self) -> None:
        model_registry = ModelRegistry()

        assert (
            model_registry.model_registry["read_from_file_segmentation"]
            == ReadFromFileSegmentationModel
        )

    def test_read_from_file_segmentation_model(self) -> None:
        read_from_file_model = ReadFromFileSegmentationModel(
            from_yaml=os.path.join(
                self.project_root,
                "test_data/test_ReadFromFileObjectDetectionModel/",
                "read-from-file_coco_test.yaml",
            ),
            string_replacement_map=self.string_replacement_map,
        )

        test_image_path = os.path.join(
            self.project_root,
            "test_data/images/dummy_task/cars.jpg",
        )

        _, segmentations = read_from_file_model.predict(data_item=test_image_path)

        logger.info(segmentations)

        self.__check_coco_segmentations(segmentations)

    def test_read_from_file_segmentation_model_image_based(self) -> None:
        read_from_file_model = ReadFromFileSegmentationModel(
            from_yaml=os.path.join(
                self.project_root,
                "test_data/test_ReadFromFileObjectDetectionModel/",
                "read-from-file_coco_test.yaml",
            ),
            string_replacement_map=self.string_replacement_map,
        )

        test_image_path = os.path.join(
            self.project_root,
            "test_data/images/dummy_task/cars.jpg",
        )

        test_image = cv2.imread(test_image_path)

        _, segmentations = read_from_file_model.predict(data_item=test_image)

        self.__check_coco_segmentations(segmentations)

    def test_read_from_file_no_data(self):
        read_from_file_model = ReadFromFileSegmentationModel(
            from_yaml=os.path.join(
                self.project_root,
                "test_data/test_ReadFromFileObjectDetectionModel/",
                "read-from-file_coco_test.yaml",
            ),
            string_replacement_map=self.string_replacement_map,
        )

        with self.assertRaises(ValueError) as value_error:
            read_from_file_model.predict("")
            assert str(value_error) == "data_item='' not in lookup dict of the ReadFromFileModel"


if __name__ == "__main__":
    main()
