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

from mlcvzoo_base.api.data.bounding_box import BoundingBox
from mlcvzoo_base.api.data.box import Box
from mlcvzoo_base.api.data.class_identifier import ClassIdentifier
from mlcvzoo_base.models.model_registry import ModelRegistry
from mlcvzoo_base.models.read_from_file.model import ReadFromFileObjectDetectionModel
from mlcvzoo_base.tests.unit_tests.test_template import TestTemplate

logger = logging.getLogger(__name__)


class TestReadFromFileObjectDetectionModel(TestTemplate):
    @staticmethod
    def __is_correct_bounding_box(
        ground_truth_bounding_box: BoundingBox,
        predicted_bounding_box: BoundingBox,
    ) -> bool:
        is_correct: bool = (
            ground_truth_bounding_box.box == predicted_bounding_box.box
            and ground_truth_bounding_box.class_id == predicted_bounding_box.class_id
            and ground_truth_bounding_box.class_name == predicted_bounding_box.class_name
        )

        return is_correct

    @staticmethod
    def __check_coco_bounding_boxes(bounding_boxes: List[BoundingBox]) -> None:
        class_identifier_0 = ClassIdentifier(
            class_id=2,
            class_name="car",
        )
        expected_bounding_box_0 = BoundingBox(
            box=Box(xmin=16, ymin=313, xmax=80, ymax=364),
            class_identifier=class_identifier_0,
            model_class_identifier=class_identifier_0,
            score=0.0,
            difficult=False,
            occluded=False,
            content="",
        )

        class_identifier_1 = ClassIdentifier(
            class_id=3,
            class_name="lp",
        )
        expected_bounding_box_1 = BoundingBox(
            box=Box(xmin=0, ymin=348, xmax=8, ymax=353),
            class_identifier=class_identifier_1,
            model_class_identifier=class_identifier_1,
            score=0.0,
            difficult=False,
            occluded=True,
            content="test_LP_42",
        )

        is_correct_0 = TestReadFromFileObjectDetectionModel.__is_correct_bounding_box(
            ground_truth_bounding_box=expected_bounding_box_0,
            predicted_bounding_box=bounding_boxes[0],
        )

        if not is_correct_0:
            logger.error(
                "Found wrong bounding_box: \n"
                f"  Expected:  {expected_bounding_box_0}\n"
                f"  Predicted: {bounding_boxes[0]}\n"
            )

            logger.error("All bounding_boxes: \n" f"{bounding_boxes}")

            raise ValueError("Output is not valid!")

        is_correct_1 = TestReadFromFileObjectDetectionModel.__is_correct_bounding_box(
            ground_truth_bounding_box=expected_bounding_box_1,
            predicted_bounding_box=bounding_boxes[1],
        )

        if not is_correct_1:
            logger.error(
                "Found wrong bounding_box: \n"
                f"  Expected:  {expected_bounding_box_1}\n"
                f"  Predicted: {bounding_boxes[1]}\n"
            )

            logger.error("All bounding_boxes: \n" f"{bounding_boxes}")

            raise ValueError("Output is not valid!")

    @staticmethod
    def __check_pascal_voc_bounding_boxes(
        bounding_boxes: List[BoundingBox],
    ) -> None:
        expected_bounding_box_0 = BoundingBox(
            box=Box(xmin=10, ymin=10, xmax=390, ymax=499),
            class_identifier=ClassIdentifier(
                class_id=2,
                class_name="car",
            ),
            score=0.0,
            difficult=False,
            occluded=False,
            content="",
        )

        expected_bounding_box_1 = BoundingBox(
            box=Box(xmin=67, ymin=58, xmax=305, ymax=370),
            class_identifier=ClassIdentifier(
                class_id=2,
                class_name="car",
            ),
            score=0.0,
            difficult=False,
            occluded=False,
            content="",
        )

        expected_bounding_box_2 = BoundingBox(
            box=Box(xmin=50, ymin=50, xmax=295, ymax=360),
            class_identifier=ClassIdentifier(
                class_id=2,
                class_name="car",
            ),
            score=0.0,
            difficult=False,
            occluded=False,
            content="",
        )

        is_correct_0 = TestReadFromFileObjectDetectionModel.__is_correct_bounding_box(
            ground_truth_bounding_box=expected_bounding_box_0,
            predicted_bounding_box=bounding_boxes[0],
        )

        if not is_correct_0:
            logger.error(
                "Found wrong bounding_box: \n"
                f"  Expected:  {expected_bounding_box_0}\n"
                f"  Predicted: {bounding_boxes[0]}\n"
            )

            logger.error("All bounding_boxes: \n" f"{bounding_boxes}")

            raise ValueError("Output is not valid!")

        is_correct_1 = TestReadFromFileObjectDetectionModel.__is_correct_bounding_box(
            ground_truth_bounding_box=expected_bounding_box_1,
            predicted_bounding_box=bounding_boxes[1],
        )

        if not is_correct_1:
            logger.error(
                "Found wrong bounding_box: \n"
                f"  Expected:  {expected_bounding_box_1}\n"
                f"  Predicted: {bounding_boxes[1]}\n"
            )

            logger.error("All bounding_boxes: \n" f"{bounding_boxes}")

            raise ValueError("Output is not valid!")

        is_correct_2 = TestReadFromFileObjectDetectionModel.__is_correct_bounding_box(
            ground_truth_bounding_box=expected_bounding_box_2,
            predicted_bounding_box=bounding_boxes[2],
        )

        if not is_correct_2:
            logger.error(
                "Found wrong bounding_box: \n"
                f"  Expected:  {expected_bounding_box_2}\n"
                f"  Predicted: {bounding_boxes[2]}\n"
            )

            logger.error("All bounding_boxes: \n" f"{bounding_boxes}")

            raise ValueError("Output is not valid!")

    def test_read_from_file_object_detection_registry(self) -> None:
        model_registry = ModelRegistry()

        assert (
            model_registry.model_registry["read_from_file_object_detection"]
            == ReadFromFileObjectDetectionModel
        )

    def test_read_from_file_inference_coco(self) -> None:
        read_from_file_model = ReadFromFileObjectDetectionModel(
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

        _, bounding_boxes = read_from_file_model.predict(data_item=test_image_path)

        logger.info(bounding_boxes)

        self.__check_coco_bounding_boxes(bounding_boxes)

    def test_read_from_file_inference_coco_check_duplicate(self) -> None:
        read_from_file_model = ReadFromFileObjectDetectionModel(
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

        annotations = read_from_file_model.annotation_handler.parse_training_annotations()
        annotations.append(annotations[0])

        read_from_file_model.initialize_annotations_dict(annotations=annotations)

        _, bounding_boxes = read_from_file_model.predict(data_item=test_image_path)

    def test_read_from_file_inference_coco_image_based(self) -> None:
        read_from_file_model = ReadFromFileObjectDetectionModel(
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

        _, bounding_boxes = read_from_file_model.predict(data_item=test_image)

        self.__check_coco_bounding_boxes(bounding_boxes)

    def test_read_from_file_inference_pascal_voc(self) -> None:
        read_from_file_model = ReadFromFileObjectDetectionModel(
            from_yaml=os.path.join(
                self.project_root,
                "test_data/test_ReadFromFileObjectDetectionModel/",
                "read-from-file_pascal-voc_test.yaml",
            ),
            string_replacement_map=self.string_replacement_map,
        )

        test_image_path = os.path.join(
            self.project_root,
            "test_data/images/dummy_task/cars.jpg",
        )

        _, bounding_boxes = read_from_file_model.predict(data_item=test_image_path)

        self.__check_pascal_voc_bounding_boxes(bounding_boxes=bounding_boxes)

    def test_read_from_file_inference_many(self) -> None:
        read_from_file_config_path = os.path.join(
            self.project_root,
            "test_data/test_ReadFromFileObjectDetectionModel/",
            "read-from-file_pascal-voc_test.yaml",
        )

        read_from_file_model = ReadFromFileObjectDetectionModel(
            from_yaml=read_from_file_config_path,
            string_replacement_map=self.string_replacement_map,
        )

        test_image_path = os.path.join(
            self.project_root,
            "test_data/images/dummy_task/cars.jpg",
        )

        results = read_from_file_model.predict_many(data_items=[test_image_path, test_image_path])

        _, bounding_boxes = read_from_file_model.predict(data_item=test_image_path)

        for _, bounding_boxes in results:
            self.__check_pascal_voc_bounding_boxes(bounding_boxes=bounding_boxes)

    def test_read_from_file_image_based_from_annotations_only(self) -> None:
        read_from_file_model = ReadFromFileObjectDetectionModel(
            from_yaml=os.path.join(
                self.project_root,
                "test_data/test_ReadFromFileObjectDetectionModel/",
                "read-from-file_pascal-voc_test_annotations_only.yaml",
            ),
            string_replacement_map=self.string_replacement_map,
        )

        image_paths = [
            os.path.join(self.project_root, "test_data/images/dummy_task/cars.jpg"),
            os.path.join(self.project_root, "test_data/images/dummy_task/person.jpg"),
            os.path.join(self.project_root, "test_data/images/dummy_task/truck.jpg"),
        ]

        for test_image_path in image_paths:
            test_image = cv2.imread(test_image_path)
            _, predicted_bounding_boxes = read_from_file_model.predict(data_item=test_image)
            logger.debug(
                "Predict on '%s':\n%s"
                % (
                    test_image_path,
                    "".join([f"\t- {str(b)}\n" for b in predicted_bounding_boxes]),
                )
            )

            assert len(predicted_bounding_boxes) > 0

    def test_read_from_file_num_classes(self):
        read_from_file_model = ReadFromFileObjectDetectionModel(
            from_yaml=os.path.join(
                self.project_root,
                "test_data/test_ReadFromFileObjectDetectionModel/",
                "read-from-file_pascal-voc_test.yaml",
            ),
            string_replacement_map=self.string_replacement_map,
        )

        assert read_from_file_model.num_classes == 4

    def test_read_from_file_no_data(self):
        read_from_file_model = ReadFromFileObjectDetectionModel(
            from_yaml=os.path.join(
                self.project_root,
                "test_data/test_ReadFromFileObjectDetectionModel/",
                "read-from-file_pascal-voc_test.yaml",
            ),
            string_replacement_map=self.string_replacement_map,
        )

        with self.assertRaises(ValueError) as value_error:
            read_from_file_model.predict("")
            assert str(value_error) == "data_item='' not in lookup dict of the ReadFromFileModel"


if __name__ == "__main__":
    main()
