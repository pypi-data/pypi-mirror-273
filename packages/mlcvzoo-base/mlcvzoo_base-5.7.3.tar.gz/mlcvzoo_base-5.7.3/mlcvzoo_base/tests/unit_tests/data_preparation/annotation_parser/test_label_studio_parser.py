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


class TestLabelStudioAnnotationParser(TestTemplate):
    def test_parse_from_label_studio(self) -> None:
        logger.info(
            "############################################################\n"
            "# TEST parsing from label studio json:\n"
            "#      test_parse_from_label_studio(self)\n"
            "############################################################"
        )

        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_AnnotationHandler",
            "annotation-handler_label-studio_test.yaml",
        )

        annotation_handler = AnnotationHandler(
            yaml_config_path=yaml_config_path,
            string_replacement_map=self.string_replacement_map,
        )

        annotations = annotation_handler.parse_annotations_from_label_studio()

        annotations = sorted(annotations, key=lambda x: x.image_path)

        # TODO: add detailed check for parsed annotations
        assert len(annotations) == 3
        assert annotations[0].image_path == os.path.join(
            self.project_root, "test_data/images/dummy_task/cars.jpg"
        )
        assert annotations[1].image_path == os.path.join(
            self.project_root, "test_data/images/dummy_task/person.jpg"
        )
        assert annotations[2].image_path == os.path.join(
            self.project_root, "test_data/images/dummy_task/truck.jpg"
        )

    def test_parse_from_label_studio_errors(self) -> None:
        logger.info(
            "############################################################\n"
            "# TEST parsing from label studio json:\n"
            "#      test_parse_from_label_studio(self)\n"
            "############################################################"
        )

        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_AnnotationHandler",
            "annotation-handler_label-studio_errors_test.yaml",
        )

        annotation_handler = AnnotationHandler(
            yaml_config_path=yaml_config_path,
            string_replacement_map=self.string_replacement_map,
        )

        annotations = annotation_handler.parse_annotations_from_label_studio()

        annotations = sorted(annotations, key=lambda x: x.image_path)

        # TODO: add detailed check for parsed annotations
        assert len(annotations) == 2
        assert annotations[0].image_path == os.path.join(
            self.project_root, "test_data/images/dummy_task/cars.jpg"
        )
        assert annotations[1].image_path == os.path.join(
            self.project_root, "test_data/images/dummy_task/cars.jpg"
        )


if __name__ == "__main__":
    main()
