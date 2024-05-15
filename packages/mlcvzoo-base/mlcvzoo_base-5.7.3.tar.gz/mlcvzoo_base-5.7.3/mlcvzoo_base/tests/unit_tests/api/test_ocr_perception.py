# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

import logging
from typing import Any, Dict

from mlcvzoo_base.api.data.ocr_perception import OCRPerception
from mlcvzoo_base.tests.unit_tests.test_template import TestTemplate

logger = logging.getLogger(__name__)


class TestAPIOCRPerception(TestTemplate):
    @staticmethod
    def __create_dummy_perception() -> OCRPerception:
        return OCRPerception(
            words=["a", "b", "c"], word_scores=[0.1, 0.2, 0.3], content="test", score=0.4
        )

    def test_to_json(self) -> None:
        dummy_perception: OCRPerception = self.__create_dummy_perception()
        perception_json: Any = dummy_perception.to_json()
        expected_json: Dict = {
            "content": "test",
            "score": 0.4,
            "word_scores": [0.1, 0.2, 0.3],
            "words": ["a", "b", "c"],
        }
        assert perception_json == expected_json
