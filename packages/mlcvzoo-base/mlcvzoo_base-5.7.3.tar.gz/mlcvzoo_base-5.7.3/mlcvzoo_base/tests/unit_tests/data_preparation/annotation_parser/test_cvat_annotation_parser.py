# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

import logging
import os
from unittest import main

from mlcvzoo_base.data_preparation.annotation_handler import AnnotationHandler
from mlcvzoo_base.tests.unit_tests.test_template import TestTemplate

logger = logging.getLogger(__name__)


class TestCVATAnnotationParser(TestTemplate):
    def test_parse_from_cvat(self) -> None:
        logger.info(
            "############################################################\n"
            "# TEST parsing from cvat xml:\n"
            "#      test_parse_from_cvat(self)\n"
            "############################################################"
        )

        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_AnnotationHandler",
            "annotation-handler_cvat_test.yaml",
        )

        annotation_handler = AnnotationHandler(
            yaml_config_path=yaml_config_path,
            string_replacement_map=self.string_replacement_map,
        )

        # TODO: add detailed check for parsed annotations
        annotations = annotation_handler.parse_annotations_from_cvat()

    def test_parse_from_cvat_all_attributes(self) -> None:
        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_AnnotationHandler",
            "annotation-handler_cvat_all_attributes_test.yaml",
        )

        annotation_handler = AnnotationHandler(
            yaml_config_path=yaml_config_path,
            string_replacement_map=self.string_replacement_map,
        )

        annotations = annotation_handler.parse_annotations_from_cvat()

        assert len(annotations) == 4
        assert len(annotations[0].bounding_boxes) == 5
        assert len(annotations[1].bounding_boxes) == 0
        assert len(annotations[2].bounding_boxes) == 0
        assert len(annotations[3].bounding_boxes) == 0

        assert annotations[0].bounding_boxes[0].difficult is False
        assert annotations[0].bounding_boxes[0].occluded is False
        assert annotations[0].bounding_boxes[0].background is False
        assert annotations[0].bounding_boxes[0].content == "car"

        assert annotations[0].bounding_boxes[1].difficult is False
        assert annotations[0].bounding_boxes[1].occluded is False
        assert annotations[0].bounding_boxes[1].background is True
        assert annotations[0].bounding_boxes[1].content is ""

        assert annotations[0].bounding_boxes[2].difficult is True
        assert annotations[0].bounding_boxes[2].occluded is False
        assert annotations[0].bounding_boxes[2].background is False
        assert annotations[0].bounding_boxes[2].content is ""

        assert annotations[0].bounding_boxes[3].difficult is False
        assert annotations[0].bounding_boxes[3].occluded is False
        assert annotations[0].bounding_boxes[3].background is False
        assert annotations[0].bounding_boxes[3].content is ""

        assert annotations[0].bounding_boxes[4].difficult is False
        assert annotations[0].bounding_boxes[4].occluded is True
        assert annotations[0].bounding_boxes[4].background is True
        assert annotations[0].bounding_boxes[4].content is ""

    def test_parse_from_cvat_all_attributes_no_difficult(self) -> None:
        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_AnnotationHandler",
            "annotation-handler_cvat_all_attributes_test.yaml",
        )

        annotation_handler = AnnotationHandler(
            yaml_config_path=yaml_config_path,
            string_replacement_map=self.string_replacement_map,
        )
        annotation_handler.configuration.cvat_input_data[0].use_difficult = False

        annotations = annotation_handler.parse_annotations_from_cvat()

        assert len(annotations) == 4
        assert len(annotations[0].bounding_boxes) == 4
        assert len(annotations[1].bounding_boxes) == 0
        assert len(annotations[2].bounding_boxes) == 0
        assert len(annotations[3].bounding_boxes) == 0

        assert annotations[0].bounding_boxes[0].difficult is False
        assert annotations[0].bounding_boxes[0].occluded is False
        assert annotations[0].bounding_boxes[0].background is False
        assert annotations[0].bounding_boxes[0].content == "car"

        assert annotations[0].bounding_boxes[1].difficult is False
        assert annotations[0].bounding_boxes[1].occluded is False
        assert annotations[0].bounding_boxes[1].background is True
        assert annotations[0].bounding_boxes[1].content is ""

        assert annotations[0].bounding_boxes[2].difficult is False
        assert annotations[0].bounding_boxes[2].occluded is False
        assert annotations[0].bounding_boxes[2].background is False
        assert annotations[0].bounding_boxes[2].content is ""

        assert annotations[0].bounding_boxes[3].difficult is False
        assert annotations[0].bounding_boxes[3].occluded is True
        assert annotations[0].bounding_boxes[3].background is True
        assert annotations[0].bounding_boxes[3].content is ""

    def test_parse_from_cvat_all_attributes_no_occluded(self) -> None:
        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_AnnotationHandler",
            "annotation-handler_cvat_all_attributes_test.yaml",
        )

        annotation_handler = AnnotationHandler(
            yaml_config_path=yaml_config_path,
            string_replacement_map=self.string_replacement_map,
        )
        annotation_handler.configuration.cvat_input_data[0].use_occluded = False

        annotations = annotation_handler.parse_annotations_from_cvat()

        assert len(annotations) == 4
        assert len(annotations[0].bounding_boxes) == 4
        assert len(annotations[1].bounding_boxes) == 0
        assert len(annotations[2].bounding_boxes) == 0
        assert len(annotations[3].bounding_boxes) == 0

        assert annotations[0].bounding_boxes[0].difficult is False
        assert annotations[0].bounding_boxes[0].occluded is False
        assert annotations[0].bounding_boxes[0].background is False
        assert annotations[0].bounding_boxes[0].content == "car"

        assert annotations[0].bounding_boxes[1].difficult is False
        assert annotations[0].bounding_boxes[1].occluded is False
        assert annotations[0].bounding_boxes[1].background is True
        assert annotations[0].bounding_boxes[1].content is ""

        assert annotations[0].bounding_boxes[2].difficult is True
        assert annotations[0].bounding_boxes[2].occluded is False
        assert annotations[0].bounding_boxes[2].background is False
        assert annotations[0].bounding_boxes[2].content is ""

        assert annotations[0].bounding_boxes[3].difficult is False
        assert annotations[0].bounding_boxes[3].occluded is False
        assert annotations[0].bounding_boxes[3].background is False
        assert annotations[0].bounding_boxes[3].content is ""

    def test_parse_from_cvat_all_attributes_no_background(self) -> None:
        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_AnnotationHandler",
            "annotation-handler_cvat_all_attributes_test.yaml",
        )

        annotation_handler = AnnotationHandler(
            yaml_config_path=yaml_config_path,
            string_replacement_map=self.string_replacement_map,
        )
        annotation_handler.configuration.cvat_input_data[0].use_background = False

        annotations = annotation_handler.parse_annotations_from_cvat()

        assert len(annotations) == 4
        assert len(annotations[0].bounding_boxes) == 3
        assert len(annotations[1].bounding_boxes) == 0
        assert len(annotations[2].bounding_boxes) == 0
        assert len(annotations[3].bounding_boxes) == 0

        assert annotations[0].bounding_boxes[0].difficult is False
        assert annotations[0].bounding_boxes[0].occluded is False
        assert annotations[0].bounding_boxes[0].background is False
        assert annotations[0].bounding_boxes[0].content == "car"

        assert annotations[0].bounding_boxes[1].difficult is True
        assert annotations[0].bounding_boxes[1].occluded is False
        assert annotations[0].bounding_boxes[1].background is False
        assert annotations[0].bounding_boxes[1].content is ""

        assert annotations[0].bounding_boxes[2].difficult is False
        assert annotations[0].bounding_boxes[2].occluded is False
        assert annotations[0].bounding_boxes[2].background is False
        assert annotations[0].bounding_boxes[2].content is ""


if __name__ == "__main__":
    main()
