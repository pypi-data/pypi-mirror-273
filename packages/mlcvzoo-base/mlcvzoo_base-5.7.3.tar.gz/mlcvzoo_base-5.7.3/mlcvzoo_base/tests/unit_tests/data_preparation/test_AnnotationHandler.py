# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

import hashlib
import logging
import os
import xml.etree.ElementTree as ET_xml
from typing import List
from unittest import main

from mlcvzoo_base.api.data.annotation import BaseAnnotation
from mlcvzoo_base.api.data.annotation_class_mapper import AnnotationClassMapper
from mlcvzoo_base.api.data.bounding_box import BoundingBox
from mlcvzoo_base.api.data.box import Box
from mlcvzoo_base.api.data.class_identifier import ClassIdentifier
from mlcvzoo_base.api.data.classification import Classification
from mlcvzoo_base.api.data.segmentation import Segmentation
from mlcvzoo_base.configuration.class_mapping_config import (
    ClassMappingConfig,
    ClassMappingModelClassesConfig,
)
from mlcvzoo_base.configuration.reduction_mapping_config import (
    ReductionMappingConfig,
    ReductionMappingMappingConfig,
)
from mlcvzoo_base.data_preparation.annotation_handler import AnnotationHandler
from mlcvzoo_base.data_preparation.structs import CSVOutputStringFormats
from mlcvzoo_base.tests.unit_tests.test_template import TestTemplate

logger = logging.getLogger(__name__)

# TODO: add test for the filtering of a "BAD IMAGE" tag/box
# TODO: add test that surrounding box is written to csv files


def _md5sum(output_dir: str, image_sub_path: str) -> str:
    with open(os.path.join(output_dir, image_sub_path), "rb") as image_file:
        content = image_file.read()
        md5 = hashlib.md5(content).hexdigest()
        return md5


def _xml_equal(xml_path_1: str, xml_path_2: str) -> bool:
    """
    Helper for comparison of two XML trees

    Args:
        xml_path_1: path to one xml file
        xml_path_2: path to the other xml file

    Returns:
        True if xml trees are identical, else False.
    """

    tree_1 = ET_xml.parse(xml_path_1)
    root_1 = tree_1.getroot()

    tree_2 = ET_xml.parse(xml_path_2)
    root_2 = tree_2.getroot()

    return _xml_root_compare(root_1=root_1, root_2=root_2)


def _xml_root_compare(root_1: ET_xml.Element, root_2: ET_xml.Element) -> bool:
    """
    Recursive helper function that compares tags and attributes of a tree and
     calls itself for each child.
    Args:
        root_1: xml.etree.ElementTree.Element object
        root_2: xml.etree.ElementTree.Element object

    Returns:
        True if trees are identical, else False.

    """

    if root_1.tag == root_2.tag:
        # NOTE: The local and gitlab-ci "path" tag are different, but are
        #       not relevant for this test
        if root_1.tag == "path":
            result = True
        elif root_1.tag == root_2.tag and root_1.text == root_2.text:
            result = True

            for index, child_1 in enumerate(root_1):
                if len(root_2) > index:
                    child_2 = root_2[index]
                    result = result and _xml_root_compare(child_1, child_2)
                else:
                    # If both roots do have the same length, they are not equal
                    result = False
                    break
        else:
            result = False
    else:
        result = False

    return result


class TestAnnotationHandler(TestTemplate):
    def test_generate_csv(self) -> None:
        logger.info(
            "############################################################\n"
            "# TEST generation of csv:\n"
            "#      test_generate_csv(self)\n"
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

        annotations: List[BaseAnnotation] = annotation_handler.parse_annotations_from_xml()

        annotation_handler.generate_csv(
            annotations=annotations, output_string_format=CSVOutputStringFormats.BASE
        )

        eval_string = (
            "IMAGE_DIR_0/dummy_task/person.jpg "
            "500 353 64,46,349,329,person 70,35,350,340,person"
        )

        train_string_0 = (
            "IMAGE_DIR_0/dummy_task/cars.jpg "
            "500 406 63,60,298,381,car 63,60,298,381,car 67,58,305,370,car"
        )
        train_string_1 = (
            "IMAGE_DIR_0/dummy_task/truck.jpg "
            "375 500 45,63,271,370,truck 45,63,271,369,truck 40,70,260,367,truck"
        )

        eval_path = os.path.join(self.project_root, "test_output", "test-task_eval.csv")
        train_path = os.path.join(self.project_root, "test_output", "test-task_train.csv")

        # CHECK eval file for correct content
        with open(eval_path, mode="r") as eval_file:
            eval_lines = eval_file.readlines()

        logger.info(
            f"==================================================================\n"
            "\n\neval_lines[0] %s\n"
            "eval_string %s\n\n"
            f"==================================================================\n",
            eval_lines[0].strip(),
            eval_string,
        )
        assert eval_lines[0].strip() == eval_string

        # CHECK train file for correct content
        with open(train_path, mode="r") as train_file:
            train_lines = train_file.readlines()

        logger.info(
            "==================================================================\n"
            "\n\ntrain_lines[0] %s\n"
            "train_string_0 %s\n\n"
            "==================================================================\n",
            train_lines[0].strip(),
            train_string_0,
        )
        assert train_lines[0].strip() == train_string_0

        logger.info(
            "==================================================================\n"
            "\n\ntrain_lines[1] %s\n"
            "train_string_1 %s\n\n"
            "==================================================================\n",
            train_lines[1].strip(),
            train_string_1,
        )
        assert train_lines[1].strip() == train_string_1

    def test_generate_csv_dont_use_occluded_and_difficult(self) -> None:
        logger.info(
            "############################################################\n"
            "# TEST generation of csv:\n"
            "#      test_generate_csv(self)\n"
            "############################################################"
        )

        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_AnnotationHandler",
            "annotation-handler_coco_test.yaml",
        )

        annotation_handler = AnnotationHandler(
            yaml_config_path=yaml_config_path,
            string_replacement_map=self.string_replacement_map,
        )

        annotations: List[BaseAnnotation] = annotation_handler.parse_annotations_from_coco()

        annotation_handler.generate_csv(
            annotations=annotations, output_string_format=CSVOutputStringFormats.BASE
        )

        val_string_0 = (
            "IMAGE_DIR_0/person.jpg 500 353 "
            "23,7,337,474,person 159,386,168,391,lp 73,252,221,340,person"
        )
        val_string_1 = (
            "IMAGE_DIR_0/cars.jpg 406 500 "
            "16,313,80,364,car 139,267,287,355,person 309,348,318,353,lp"
        )

        val_path = os.path.join(
            self.project_root,
            "test_output",
            "test-task_difficult-occluded_validation.csv",
        )

        # CHECK eval file for correct content
        with open(val_path, mode="r") as val_file:
            val_lines = val_file.readlines()

        logger.info(
            "==================================================================\n"
            "\n\ntrain_lines[0] %s\n"
            "train_string_0 %s\n\n"
            "==================================================================\n",
            val_lines[0].strip(),
            val_string_0,
        )
        assert val_lines[0].strip() == val_string_0

        logger.info(
            "==================================================================\n"
            "\n\nval_lines[1] %s\n"
            "val_string_1 %s\n\n"
            "==================================================================\n",
            val_lines[1].strip(),
            val_string_1,
        )
        assert val_lines[1].strip() == val_string_1

    def test_generate_csv_wrong_format(self) -> None:
        logger.info(
            "############################################################\n"
            "# TEST generation of csv:\n"
            "#      test_generate_csv(self)\n"
            "############################################################"
        )

        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_AnnotationHandler",
            "annotation-handler_coco_test.yaml",
        )

        annotation_handler = AnnotationHandler(
            yaml_config_path=yaml_config_path,
            string_replacement_map=self.string_replacement_map,
        )

        annotations: List[BaseAnnotation] = annotation_handler.parse_annotations_from_coco()

        with self.assertRaises(ValueError):
            annotation_handler.generate_csv(annotations=annotations, output_string_format="WRONG")

    def test_generate_darknet_train_set(self) -> None:
        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_AnnotationHandler",
            "annotation-handler_generate-darknet_test.yaml",
        )

        annotation_handler = AnnotationHandler(
            yaml_config_path=yaml_config_path,
            string_replacement_map=self.string_replacement_map,
        )

        annotations: List[BaseAnnotation] = annotation_handler.parse_annotations_from_xml()

        output_dir = os.path.join(self.project_root, "test_output", "darknet_train_set")

        annotation_handler.generate_darknet_train_set(
            annotations=annotations,
        )

        assert _md5sum(output_dir, "JPEGImages/cars.jpg") == "e1126d7955bf1691b8182b2170bf530c"
        assert _md5sum(output_dir, "JPEGImages/person.jpg") == "f5de025562070a71da4b791d52b04614"
        assert _md5sum(output_dir, "JPEGImages/truck.jpg") == "f4b1d605ec675098df2e39c19c93e720"
        with open(os.path.join(output_dir, "labels/cars.txt")) as cars_file:
            cars_lines = cars_file.readlines()

        assert cars_lines == [
            "2 0.4445812807881774 0.441 0.5788177339901478 0.642\n",
            "2 0.4445812807881774 0.441 0.5788177339901478 0.642\n",
            "2 0.458128078817734 0.428 0.5862068965517241 0.624\n",
        ]

        with open(os.path.join(output_dir, "labels/person.txt")) as person_file:
            person_lines = person_file.readlines()

        assert person_lines == [
            "0 0.584985835694051 0.375 0.8073654390934845 0.566\n",
            "0 0.594900849858357 0.375 0.7932011331444759 0.61\n",
        ]

        with open(os.path.join(output_dir, "labels/truck.txt")) as truck_file:
            truck_lines = truck_file.readlines()

        assert truck_lines == [
            "1 0.316 0.5773333333333334 0.452 0.8186666666666667\n",
            "1 0.316 0.576 0.452 0.816\n",
            "1 0.30000000000000004 0.5706666666666667 0.4 0.8213333333333334\n",
            "1 0.3 0.5826666666666667 0.44 0.792\n",
        ]

        line_count = 0

        test_file_path = (
            annotation_handler.configuration.write_output.darknet_train_set.get_test_file_path()
        )
        train_file_path = (
            annotation_handler.configuration.write_output.darknet_train_set.get_train_file_path()
        )

        with open(test_file_path, "r") as f:
            for _ in f:
                line_count += 1
        with open(train_file_path, "r") as f:
            for _ in f:
                line_count += 1
        assert line_count == 3

    def test_generate_yolo_csv(self) -> None:
        logger.info(
            "############################################################\n"
            "# TEST generation of txt:\n"
            "#      test_generate_txt(self)\n"
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

        annotations: List[BaseAnnotation] = annotation_handler.parse_annotations_from_xml()

        annotation_handler.generate_csv(
            annotations=annotations, output_string_format=CSVOutputStringFormats.YOLO
        )

        eval_string = "IMAGE_DIR_0/dummy_task/person.jpg " "64,46,349,329,0 70,35,350,340,0"

        train_string_0 = (
            "IMAGE_DIR_0/dummy_task/cars.jpg " "63,60,298,381,2 63,60,298,381,2 67,58,305,370,2"
        )

        train_string_1 = (
            "IMAGE_DIR_0/dummy_task/truck.jpg " "45,63,271,370,1 45,63,271,369,1 40,70,260,367,1"
        )

        eval_path = os.path.join(self.project_root, "test_output", "test-task_eval.txt")

        train_path = os.path.join(self.project_root, "test_output", "test-task_train.txt")

        # CHECK eval file for correct content
        with open(eval_path, mode="r") as eval_file:
            eval_lines = eval_file.readlines()

        logger.info(
            "==================================================================\n"
            "\n\neval_lines[0] %s\n"
            "eval_string %s\n\n"
            "==================================================================\n",
            eval_lines[0].strip(),
            eval_string,
        )

        # CHECK train file for correct content
        with open(train_path, mode="r") as train_file:
            train_lines = train_file.readlines()

        logger.info(
            "==================================================================\n"
            "\n\ntrain_lines[0] %s\n"
            "train_string_0 %s\n\n"
            "==================================================================\n",
            train_lines[0].strip(),
            train_string_0,
        )
        assert train_lines[0].strip() == train_string_0

        logger.info(
            "==================================================================\n"
            "\n\ntrain_lines[1] %s\n"
            "train_string_1 %s\n\n"
            "==================================================================\n",
            train_lines[1].strip(),
            train_string_1,
        )
        assert train_lines[1].strip() == train_string_1

    def test_parse_annotations_from_csv(self) -> None:
        logger.info(
            "############################################################\n"
            "# TEST parsing from csv:\n"
            "#      test_parse_annotations_from_csv(self)\n"
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

        train_path = os.path.join(self.project_root, "test_output", "test-task_train.csv")

        annotations = annotation_handler.parse_annotations_from_csv(csv_file_path=train_path)

        assert annotations[0].image_shape == (500, 406)
        assert annotations[0].image_path == os.path.join(
            self.project_root,
            "test_data/images/dummy_task/cars.jpg",
        )
        assert annotations[0].image_dir == os.path.join(
            self.project_root,
            "test_data/images",
        )
        assert annotations[0].annotation_path == os.path.join(
            self.project_root,
            "test_data/annotations/pascal_voc/dummy_task/cars.xml",
        )
        assert annotations[0].annotation_dir == os.path.join(
            self.project_root,
            "test_data/annotations/pascal_voc",
        )

        assert annotations[0].bounding_boxes[0].class_id == 2
        assert annotations[0].bounding_boxes[0].class_name == "car"
        assert annotations[0].bounding_boxes[0].difficult is False
        assert annotations[0].bounding_boxes[0].score == 1.0

        assert annotations[0].bounding_boxes[0].box.xmin == 63
        assert annotations[0].bounding_boxes[0].box.ymin == 60
        assert annotations[0].bounding_boxes[0].box.xmax == 298
        assert annotations[0].bounding_boxes[0].box.ymax == 381

    def test_parse_from_all_sources(self) -> None:
        logger.info(
            "############################################################\n"
            "# TEST parsing from all sources:\n"
            "#      test_parse_from_all_sources(self)\n"
            "############################################################"
        )

        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_AnnotationHandler",
            "annotation-handler_all_sources_test.yaml",
        )

        annotation_handler = AnnotationHandler(
            yaml_config_path=yaml_config_path,
            string_replacement_map=self.string_replacement_map,
        )

        # TODO: add detailed check for parsed annotations
        annotations = annotation_handler.parse_training_annotations()

    def test_load_meta_info_from_cvat(self) -> None:
        logger.info(
            "############################################################\n"
            "# TEST parsing meta info from cvat xml:\n"
            "#      test_parse_meta_info_from_cvat(self)\n"
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

        meta = annotation_handler.parse_meta_info_from_cvat()[0]
        tasks = meta.findall("task")
        dumped = meta.findall("dumped")

        assert len(tasks) == 1
        assert len(dumped) == 1

        labels = tasks[0].findall("labels")
        assert len(labels) == 1

        label_tags = labels[0].findall("label")
        assert len(label_tags) == 4

        segments = tasks[0].findall("segments")
        assert len(segments) == 1

        segment_tags = segments[0].findall("segment")
        assert len(segment_tags) == 1

    def test_reduce_annotations(self):
        annotations = [
            BaseAnnotation(
                image_path="TEST_PATH/test.jpg",
                classifications=[
                    Classification(
                        class_identifier=ClassIdentifier(
                            class_id=0,
                            class_name="person",
                        ),
                        score=0.7,
                    ),
                    Classification(
                        class_identifier=ClassIdentifier(
                            class_id=1,
                            class_name="car",
                        ),
                        score=0.7,
                    ),
                ],
                bounding_boxes=[
                    BoundingBox(
                        box=Box(xmin=0, ymin=0, xmax=100, ymax=100),
                        class_identifier=ClassIdentifier(
                            class_id=0,
                            class_name="person",
                        ),
                        score=0.7,
                        difficult=False,
                        occluded=False,
                        background=False,
                        content="",
                    ),
                    BoundingBox(
                        box=Box(xmin=0, ymin=0, xmax=100, ymax=100),
                        class_identifier=ClassIdentifier(
                            class_id=1,
                            class_name="car",
                        ),
                        score=0.8,
                        difficult=False,
                        occluded=False,
                        background=False,
                        content="",
                    ),
                ],
                segmentations=[
                    Segmentation(
                        polygon=[(0, 0), (100, 0), (100, 100), (0, 100)],
                        box=Box(xmin=0, ymin=0, xmax=100, ymax=100),
                        class_identifier=ClassIdentifier(
                            class_id=0,
                            class_name="person",
                        ),
                        score=0.8,
                        difficult=False,
                        occluded=False,
                        background=False,
                        content="",
                    ),
                    Segmentation(
                        polygon=[(0, 0), (100, 0), (100, 100), (0, 100)],
                        box=Box(xmin=0, ymin=0, xmax=100, ymax=100),
                        class_identifier=ClassIdentifier(
                            class_id=1,
                            class_name="car",
                        ),
                        score=0.7,
                        difficult=False,
                        occluded=False,
                        background=False,
                        content="",
                    ),
                ],
                annotation_path="TEST_PATH/test.xml",
                image_shape=(1, 1),
                image_dir="",
                annotation_dir="",
                replacement_string="",
            )
        ]

        reduced_annotations = AnnotationHandler.reduce_annotations(
            annotations=annotations,
            mapper=AnnotationClassMapper(
                class_mapping=ClassMappingConfig(
                    mapping=[],
                    model_classes=[
                        ClassMappingModelClassesConfig(class_id=0, class_name="person"),
                        ClassMappingModelClassesConfig(class_id=1, class_name="car"),
                    ],
                    number_model_classes=2,
                ),
                reduction_mapping=ReductionMappingConfig(
                    mapping=[
                        ReductionMappingMappingConfig(
                            model_class_ids=[0],
                            output_class_id=10,
                            output_class_name="human",
                        )
                    ]
                ),
            ),
        )

        # Check classifications
        assert reduced_annotations[0].classifications[0].class_id == 10
        assert reduced_annotations[0].classifications[0].class_name == "human"
        assert reduced_annotations[0].classifications[1].class_id == 1
        assert reduced_annotations[0].classifications[1].class_name == "car"

        # Check bounding boxes
        assert reduced_annotations[0].bounding_boxes[0].class_id == 10
        assert reduced_annotations[0].bounding_boxes[0].class_name == "human"
        assert reduced_annotations[0].bounding_boxes[1].class_id == 1
        assert reduced_annotations[0].bounding_boxes[1].class_name == "car"

        # Check segmentations
        assert reduced_annotations[0].segmentations[0].class_id == 10
        assert reduced_annotations[0].segmentations[0].class_name == "human"
        assert reduced_annotations[0].segmentations[1].class_id == 1
        assert reduced_annotations[0].segmentations[1].class_name == "car"


if __name__ == "__main__":
    main()
