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


class TestPascalVOCAnnotationParser(TestTemplate):
    def test_parse_from_pascal_voc_xml(self) -> None:
        logger.info(
            "############################################################\n"
            "# TEST parsing from pascal-voc xml:\n"
            "#      test_parse_from_pascal_voc_xml(self)\n"
            "############################################################"
        )

        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_AnnotationHandler",
            "annotation-handler_pascal-voc_test.yaml",
        )

        annotation_handler = AnnotationHandler(
            yaml_config_path=yaml_config_path,
            string_replacement_map=self.string_replacement_map,
        )

        # TODO: add detailed check for parsed annotations
        annotations = annotation_handler.parse_annotations_from_xml()

    def test_parse_from_pascal_voc_xml_ignore_missing_images(self) -> None:
        logger.info(
            "############################################################\n"
            "# TEST parsing from pascal-voc xml:\n"
            "#      test_parse_from_pascal_voc_xml(self)\n"
            "############################################################"
        )

        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_AnnotationHandler",
            "annotation-handler_pascal-voc_test_ignore_missing_images.yaml",
        )

        annotation_handler = AnnotationHandler(
            yaml_config_path=yaml_config_path,
            string_replacement_map=self.string_replacement_map,
        )

        # TODO: add detailed check for parsed annotations
        annotations = annotation_handler.parse_annotations_from_xml()

    def test_parse_from_pascal_voc_all_attributes(self) -> None:
        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_AnnotationHandler",
            "annotation-handler_pascal-voc_all_attributes_test.yaml",
        )

        annotation_handler = AnnotationHandler(
            yaml_config_path=yaml_config_path,
            string_replacement_map=self.string_replacement_map,
        )

        annotations = annotation_handler.parse_annotations_from_xml()

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
        assert annotations[0].bounding_boxes[1].content == ""

        assert annotations[0].bounding_boxes[2].difficult is True
        assert annotations[0].bounding_boxes[2].occluded is False
        assert annotations[0].bounding_boxes[2].background is False
        assert annotations[0].bounding_boxes[2].content == ""

        assert annotations[0].bounding_boxes[3].difficult is False
        assert annotations[0].bounding_boxes[3].occluded is False
        assert annotations[0].bounding_boxes[3].background is False
        assert annotations[0].bounding_boxes[3].content == ""

        assert annotations[0].bounding_boxes[4].difficult is False
        assert annotations[0].bounding_boxes[4].occluded is True
        assert annotations[0].bounding_boxes[4].background is True
        assert annotations[0].bounding_boxes[4].content == ""

    def test_parse_from_pascal_voc_all_attributes_no_difficult(self) -> None:
        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_AnnotationHandler",
            "annotation-handler_pascal-voc_all_attributes_test.yaml",
        )

        annotation_handler = AnnotationHandler(
            yaml_config_path=yaml_config_path,
            string_replacement_map=self.string_replacement_map,
        )
        annotation_handler.configuration.pascal_voc_input_data[0].use_difficult = False

        annotations = annotation_handler.parse_annotations_from_xml()

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
        assert annotations[0].bounding_boxes[1].content == ""

        assert annotations[0].bounding_boxes[2].difficult is False
        assert annotations[0].bounding_boxes[2].occluded is False
        assert annotations[0].bounding_boxes[2].background is False
        assert annotations[0].bounding_boxes[2].content == ""

        assert annotations[0].bounding_boxes[3].difficult is False
        assert annotations[0].bounding_boxes[3].occluded is True
        assert annotations[0].bounding_boxes[3].background is True
        assert annotations[0].bounding_boxes[3].content == ""

    def test_parse_from_pascal_voc_all_attributes_no_occluded(self) -> None:
        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_AnnotationHandler",
            "annotation-handler_pascal-voc_all_attributes_test.yaml",
        )

        annotation_handler = AnnotationHandler(
            yaml_config_path=yaml_config_path,
            string_replacement_map=self.string_replacement_map,
        )
        annotation_handler.configuration.pascal_voc_input_data[0].use_occluded = False

        annotations = annotation_handler.parse_annotations_from_xml()

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
        assert annotations[0].bounding_boxes[1].content == ""

        assert annotations[0].bounding_boxes[2].difficult is True
        assert annotations[0].bounding_boxes[2].occluded is False
        assert annotations[0].bounding_boxes[2].background is False
        assert annotations[0].bounding_boxes[2].content == ""

        assert annotations[0].bounding_boxes[3].difficult is False
        assert annotations[0].bounding_boxes[3].occluded is False
        assert annotations[0].bounding_boxes[3].background is False
        assert annotations[0].bounding_boxes[3].content == ""

    def test_parse_from_pascal_voc_all_attributes_no_background(self) -> None:
        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_AnnotationHandler",
            "annotation-handler_pascal-voc_all_attributes_test.yaml",
        )

        annotation_handler = AnnotationHandler(
            yaml_config_path=yaml_config_path,
            string_replacement_map=self.string_replacement_map,
        )
        annotation_handler.configuration.pascal_voc_input_data[0].use_background = False

        annotations = annotation_handler.parse_annotations_from_xml()

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
        assert annotations[0].bounding_boxes[1].content == ""

        assert annotations[0].bounding_boxes[2].difficult is False
        assert annotations[0].bounding_boxes[2].occluded is False
        assert annotations[0].bounding_boxes[2].background is False
        assert annotations[0].bounding_boxes[2].content == ""


if __name__ == "__main__":
    main()
