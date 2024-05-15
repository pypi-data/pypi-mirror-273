# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

import logging
import os
from unittest import main
from unittest.mock import MagicMock

from pytest import fixture, mark
from pytest_mock import MockerFixture

from mlcvzoo_base.data_preparation.annotation_handler import AnnotationHandler
from mlcvzoo_base.tests.unit_tests.test_template import TestTemplate

logger = logging.getLogger(__name__)


@fixture(scope="function")
def cv2_imread_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        "cv2.imread",
        return_value=None,
    )


class TestMOTAnnotationParser(TestTemplate):
    def test_parse_from_mot2015(self) -> None:
        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_AnnotationHandler",
            "annotation-handler_mot2015_test.yaml",
        )

        annotation_handler = AnnotationHandler(
            yaml_config_path=yaml_config_path,
            string_replacement_map=self.string_replacement_map,
        )

        annotations = annotation_handler.parse_annotations_from_mot()

        logger.debug("Parsed Annotation Object: %s", annotations)

        # TODO: use os.path
        # assert annotations[0].image_shape == (500, 353)
        assert annotations[0].image_path == os.path.join(
            self.project_root,
            "test_data/images/dummy_task/cars.jpg",
        )
        assert annotations[0].image_dir == os.path.join(
            self.project_root,
            "test_data/images/dummy_task",
        )
        assert annotations[0].annotation_path == os.path.join(
            self.project_root,
            "test_data/annotations/mot/mot_ground-truth_2015.txt",
        )
        assert annotations[0].annotation_dir == os.path.join(
            self.project_root,
            "test_data/annotations/mot",
        )

        assert len(annotations[0].bounding_boxes) == 2

        assert annotations[0].bounding_boxes[0].class_id == 1
        assert annotations[0].bounding_boxes[0].class_name == "pedestrian"
        assert annotations[0].bounding_boxes[0].difficult is False
        assert annotations[0].bounding_boxes[0].score == 1.0

        assert annotations[0].bounding_boxes[0].box.xmin == 50
        assert annotations[0].bounding_boxes[0].box.ymin == 200
        assert annotations[0].bounding_boxes[0].box.xmax == 250
        assert annotations[0].bounding_boxes[0].box.ymax == 400

        assert annotations[0].bounding_boxes[1].class_id == 1
        assert annotations[0].bounding_boxes[1].class_name == "pedestrian"
        assert annotations[0].bounding_boxes[1].difficult is False
        assert annotations[0].bounding_boxes[1].score == 1.0

        assert annotations[0].bounding_boxes[1].box.xmin == 100
        assert annotations[0].bounding_boxes[1].box.ymin == 150
        assert annotations[0].bounding_boxes[1].box.xmax == 200
        assert annotations[0].bounding_boxes[1].box.ymax == 450

        assert len(annotations[1].bounding_boxes) == 2

        assert annotations[1].bounding_boxes[0].class_id == 1
        assert annotations[1].bounding_boxes[0].class_name == "pedestrian"
        assert annotations[1].bounding_boxes[0].difficult is False
        assert annotations[1].bounding_boxes[0].score == 1.0

        assert annotations[1].bounding_boxes[0].box.xmin == 50
        assert annotations[1].bounding_boxes[0].box.ymin == 200
        assert annotations[1].bounding_boxes[0].box.xmax == 200
        assert annotations[1].bounding_boxes[0].box.ymax == 400

        assert annotations[1].bounding_boxes[1].class_id == 1
        assert annotations[1].bounding_boxes[0].class_name == "pedestrian"
        assert annotations[1].bounding_boxes[1].difficult is False
        assert annotations[1].bounding_boxes[1].score == 1.0

        assert annotations[1].bounding_boxes[1].box.xmin == 100
        assert annotations[1].bounding_boxes[1].box.ymin == 200
        assert annotations[1].bounding_boxes[1].box.xmax == 250
        assert annotations[1].bounding_boxes[1].box.ymax == 250

        assert len(annotations[2].bounding_boxes) == 1

        assert annotations[2].bounding_boxes[0].class_id == 1
        assert annotations[2].bounding_boxes[0].class_name == "pedestrian"
        assert annotations[2].bounding_boxes[0].difficult is False
        assert annotations[2].bounding_boxes[0].score == 1.0

        assert annotations[2].bounding_boxes[0].box.xmin == 100
        assert annotations[2].bounding_boxes[0].box.ymin == 100
        assert annotations[2].bounding_boxes[0].box.xmax == 200
        assert annotations[2].bounding_boxes[0].box.ymax == 400

    def test_parse_from_mot201617(self) -> None:
        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_AnnotationHandler",
            "annotation-handler_mot201617_test.yaml",
        )

        annotation_handler = AnnotationHandler(
            yaml_config_path=yaml_config_path,
            string_replacement_map=self.string_replacement_map,
        )

        annotations = annotation_handler.parse_annotations_from_mot()

        logger.debug("Parsed Annotation Object: %s", annotations)

        # TODO: use os.path
        # assert annotations[0].image_shape == (500, 353)
        assert annotations[0].image_path == os.path.join(
            self.project_root,
            "test_data/images/dummy_task/cars.jpg",
        )
        assert annotations[0].image_dir == os.path.join(
            self.project_root,
            "test_data/images/dummy_task",
        )
        assert annotations[0].annotation_path == os.path.join(
            self.project_root,
            "test_data/annotations/mot/mot_ground-truth_201617.txt",
        )
        assert annotations[0].annotation_dir == os.path.join(
            self.project_root,
            "test_data/annotations/mot",
        )

        assert len(annotations[0].bounding_boxes) == 2

        assert annotations[0].bounding_boxes[0].class_id == 1
        assert annotations[0].bounding_boxes[0].class_name == "pedestrian"
        assert annotations[0].bounding_boxes[0].difficult is False
        assert annotations[0].bounding_boxes[0].score == 1.0

        assert annotations[0].bounding_boxes[0].box.xmin == 50
        assert annotations[0].bounding_boxes[0].box.ymin == 200
        assert annotations[0].bounding_boxes[0].box.xmax == 250
        assert annotations[0].bounding_boxes[0].box.ymax == 400

        assert annotations[0].bounding_boxes[1].class_id == 3
        assert annotations[0].bounding_boxes[1].class_name == "car"
        assert annotations[0].bounding_boxes[1].difficult is False
        assert annotations[0].bounding_boxes[1].score == 1.0

        assert annotations[0].bounding_boxes[1].box.xmin == 100
        assert annotations[0].bounding_boxes[1].box.ymin == 200
        assert annotations[0].bounding_boxes[1].box.xmax == 200
        assert annotations[0].bounding_boxes[1].box.ymax == 450

        assert len(annotations[1].bounding_boxes) == 2

        assert annotations[1].bounding_boxes[0].class_id == 1
        assert annotations[1].bounding_boxes[0].class_name == "pedestrian"
        assert annotations[1].bounding_boxes[0].difficult is False
        assert annotations[1].bounding_boxes[0].score == 1.0

        assert annotations[1].bounding_boxes[0].box.xmin == 50
        assert annotations[1].bounding_boxes[0].box.ymin == 200
        assert annotations[1].bounding_boxes[0].box.xmax == 200
        assert annotations[1].bounding_boxes[0].box.ymax == 400

        assert annotations[1].bounding_boxes[1].class_id == 1
        assert annotations[1].bounding_boxes[0].class_name == "pedestrian"
        assert annotations[1].bounding_boxes[1].difficult is False
        assert annotations[1].bounding_boxes[1].score == 1.0

        assert annotations[1].bounding_boxes[1].box.xmin == 100
        assert annotations[1].bounding_boxes[1].box.ymin == 200
        assert annotations[1].bounding_boxes[1].box.xmax == 250
        assert annotations[1].bounding_boxes[1].box.ymax == 250

        assert len(annotations[2].bounding_boxes) == 1

        assert annotations[2].bounding_boxes[0].class_id == 1
        assert annotations[2].bounding_boxes[0].class_name == "pedestrian"
        assert annotations[2].bounding_boxes[0].difficult is False
        assert (
            annotations[2].bounding_boxes[0].score == 1.0
        )  # ToDo check which score should be used

        assert annotations[2].bounding_boxes[0].box.xmin == 100
        assert annotations[2].bounding_boxes[0].box.ymin == 100
        assert annotations[2].bounding_boxes[0].box.xmax == 200
        assert annotations[2].bounding_boxes[0].box.ymax == 400

    def test_parse_from_mot2020(self) -> None:
        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_AnnotationHandler",
            "annotation-handler_mot2020_test.yaml",
        )

        annotation_handler = AnnotationHandler(
            yaml_config_path=yaml_config_path,
            string_replacement_map=self.string_replacement_map,
        )

        annotations = annotation_handler.parse_annotations_from_mot()

        logger.debug("Parsed Annotation Object: %s", annotations)

        assert len(annotations[0].bounding_boxes) == 2

        assert annotations[0].image_path == os.path.join(
            self.project_root,
            "test_data/images/dummy_task/cars.jpg",
        )
        assert annotations[0].image_dir == os.path.join(
            self.project_root,
            "test_data/images/dummy_task",
        )
        assert annotations[0].annotation_path == os.path.join(
            self.project_root,
            "test_data/annotations/mot/mot_ground-truth_2020.txt",
        )
        assert annotations[0].annotation_dir == os.path.join(
            self.project_root,
            "test_data/annotations/mot",
        )

        assert annotations[0].bounding_boxes[0].class_id == 1
        assert annotations[0].bounding_boxes[0].class_name == "pedestrian"
        assert annotations[0].bounding_boxes[0].difficult is False
        assert (
            annotations[0].bounding_boxes[0].score == 1.0
        )  # ToDo check which score should be used

        assert annotations[0].bounding_boxes[0].box.xmin == 50
        assert annotations[0].bounding_boxes[0].box.ymin == 200
        assert annotations[0].bounding_boxes[0].box.xmax == 250
        assert annotations[0].bounding_boxes[0].box.ymax == 400

        assert annotations[0].bounding_boxes[1].class_id == 1
        assert annotations[0].bounding_boxes[1].class_name == "pedestrian"
        assert annotations[0].bounding_boxes[1].difficult is False
        assert (
            annotations[0].bounding_boxes[1].score == 1.0
        )  # ToDo check which score should be used

        assert annotations[0].bounding_boxes[1].box.xmin == 100
        assert annotations[0].bounding_boxes[1].box.ymin == 150
        assert annotations[0].bounding_boxes[1].box.xmax == 200
        assert annotations[0].bounding_boxes[1].box.ymax == 450

        assert len(annotations[1].bounding_boxes) == 1

        assert annotations[1].image_path == os.path.join(
            self.project_root,
            "test_data/images/dummy_task/empty.jpg",
        )
        assert annotations[1].image_dir == os.path.join(
            self.project_root,
            "test_data/images/dummy_task",
        )
        assert annotations[1].annotation_path == os.path.join(
            self.project_root,
            "test_data/annotations/mot/mot_ground-truth_2020.txt",
        )
        assert annotations[1].annotation_dir == os.path.join(
            self.project_root,
            "test_data/annotations/mot",
        )

        assert annotations[1].bounding_boxes[0].class_id == 1
        assert annotations[1].bounding_boxes[0].class_name == "pedestrian"
        assert annotations[1].bounding_boxes[0].difficult is False
        assert annotations[1].bounding_boxes[0].score == 1.0

        assert annotations[1].bounding_boxes[0].box.xmin == 50
        assert annotations[1].bounding_boxes[0].box.ymin == 200
        assert annotations[1].bounding_boxes[0].box.xmax == 200
        assert annotations[1].bounding_boxes[0].box.ymax == 400

        assert len(annotations[2].bounding_boxes) == 1

        assert annotations[2].image_path == os.path.join(
            self.project_root,
            "test_data/images/dummy_task/person.jpg",
        )
        assert annotations[2].image_dir == os.path.join(
            self.project_root,
            "test_data/images/dummy_task",
        )
        assert annotations[2].annotation_path == os.path.join(
            self.project_root,
            "test_data/annotations/mot/mot_ground-truth_2020.txt",
        )
        assert annotations[2].annotation_dir == os.path.join(
            self.project_root,
            "test_data/annotations/mot",
        )

        assert annotations[2].bounding_boxes[0].class_id == 3
        assert annotations[2].bounding_boxes[0].class_name == "car"
        assert annotations[2].bounding_boxes[0].difficult is False
        assert annotations[2].bounding_boxes[0].score == 1.0

        assert annotations[2].bounding_boxes[0].box.xmin == 100
        assert annotations[2].bounding_boxes[0].box.ymin == 300
        assert annotations[2].bounding_boxes[0].box.xmax == 250
        assert annotations[2].bounding_boxes[0].box.ymax == 350

    def test_parse_from_mot_invalid_format_in_yaml(self) -> None:
        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_AnnotationHandler",
            "annotation-handler_mot-invalid-format_test.yaml",
        )

        with self.assertRaises(ValueError):
            AnnotationHandler(
                yaml_config_path=yaml_config_path,
                string_replacement_map=self.string_replacement_map,
            )

    def test_parse_from_mot_builder_invalid_format(self) -> None:
        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_AnnotationHandler",
            "annotation-handler_mot2020_test.yaml",
        )

        annotation_handler = AnnotationHandler(
            yaml_config_path=yaml_config_path,
            string_replacement_map=self.string_replacement_map,
        )
        annotation_handler.configuration.mot_input_data[0].mot_format = "2020"

        with self.assertRaises(ValueError):
            annotation_handler.parse_annotations_from_mot()

    def test_parse_mot_with_mapping_error(self) -> None:
        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_AnnotationHandler",
            "annotation-handler_mot_missing-class_test.yaml",
        )

        annotation_handler = AnnotationHandler(
            yaml_config_path=yaml_config_path,
            string_replacement_map=self.string_replacement_map,
        )

        annotations = annotation_handler.parse_annotations_from_mot()

        assert len(annotations[0].bounding_boxes) == 2

        assert annotations[0].image_path == os.path.join(
            self.project_root,
            "test_data/images/dummy_task/cars.jpg",
        )
        assert annotations[0].image_dir == os.path.join(
            self.project_root,
            "test_data/images/dummy_task",
        )
        assert annotations[0].annotation_path == os.path.join(
            self.project_root,
            "test_data/annotations/mot/mot_ground-truth_2020.txt",
        )
        assert annotations[0].annotation_dir == os.path.join(
            self.project_root,
            "test_data/annotations/mot",
        )

        assert annotations[0].bounding_boxes[0].class_id == 0
        assert annotations[0].bounding_boxes[0].class_name == "person"
        assert annotations[0].bounding_boxes[0].difficult is False
        assert (
            annotations[0].bounding_boxes[0].score == 1.0
        )  # ToDo check which score should be used

        assert annotations[0].bounding_boxes[0].box.xmin == 50
        assert annotations[0].bounding_boxes[0].box.ymin == 200
        assert annotations[0].bounding_boxes[0].box.xmax == 250
        assert annotations[0].bounding_boxes[0].box.ymax == 400

        assert annotations[0].bounding_boxes[1].class_id == 0
        assert annotations[0].bounding_boxes[1].class_name == "person"
        assert annotations[0].bounding_boxes[1].difficult is False
        assert (
            annotations[0].bounding_boxes[1].score == 1.0
        )  # ToDo check which score should be used

        assert annotations[0].bounding_boxes[1].box.xmin == 100
        assert annotations[0].bounding_boxes[1].box.ymin == 150
        assert annotations[0].bounding_boxes[1].box.xmax == 200
        assert annotations[0].bounding_boxes[1].box.ymax == 450

        assert len(annotations[1].bounding_boxes) == 1

        assert annotations[1].image_path == os.path.join(
            self.project_root,
            "test_data/images/dummy_task/empty.jpg",
        )
        assert annotations[1].image_dir == os.path.join(
            self.project_root,
            "test_data/images/dummy_task",
        )
        assert annotations[1].annotation_path == os.path.join(
            self.project_root,
            "test_data/annotations/mot/mot_ground-truth_2020.txt",
        )
        assert annotations[1].annotation_dir == os.path.join(
            self.project_root,
            "test_data/annotations/mot",
        )

        assert annotations[1].bounding_boxes[0].class_id == 0
        assert annotations[1].bounding_boxes[0].class_name == "person"
        assert annotations[1].bounding_boxes[0].difficult is False
        assert annotations[1].bounding_boxes[0].score == 1.0

        assert annotations[1].bounding_boxes[0].box.xmin == 50
        assert annotations[1].bounding_boxes[0].box.ymin == 200
        assert annotations[1].bounding_boxes[0].box.xmax == 200
        assert annotations[1].bounding_boxes[0].box.ymax == 400

        assert len(annotations[2].bounding_boxes) == 1

        assert annotations[2].image_path == os.path.join(
            self.project_root,
            "test_data/images/dummy_task/person.jpg",
        )
        assert annotations[2].image_dir == os.path.join(
            self.project_root,
            "test_data/images/dummy_task",
        )
        assert annotations[2].annotation_path == os.path.join(
            self.project_root,
            "test_data/annotations/mot/mot_ground-truth_2020.txt",
        )
        assert annotations[2].annotation_dir == os.path.join(
            self.project_root,
            "test_data/annotations/mot",
        )

        assert annotations[2].bounding_boxes[0].class_id == 2
        assert annotations[2].bounding_boxes[0].class_name == "car"
        assert annotations[2].bounding_boxes[0].difficult is False
        assert annotations[2].bounding_boxes[0].score == 1.0

        assert annotations[2].bounding_boxes[0].box.xmin == 100
        assert annotations[2].bounding_boxes[0].box.ymin == 300
        assert annotations[2].bounding_boxes[0].box.xmax == 250
        assert annotations[2].bounding_boxes[0].box.ymax == 350

    def test_parse_from_mot2020_no_gt(self) -> None:
        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_AnnotationHandler",
            "annotation-handler_mot2020_no-gt-data_test.yaml",
        )

        annotation_handler = AnnotationHandler(
            yaml_config_path=yaml_config_path,
            string_replacement_map=self.string_replacement_map,
        )

        annotations = annotation_handler.parse_annotations_from_mot()

        logger.info("Parsed annotations: %s", annotations)

        # assert annotations[0].image_shape == (500, 353)
        assert annotations[0].image_path == os.path.join(
            self.project_root,
            "test_data/images/dummy_task/cars.jpg",
        )
        assert annotations[0].image_dir == os.path.join(
            self.project_root,
            "test_data/images/dummy_task",
        )
        assert annotations[0].annotation_path == os.path.join(
            self.project_root,
            "test_data/annotations/mot/mot_predictions_2020.txt",
        )
        assert annotations[0].annotation_dir == os.path.join(
            self.project_root,
            "test_data/annotations/mot",
        )

        assert len(annotations[0].bounding_boxes) == 1

        assert annotations[0].bounding_boxes[0].class_id == 1
        assert annotations[0].bounding_boxes[0].class_name == "pedestrian"
        assert annotations[0].bounding_boxes[0].difficult is False
        assert (
            annotations[0].bounding_boxes[0].score == 0.9
        )  # ToDo check which score should be used

        assert annotations[0].bounding_boxes[0].box.xmin == 50
        assert annotations[0].bounding_boxes[0].box.ymin == 200
        assert annotations[0].bounding_boxes[0].box.xmax == 250
        assert annotations[0].bounding_boxes[0].box.ymax == 400

        assert len(annotations[1].bounding_boxes) == 1

        assert annotations[1].bounding_boxes[0].class_id == 1
        assert annotations[1].bounding_boxes[0].class_name == "pedestrian"
        assert annotations[1].bounding_boxes[0].difficult is False
        assert annotations[1].bounding_boxes[0].score == 0.75

        assert annotations[1].bounding_boxes[0].box.xmin == 50
        assert annotations[1].bounding_boxes[0].box.ymin == 200
        assert annotations[1].bounding_boxes[0].box.xmax == 200
        assert annotations[1].bounding_boxes[0].box.ymax == 400

        assert len(annotations[2].bounding_boxes) == 1

        assert annotations[2].bounding_boxes[0].class_id == 3  # ToDo insert correct class_id
        assert annotations[2].bounding_boxes[0].class_name == "car"
        assert annotations[2].bounding_boxes[0].difficult is False
        assert annotations[2].bounding_boxes[0].score == 0.6

        assert annotations[2].bounding_boxes[0].box.xmin == 100
        assert annotations[2].bounding_boxes[0].box.ymin == 100
        assert annotations[2].bounding_boxes[0].box.xmax == 200
        assert annotations[2].bounding_boxes[0].box.ymax == 400

    def test_ignore_class_mot_annotation_parser(self) -> None:
        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_AnnotationHandler",
            "annotation-handler_mot2020_ignore-class-names_test.yaml",
        )

        annotation_handler = AnnotationHandler(
            yaml_config_path=yaml_config_path,
            string_replacement_map=self.string_replacement_map,
        )

        annotations = annotation_handler.parse_annotations_from_mot()

        logger.info("Parsed annotations: %s", annotations)

        assert len(annotations) == 1
        assert len(annotations[0].bounding_boxes) == 1

        assert annotations[0].image_path == os.path.join(
            self.project_root,
            "test_data/images/dummy_task/person.jpg",
        )
        assert annotations[0].image_dir == os.path.join(
            self.project_root,
            "test_data/images/dummy_task",
        )
        assert annotations[0].annotation_path == os.path.join(
            self.project_root,
            "test_data/annotations/mot/mot_ground-truth_2020.txt",
        )
        assert annotations[0].annotation_dir == os.path.join(
            self.project_root,
            "test_data/annotations/mot",
        )

        assert annotations[0].bounding_boxes[0].class_id == 3
        assert annotations[0].bounding_boxes[0].class_name == "car"
        assert annotations[0].bounding_boxes[0].difficult is False
        assert annotations[0].bounding_boxes[0].score == 1.0

        assert annotations[0].bounding_boxes[0].box.xmin == 100
        assert annotations[0].bounding_boxes[0].box.ymin == 300
        assert annotations[0].bounding_boxes[0].box.xmax == 250
        assert annotations[0].bounding_boxes[0].box.ymax == 350

    def test_parse_from_custom(self) -> None:
        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_AnnotationHandler",
            "annotation-handler_mot-custom_test.yaml",
        )

        annotation_handler = AnnotationHandler(
            yaml_config_path=yaml_config_path,
            string_replacement_map=self.string_replacement_map,
        )

        annotations = annotation_handler.parse_annotations_from_mot()

        logger.debug("Parsed Annotation Object: %s", annotations)

        assert len(annotations[0].bounding_boxes) == 2
        assert annotations[0].bounding_boxes[0].class_name == "Person_Pedestrian"
        assert annotations[0].bounding_boxes[1].class_name == "Person_Pedestrian"
        assert len(annotations[1].bounding_boxes) == 1
        assert annotations[1].bounding_boxes[0].class_name == "Person_Pedestrian"
        assert len(annotations[2].bounding_boxes) == 1
        assert annotations[2].bounding_boxes[0].class_name == "Vehicle_Car"

    @mark.usefixtures("cv2_imread_mock")
    def test_parse_no_image_path(self) -> None:
        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_AnnotationHandler",
            "annotation-handler_mot-custom_test.yaml",
        )

        annotation_handler = AnnotationHandler(
            yaml_config_path=yaml_config_path,
            string_replacement_map=self.string_replacement_map,
        )

        annotations = annotation_handler.parse_annotations_from_mot()

        assert len(annotations) == 0


if __name__ == "__main__":
    main()
