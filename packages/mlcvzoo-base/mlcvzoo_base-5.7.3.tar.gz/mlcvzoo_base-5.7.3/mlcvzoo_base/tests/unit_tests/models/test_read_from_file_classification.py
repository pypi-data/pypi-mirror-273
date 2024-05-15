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

from mlcvzoo_base.api.data.class_identifier import ClassIdentifier
from mlcvzoo_base.api.data.classification import Classification
from mlcvzoo_base.models.model_registry import ModelRegistry
from mlcvzoo_base.models.read_from_file.model import ReadFromFileClassificationModel
from mlcvzoo_base.tests.unit_tests.test_template import TestTemplate

logger = logging.getLogger(__name__)


class TestReadFromFileClassificationModel(TestTemplate):
    @staticmethod
    def __check_cvat_classifications(
        classifications: List[Classification],
    ) -> None:
        expected_classification = Classification(
            class_identifier=ClassIdentifier(
                class_id=2,
                class_name="car",
            ),
            score=1.0,
        )

        predicted_classification = classifications[0]

        is_correct: bool = (
            expected_classification.class_id == predicted_classification.class_id
            and expected_classification.class_name == predicted_classification.class_name
            and expected_classification.score == predicted_classification.score
        )

        if not is_correct:
            logger.error(
                "Found wrong classification: \n"
                f"  Expected (Name/ID):  {expected_classification.class_name, expected_classification.class_id}\n"
                f"  Expected Score: {expected_classification.score}\n"
                f"  Predicted (Name/ID): {predicted_classification.class_name, predicted_classification.class_id}\n"
                f"  Predicted Score: {predicted_classification.score}\n"
            )

            raise ValueError("Output is not valid!")

    def test_read_from_file_classification_registry(self) -> None:
        model_registry = ModelRegistry()

        assert (
            model_registry.model_registry["read_from_file_classification"]
            == ReadFromFileClassificationModel
        )

    def test_read_from_file_classification_model(self) -> None:
        read_from_file_model = ReadFromFileClassificationModel(
            from_yaml=os.path.join(
                self.project_root,
                "test_data/test_ReadFromFileObjectDetectionModel/",
                "read-from-file_cvat_test.yaml",
            ),
            string_replacement_map=self.string_replacement_map,
        )

        test_image_path = os.path.join(
            self.project_root,
            "test_data/images/dummy_task/cars.jpg",
        )

        _, classifications = read_from_file_model.predict(data_item=test_image_path)

        logger.info(classifications)

        self.__check_cvat_classifications(classifications=classifications)

    def test_read_from_file_classification_model_image_based(self) -> None:
        read_from_file_model = ReadFromFileClassificationModel(
            from_yaml=os.path.join(
                self.project_root,
                "test_data/test_ReadFromFileObjectDetectionModel/",
                "read-from-file_cvat_test.yaml",
            ),
            string_replacement_map=self.string_replacement_map,
        )

        test_image_path = os.path.join(
            self.project_root,
            "test_data/images/dummy_task/cars.jpg",
        )

        test_image = cv2.imread(test_image_path)

        _, classifications = read_from_file_model.predict(data_item=test_image)

        self.__check_cvat_classifications(classifications)

    def test_read_from_file_no_data(self):
        read_from_file_model = ReadFromFileClassificationModel(
            from_yaml=os.path.join(
                self.project_root,
                "test_data/test_ReadFromFileObjectDetectionModel/",
                "read-from-file_cvat_test.yaml",
            ),
            string_replacement_map=self.string_replacement_map,
        )

        with self.assertRaises(ValueError) as value_error:
            read_from_file_model.predict("")
            assert str(value_error) == "data_item='' not in lookup dict of the ReadFromFileModel"


if __name__ == "__main__":
    main()
