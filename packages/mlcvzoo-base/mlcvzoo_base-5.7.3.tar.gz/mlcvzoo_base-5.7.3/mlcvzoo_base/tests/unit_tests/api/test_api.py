# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

import copy
import logging
from unittest import main

from mlcvzoo_base.api.data.class_identifier import ClassIdentifier
from mlcvzoo_base.api.data.ocr_perception import OCRPerception
from mlcvzoo_base.tests.unit_tests.test_template import TestTemplate

logger = logging.getLogger(__name__)

# TODO: add test that surrounding box is written to csv files


class TestMLCVZooAPI(TestTemplate):
    def setUp(self) -> None:
        TestTemplate.setUp(self)

        self.test_ocr_perception_words = OCRPerception(
            words=["Hello", "World"], word_scores=[0.9, 0.8], content="", score=0.99
        )
        self.test_ocr_perception_content = OCRPerception(
            words=[], word_scores=[], content="Hello World", score=0.99
        )

    def test_ocr_perception_to_dict(self) -> None:
        test_ocr_perception_words = copy.deepcopy(self.test_ocr_perception_words)
        test_ocr_perception_words_dict = test_ocr_perception_words.to_dict()

        assert test_ocr_perception_words_dict["words"] == ["Hello", "World"]
        assert test_ocr_perception_words_dict["word_scores"] == [0.9, 0.8]
        assert test_ocr_perception_words_dict["content"] == "Hello World"
        assert test_ocr_perception_words_dict["score"] == 0.99

    def test_ocr_perception_from_dict(self) -> None:
        test_ocr_perception_words_dict = {}
        test_ocr_perception_words_dict["words"] = ["Hello", "World"]
        test_ocr_perception_words_dict["word_scores"] = [0.9, 0.8]
        test_ocr_perception_words_dict["content"] = "Hello World"
        test_ocr_perception_words_dict["score"] = 0.99

        test_ocr_perception_words = OCRPerception.from_dict(
            from_dict=test_ocr_perception_words_dict
        )

        assert test_ocr_perception_words.words == ["Hello", "World"]
        assert test_ocr_perception_words.word_scores == [0.9, 0.8]
        assert test_ocr_perception_words.content == "Hello World"
        assert test_ocr_perception_words.score == 0.99

    def test_class_identifier_from_str(self) -> None:
        class_identifier: ClassIdentifier = ClassIdentifier.from_str(class_identifier_str="0_Car")

        assert class_identifier.class_id == 0
        assert class_identifier.class_name == "Car"

        class_identifier = ClassIdentifier.from_str(class_identifier_str="1_Ignored_Class")

        assert class_identifier.class_id == 1
        assert class_identifier.class_name == "Ignored_Class"

    def test_class_identifier_from_str_no_delimiter_error(self) -> None:
        with self.assertRaises(ValueError):
            ClassIdentifier.from_str(class_identifier_str="Car")

    def test_class_identifier_from_str_no_class_id_info_error(self) -> None:
        with self.assertRaises(ValueError):
            ClassIdentifier.from_str(class_identifier_str="_Car")

    def test_class_identifier_from_str_no_class_name_info_error(self) -> None:
        with self.assertRaises(ValueError):
            ClassIdentifier.from_str(class_identifier_str="0_")


if __name__ == "__main__":
    main()
