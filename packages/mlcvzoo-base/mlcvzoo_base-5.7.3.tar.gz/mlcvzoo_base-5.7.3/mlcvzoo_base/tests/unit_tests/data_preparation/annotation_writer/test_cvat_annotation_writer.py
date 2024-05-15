# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

import hashlib
import logging
import os
import xml.etree.ElementTree as ET_xml
from unittest import main

from mlcvzoo_base.api.data.class_identifier import ClassIdentifier
from mlcvzoo_base.data_preparation.annotation_handler import AnnotationHandler
from mlcvzoo_base.data_preparation.annotation_writer.cvat_annotation_writer import (
    CVATAnnotationWriter,
)
from mlcvzoo_base.tests.unit_tests.test_template import TestTemplate

logger = logging.getLogger(__name__)


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


class TestCVATAnnotationWriter(TestTemplate):
    def test_write_to_cvat(self) -> None:
        logger.info(
            "############################################################\n"
            "# TEST parsing to cvat xml:\n"
            "#      test_parse_to_cvat(self)\n"
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

        # compare initial file wth new file
        initial_cvat_xml_path = annotation_handler.configuration.cvat_input_data[0].input_path

        annotations = annotation_handler.parse_annotations_from_cvat()

        output_file_path = os.path.join(self.project_root, "test_output", "test_cvat.xml")

        cvat_annotation_writer = CVATAnnotationWriter(
            cvat_xml_input_path=initial_cvat_xml_path,
            clean_boxes=False,
            clean_segmentations=False,
            clean_tags=False,
            output_file_path=output_file_path,
        )

        cvat_annotation_writer.write(
            annotations=annotations,
        )

        # TODO: adjust equality test, what about undefined handling of attributes
        #  (eg difficult false)
        assert _xml_equal(xml_path_1=initial_cvat_xml_path, xml_path_2=output_file_path)

    def test_clean_write_to_cvat(self) -> None:
        logger.info(
            "############################################################\n"
            "# TEST clean parsing to cvat xml:\n"
            "#      test_parse_to_cvat(self)\n"
            "############################################################"
        )
        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_AnnotationHandler",
            "annotation-handler_cvat_write_test.yaml",
        )

        annotation_handler = AnnotationHandler(
            yaml_config_path=yaml_config_path,
            string_replacement_map=self.string_replacement_map,
        )

        # create new dummy annotations per known annotations
        annotations = annotation_handler.parse_annotations_from_cvat()

        from mlcvzoo_base.api.data.classification import Classification

        test_class_identifier = ClassIdentifier(
            class_id=0,
            class_name="test_class",
        )
        test_classifications = [
            Classification(
                class_identifier=test_class_identifier,
                model_class_identifier=test_class_identifier,
                score=1.0,
            )
        ]
        for annotation in annotations:
            annotation.bounding_boxes = []
            annotation.segmentations = []
            annotation.classifications = test_classifications

        output_file_path = os.path.join(self.project_root, "test_output", "test_clean_cvat.xml")

        cvat_annotation_writer = CVATAnnotationWriter(
            cvat_xml_input_path=annotation_handler.configuration.cvat_input_data[0].input_path,
            clean_boxes=True,
            clean_segmentations=True,
            clean_tags=True,
            output_file_path=output_file_path,
        )

        cvat_annotation_writer.write(
            annotations=annotations,
        )

        # compare initial file wth new file
        clean_cvat_xml_path = os.path.join(
            self.project_root,
            "test_data/annotations/cvat/test-cvat-write-annotations_expected.xml",
        )

        assert _xml_equal(xml_path_1=output_file_path, xml_path_2=clean_cvat_xml_path)


if __name__ == "__main__":
    main()
