# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

import logging
import os
from typing import Dict
from unittest import main

from mlcvzoo_base.api.data.annotation import BaseAnnotation
from mlcvzoo_base.api.data.bounding_box import BoundingBox
from mlcvzoo_base.api.data.box import Box
from mlcvzoo_base.api.data.class_identifier import ClassIdentifier
from mlcvzoo_base.api.data.classification import Classification
from mlcvzoo_base.api.data.segmentation import Segmentation
from mlcvzoo_base.tests.unit_tests.test_template import TestTemplate

logger = logging.getLogger(__name__)


class TestAPIAnnotation(TestTemplate):
    def test_to_dict(self) -> None:
        score: int = 1
        dummy_annotation: BaseAnnotation = BaseAnnotation(
            image_path=os.path.join(
                self.project_root,
                "test_data/images/dummy_taskcars.jpg",
            ),
            annotation_path="",
            image_shape=(1, 1),
            classifications=[
                Classification(
                    class_identifier=ClassIdentifier(
                        class_id=0,
                        class_name="test",
                    ),
                    score=score,
                ),
                Classification(
                    class_identifier=ClassIdentifier(class_id=2, class_name="test-2"),
                    score=score,
                ),
            ],
            bounding_boxes=[
                BoundingBox(
                    box=Box(xmin=0, ymin=0, xmax=100, ymax=100),
                    class_identifier=ClassIdentifier(
                        class_id=0,
                        class_name="test",
                    ),
                    score=score,
                    difficult=False,
                    occluded=False,
                    background=False,
                    content="",
                ),
                BoundingBox(
                    box=Box(xmin=0, ymin=0, xmax=100, ymax=100),
                    class_identifier=ClassIdentifier(
                        class_id=1,
                        class_name="test-1",
                    ),
                    score=score,
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
                        class_name="test",
                    ),
                    score=score,
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
                        class_name="test-1",
                    ),
                    score=score,
                    difficult=False,
                    occluded=False,
                    background=False,
                    content="",
                ),
            ],
            image_dir="",
            annotation_dir="",
            replacement_string="" "",
        )

        expected_dict: Dict = {
            "image_path": os.path.join(
                self.project_root,
                "test_data/images/dummy_taskcars.jpg",
            ),
            "annotation_path": "",
            "image_shape": (1, 1),
            "classifications": [
                Classification(
                    class_identifier=ClassIdentifier(class_id=0, class_name="test"),
                    model_class_identifier=ClassIdentifier(class_id=0, class_name="test"),
                    score=1,
                ),
                Classification(
                    class_identifier=ClassIdentifier(class_id=2, class_name="test-2"),
                    model_class_identifier=ClassIdentifier(class_id=2, class_name="test-2"),
                    score=1,
                ),
            ],
            "bounding_boxes": [
                BoundingBox(
                    box=Box(xmin=0, ymin=0, xmax=100, ymax=100),
                    class_identifier=ClassIdentifier(
                        class_id=0,
                        class_name="test",
                    ),
                    model_class_identifier=ClassIdentifier(
                        class_id=0,
                        class_name="test",
                    ),
                    score=1,
                    difficult=False,
                    occluded=False,
                    background=False,
                    content="",
                ),
                BoundingBox(
                    box=Box(xmin=0, ymin=0, xmax=100, ymax=100),
                    class_identifier=ClassIdentifier(
                        class_id=1,
                        class_name="test-1",
                    ),
                    model_class_identifier=ClassIdentifier(
                        class_id=1,
                        class_name="test-1",
                    ),
                    score=1,
                    difficult=False,
                    occluded=False,
                    background=False,
                    content="",
                ),
            ],
            "segmentations": [
                Segmentation(
                    polygon=[(0, 0), (100, 0), (100, 100), (0, 100)],
                    box=Box(xmin=0, ymin=0, xmax=100, ymax=100),
                    class_identifier=ClassIdentifier(class_id=0, class_name="test"),
                    model_class_identifier=ClassIdentifier(class_id=0, class_name="test"),
                    score=1,
                    difficult=False,
                    occluded=False,
                    background=False,
                    content="",
                ),
                Segmentation(
                    polygon=[(0, 0), (100, 0), (100, 100), (0, 100)],
                    box=Box(xmin=0, ymin=0, xmax=100, ymax=100),
                    class_identifier=ClassIdentifier(class_id=1, class_name="test-1"),
                    model_class_identifier=ClassIdentifier(class_id=1, class_name="test-1"),
                    score=1,
                    difficult=False,
                    occluded=False,
                    background=False,
                    content="",
                ),
            ],
            "ocr_perception": None,
            "image_dir": "",
            "annotation_dir": "",
            "replacement_string": "",
        }

        assert dummy_annotation.to_dict() == expected_dict


if __name__ == "__main__":
    main()
