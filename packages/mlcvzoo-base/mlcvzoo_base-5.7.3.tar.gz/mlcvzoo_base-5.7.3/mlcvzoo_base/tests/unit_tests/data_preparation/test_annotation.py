import copy
import logging
import os
from typing import List
from unittest import main

from mlcvzoo_base.api.data.annotation import BaseAnnotation
from mlcvzoo_base.api.data.bounding_box import BoundingBox
from mlcvzoo_base.api.data.box import Box
from mlcvzoo_base.api.data.class_identifier import ClassIdentifier
from mlcvzoo_base.api.data.classification import Classification
from mlcvzoo_base.api.data.segmentation import Segmentation
from mlcvzoo_base.data_preparation.utils import annotation_to_xml, filter_annotations
from mlcvzoo_base.tests.unit_tests.data_preparation.test_AnnotationHandler import (
    _xml_equal,
)
from mlcvzoo_base.tests.unit_tests.test_template import TestTemplate

logger = logging.getLogger(__name__)


class TestAnnotation(TestTemplate):
    def __init_annotation_list(self) -> List[BaseAnnotation]:
        score_list = [0.6, 0.7, 0.8, 0.9]

        annotations: List[BaseAnnotation] = [
            BaseAnnotation(
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
            for score in score_list
        ]

        return annotations

    def test_annotation_filter_classifications(self) -> None:
        logger.info(
            "############################################################\n"
            "# TEST filtering of classifications of annotations by score:\n"
            "#      test_annotation_filter_classifications(self)\n"
            "############################################################"
        )

        annotations = self.__init_annotation_list()

        filtered_annotations = filter_annotations(
            annotations=annotations,
            classification_score=0.9,
        )

        expected_annotations = copy.deepcopy(annotations)

        expected_annotations[0].classifications = []
        expected_annotations[1].classifications = []
        expected_annotations[2].classifications = []

        for filtered_annotation, expected_annotation in zip(
            filtered_annotations, expected_annotations
        ):
            assert filtered_annotation == expected_annotation

    def test_annotation_filter_bounding_boxes(self) -> None:
        logger.info(
            "############################################################\n"
            "# TEST filtering of bounding boxes of annotations by score:\n"
            "#      test_annotation_filter_bounding_boxes(self)\n"
            "############################################################"
        )

        annotations = self.__init_annotation_list()

        filtered_annotations = filter_annotations(
            annotations=annotations,
            bounding_box_score=0.8,
        )

        expected_annotations = copy.deepcopy(annotations)

        expected_annotations[0].bounding_boxes = []
        expected_annotations[1].bounding_boxes = []

        for filtered_annotation, expected_annotation in zip(
            filtered_annotations, expected_annotations
        ):
            assert filtered_annotation == expected_annotation

    def test_annotation_filter_segmentations(self) -> None:
        logger.info(
            "############################################################\n"
            "# TEST filtering of segmentations of annotations by score:\n"
            "#      test_annotation_filter_segmentations(self)\n"
            "############################################################"
        )

        annotations = self.__init_annotation_list()

        filtered_annotations = filter_annotations(
            annotations=annotations,
            segmentation_score=0.7,
        )

        expected_annotations = copy.deepcopy(annotations)

        expected_annotations[0].segmentations = []

        for filtered_annotation, expected_annotation in zip(
            filtered_annotations, expected_annotations
        ):
            assert filtered_annotation == expected_annotation

    def test_annotation_filter_class_ids(self) -> None:
        logger.info(
            "############################################################\n"
            "# TEST filtering of class ids of any datastructure of an annotation:\n"
            "#      test_annotation_filter_class_ids(self)\n"
            "############################################################"
        )

        annotations = self.__init_annotation_list()

        filtered_annotations = filter_annotations(annotations=annotations, class_ids=[0])

        expected_annotations = copy.deepcopy(annotations)

        expected_annotations[0].classifications.pop(1)
        expected_annotations[0].bounding_boxes.pop(1)
        expected_annotations[0].segmentations.pop(1)

        expected_annotations[1].classifications.pop(1)
        expected_annotations[1].bounding_boxes.pop(1)
        expected_annotations[1].segmentations.pop(1)

        expected_annotations[2].classifications.pop(1)
        expected_annotations[2].bounding_boxes.pop(1)
        expected_annotations[2].segmentations.pop(1)

        expected_annotations[3].classifications.pop(1)
        expected_annotations[3].bounding_boxes.pop(1)
        expected_annotations[3].segmentations.pop(1)

        for filtered_annotation, expected_annotation in zip(
            filtered_annotations, expected_annotations
        ):
            assert filtered_annotation == expected_annotation

    def test_annotation_filter_class_names(self) -> None:
        logger.info(
            "############################################################\n"
            "# TEST filtering of class names of any datastructure of an annotation:\n"
            "#      test_annotation_filter_class_names(self)\n"
            "############################################################"
        )

        annotations = self.__init_annotation_list()

        filtered_annotations = filter_annotations(annotations=annotations, class_names=["test-2"])

        expected_annotations = copy.deepcopy(annotations)

        expected_annotations[0].classifications.pop(0)
        expected_annotations[0].bounding_boxes = []
        expected_annotations[0].segmentations = []

        expected_annotations[1].classifications.pop(0)
        expected_annotations[1].bounding_boxes = []
        expected_annotations[1].segmentations = []

        expected_annotations[2].classifications.pop(0)
        expected_annotations[2].bounding_boxes = []
        expected_annotations[2].segmentations = []

        expected_annotations[3].classifications.pop(0)
        expected_annotations[3].bounding_boxes = []
        expected_annotations[3].segmentations = []

        for filtered_annotation, expected_annotation in zip(
            filtered_annotations, expected_annotations
        ):
            assert filtered_annotation == expected_annotation

    def test_annotation_classification_equal(self) -> None:
        annotation_1 = BaseAnnotation(
            image_path=os.path.join(
                self.project_root,
                "test_data/images/dummy_taskcars.jpg",
            ),
            classifications=[
                Classification(
                    class_identifier=ClassIdentifier(
                        class_id=0,
                        class_name="test",
                    ),
                    score=0.7,
                ),
                Classification(
                    class_identifier=ClassIdentifier(
                        class_id=0,
                        class_name="test",
                    ),
                    score=0.7,
                ),
            ],
            annotation_path="",
            image_shape=(1, 1),
            image_dir="",
            annotation_dir="",
            replacement_string="",
        )

        annotation_2 = BaseAnnotation(
            image_path=os.path.join(
                self.project_root,
                "test_data/images/dummy_taskcars.jpg",
            ),
            classifications=[
                Classification(
                    class_identifier=ClassIdentifier(
                        class_id=0,
                        class_name="test",
                    ),
                    score=0.7,
                ),
                Classification(
                    class_identifier=ClassIdentifier(
                        class_id=0,
                        class_name="test",
                    ),
                    score=0.7,
                ),
            ],
            annotation_path="",
            image_shape=(1, 1),
            image_dir="",
            annotation_dir="",
            replacement_string="",
        )

        assert annotation_1 == annotation_2

    def test_annotation_classification_not_equal(self) -> None:
        annotation_1 = BaseAnnotation(
            image_path=os.path.join(
                self.project_root,
                "test_data/images/dummy_taskcars.jpg",
            ),
            classifications=[
                Classification(
                    class_identifier=ClassIdentifier(
                        class_id=0,
                        class_name="test",
                    ),
                    score=0.7,
                ),
                Classification(
                    class_identifier=ClassIdentifier(
                        class_id=0,
                        class_name="test",
                    ),
                    score=0.7,
                ),
            ],
            annotation_path="",
            image_shape=(1, 1),
            image_dir="",
            annotation_dir="",
            replacement_string="",
        )

        annotation_2 = BaseAnnotation(
            image_path=os.path.join(
                self.project_root,
                "test_data/images/dummy_taskcars.jpg",
            ),
            classifications=[
                Classification(
                    class_identifier=ClassIdentifier(
                        class_id=0,
                        class_name="test",
                    ),
                    score=0.7,
                ),
                Classification(
                    class_identifier=ClassIdentifier(
                        class_id=0,
                        class_name="test-2",
                    ),
                    score=0.7,
                ),
            ],
            annotation_path="",
            image_shape=(1, 1),
            image_dir="",
            annotation_dir="",
            replacement_string="",
        )

        annotation_3 = BaseAnnotation(
            image_path=os.path.join(
                self.project_root,
                "test_data/images/dummy_taskcars.jpg",
            ),
            classifications=[
                Classification(
                    class_identifier=ClassIdentifier(
                        class_id=0,
                        class_name="test",
                    ),
                    score=0.7,
                )
            ],
            annotation_path="",
            image_shape=(1, 1),
            image_dir="",
            annotation_dir="",
            replacement_string="",
        )

        assert annotation_1 != annotation_2
        assert annotation_1 != annotation_3

    def test_bounding_box_equal(self) -> None:
        annotation_1 = BaseAnnotation(
            image_path=os.path.join(
                self.project_root,
                "test_data/images/dummy_taskcars.jpg",
            ),
            bounding_boxes=[
                BoundingBox(
                    box=Box(xmin=0, ymin=0, xmax=100, ymax=100),
                    class_identifier=ClassIdentifier(
                        class_id=0,
                        class_name="test",
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
                        class_name="test-1",
                    ),
                    score=0.7,
                    difficult=False,
                    occluded=False,
                    background=False,
                    content="",
                ),
            ],
            annotation_path="",
            image_shape=(1, 1),
            image_dir="",
            annotation_dir="",
            replacement_string="",
        )

        annotation_2 = BaseAnnotation(
            image_path=os.path.join(
                self.project_root,
                "test_data/images/dummy_taskcars.jpg",
            ),
            bounding_boxes=[
                BoundingBox(
                    box=Box(xmin=0, ymin=0, xmax=100, ymax=100),
                    class_identifier=ClassIdentifier(
                        class_id=0,
                        class_name="test",
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
                        class_name="test-1",
                    ),
                    score=0.7,
                    difficult=False,
                    occluded=False,
                    background=False,
                    content="",
                ),
            ],
            annotation_path="",
            image_shape=(1, 1),
            image_dir="",
            annotation_dir="",
            replacement_string="",
        )

        assert annotation_1 == annotation_2

    def test_bounding_box_not_equal(self) -> None:
        annotation_1 = BaseAnnotation(
            image_path=os.path.join(
                self.project_root,
                "test_data/images/dummy_taskcars.jpg",
            ),
            bounding_boxes=[
                BoundingBox(
                    box=Box(xmin=0, ymin=0, xmax=100, ymax=100),
                    class_identifier=ClassIdentifier(
                        class_id=0,
                        class_name="test",
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
                        class_name="test-1",
                    ),
                    score=0.7,
                    difficult=False,
                    occluded=False,
                    background=False,
                    content="",
                ),
            ],
            annotation_path="",
            image_shape=(1, 1),
            image_dir="",
            annotation_dir="",
            replacement_string="",
        )

        annotation_2 = BaseAnnotation(
            image_path=os.path.join(
                self.project_root,
                "test_data/images/dummy_taskcars.jpg",
            ),
            bounding_boxes=[
                BoundingBox(
                    box=Box(xmin=0, ymin=0, xmax=1, ymax=100),
                    class_identifier=ClassIdentifier(
                        class_id=0,
                        class_name="test",
                    ),
                    score=0.7,
                    difficult=False,
                    occluded=False,
                    background=False,
                    content="",
                ),
            ],
            annotation_path="",
            image_shape=(1, 1),
            image_dir="",
            annotation_dir="",
            replacement_string="",
        )

        annotation_3 = BaseAnnotation(
            image_path=os.path.join(
                self.project_root,
                "test_data/images/dummy_taskcars.jpg",
            ),
            bounding_boxes=[
                BoundingBox(
                    box=Box(xmin=0, ymin=0, xmax=100, ymax=100),
                    class_identifier=ClassIdentifier(
                        class_id=0,
                        class_name="test",
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
                        class_name="test-1",
                    ),
                    score=0.8,
                    difficult=False,
                    occluded=False,
                    background=False,
                    content="",
                ),
            ],
            annotation_path="",
            image_shape=(1, 1),
            image_dir="",
            annotation_dir="",
            replacement_string="",
        )

        annotation_4 = BaseAnnotation(
            image_path=os.path.join(
                self.project_root,
                "test_data/images/dummy_taskcars.jpg",
            ),
            bounding_boxes=[
                BoundingBox(
                    box=Box(xmin=0, ymin=0, xmax=100, ymax=100),
                    class_identifier=ClassIdentifier(
                        class_id=0,
                        class_name="test",
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
                        class_name="test",
                    ),
                    score=0.7,
                    difficult=False,
                    occluded=False,
                    background=False,
                    content="",
                ),
            ],
            annotation_path="",
            image_shape=(1, 1),
            image_dir="",
            annotation_dir="",
            replacement_string="",
        )

        assert annotation_1 != annotation_2
        assert annotation_1 != annotation_3
        assert annotation_1 != annotation_4

    def test_segmentation_equal(self) -> None:
        annotation_1 = BaseAnnotation(
            image_path=os.path.join(
                self.project_root,
                "test_data/images/dummy_taskcars.jpg",
            ),
            segmentations=[
                Segmentation(
                    polygon=[(0, 0), (100, 0), (100, 100), (0, 100)],
                    box=Box(xmin=0, ymin=0, xmax=100, ymax=100),
                    class_identifier=ClassIdentifier(
                        class_id=0,
                        class_name="test",
                    ),
                    score=0.7,
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
                    score=0.7,
                    difficult=False,
                    occluded=False,
                    background=False,
                    content="",
                ),
            ],
            annotation_path="",
            image_shape=(1, 1),
            image_dir="",
            annotation_dir="",
            replacement_string="",
        )

        annotation_2 = BaseAnnotation(
            image_path=os.path.join(
                self.project_root,
                "test_data/images/dummy_taskcars.jpg",
            ),
            segmentations=[
                Segmentation(
                    polygon=[(0, 0), (100, 0), (100, 100), (0, 100)],
                    box=Box(xmin=0, ymin=0, xmax=100, ymax=100),
                    class_identifier=ClassIdentifier(
                        class_id=0,
                        class_name="test",
                    ),
                    score=0.7,
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
                    score=0.7,
                    difficult=False,
                    occluded=False,
                    background=False,
                    content="",
                ),
            ],
            annotation_path="",
            image_shape=(1, 1),
            image_dir="",
            annotation_dir="",
            replacement_string="",
        )

        assert annotation_1 == annotation_2

    def test_segmentation_not_equal(self) -> None:
        annotation_1 = BaseAnnotation(
            image_path=os.path.join(
                self.project_root,
                "test_data/images/dummy_taskcars.jpg",
            ),
            segmentations=[
                Segmentation(
                    polygon=[(0, 0), (100, 0), (100, 100), (0, 100)],
                    box=Box(xmin=0, ymin=0, xmax=100, ymax=100),
                    class_identifier=ClassIdentifier(
                        class_id=0,
                        class_name="test",
                    ),
                    score=0.7,
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
                    score=0.7,
                    difficult=False,
                    occluded=False,
                    background=False,
                    content="",
                ),
            ],
            annotation_path="",
            image_shape=(1, 1),
            image_dir="",
            annotation_dir="",
            replacement_string="",
        )

        annotation_2 = BaseAnnotation(
            image_path=os.path.join(
                self.project_root,
                "test_data/images/dummy_taskcars.jpg",
            ),
            segmentations=[
                Segmentation(
                    polygon=[(0, 0), (100, 0), (100, 100), (0, 100)],
                    box=Box(xmin=0, ymin=0, xmax=100, ymax=100),
                    class_identifier=ClassIdentifier(
                        class_id=0,
                        class_name="test",
                    ),
                    score=0.7,
                    difficult=False,
                    occluded=False,
                    background=False,
                    content="",
                )
            ],
            annotation_path="",
            image_shape=(1, 1),
            image_dir="",
            annotation_dir="",
            replacement_string="",
        )

        annotation_3 = BaseAnnotation(
            image_path=os.path.join(
                self.project_root,
                "test_data/images/dummy_taskcars.jpg",
            ),
            segmentations=[
                Segmentation(
                    polygon=[(0, 0), (100, 0), (9, 100), (0, 100)],
                    box=Box(xmin=0, ymin=0, xmax=100, ymax=100),
                    class_identifier=ClassIdentifier(
                        class_id=0,
                        class_name="test",
                    ),
                    score=0.7,
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
                    score=0.7,
                    difficult=False,
                    occluded=False,
                    background=False,
                    content="",
                ),
            ],
            annotation_path="",
            image_shape=(1, 1),
            image_dir="",
            annotation_dir="",
            replacement_string="",
        )

        annotation_4 = BaseAnnotation(
            image_path=os.path.join(
                self.project_root,
                "test_data/images/dummy_taskcars.jpg",
            ),
            segmentations=[
                Segmentation(
                    polygon=[(0, 0), (100, 0), (100, 100), (0, 100)],
                    box=Box(xmin=0, ymin=0, xmax=100, ymax=100),
                    class_identifier=ClassIdentifier(
                        class_id=0,
                        class_name="test",
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
                        class_name="test-1",
                    ),
                    score=0.7,
                    difficult=False,
                    occluded=False,
                    background=False,
                    content="",
                ),
            ],
            annotation_path="",
            image_shape=(1, 1),
            image_dir="",
            annotation_dir="",
            replacement_string="",
        )

        assert annotation_1 != annotation_2
        assert annotation_1 != annotation_3
        assert annotation_1 != annotation_4

    def test_annotation_to_xml(self):
        annotation = BaseAnnotation(
            image_path="TEST_PATH/cars.xml",
            bounding_boxes=[
                BoundingBox(
                    box=Box(xmin=0, ymin=0, xmax=100, ymax=100),
                    class_identifier=ClassIdentifier(
                        class_id=0,
                        class_name="test",
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
                        class_name="test-1",
                    ),
                    score=0.8,
                    difficult=False,
                    occluded=False,
                    background=False,
                    content="",
                ),
            ],
            annotation_path=os.path.join(
                self.project_root,
                "test_output/data_preparation/cars.xml",
            ),
            image_shape=(1, 1),
            image_dir="",
            annotation_dir="",
            replacement_string="",
        )

        annotation_to_xml(annotation=annotation)

        wanted_xml_file_path = os.path.join(
            self.project_root,
            "test_data/test_AnnotationHandler/" "wanted_output_annotation.xml",
        )

        assert _xml_equal(xml_path_1=annotation.annotation_path, xml_path_2=wanted_xml_file_path)

    def test_classification_to_str(self):
        assert (
            (
                "%r"
                % Classification(
                    class_identifier=ClassIdentifier(
                        class_name="car",
                        class_id=0,
                    ),
                    score=0.1,
                )
            )
            == "Classification("
            "class-id=0, class-name=car: model-class-id=0, model-class-name=car: score=0.1"
            ")"
        )

    def test_box_to_str(self):
        assert (
            "%r" % Box(xmin=0, ymin=0, xmax=100, ymax=100)
        ) == "Box(xmin=0, ymin=0, xmax=100, ymax=100)"
        assert (
            "%s" % Box(xmin=0, ymin=0, xmax=100, ymax=100)
        ) == "Box(xmin=0, ymin=0, xmax=100, ymax=100)"

    def test_segmentation_to_str(self):
        assert (
            (
                "%r"
                % Segmentation(
                    polygon=[(0, 0), (100, 0), (100, 100), (0, 100)],
                    box=Box(xmin=0, ymin=0, xmax=100, ymax=100),
                    class_identifier=ClassIdentifier(
                        class_id=0,
                        class_name="test",
                    ),
                    score=1.0,
                    difficult=False,
                    occluded=False,
                    background=False,
                    content="test",
                )
            )
            == "Segmentation("
            "class-id=0, class-name=test: model-class-id=0, model-class-name=test: "
            "Box=Box(xmin=0, ymin=0, xmax=100, ymax=100), "
            "Polygon=[(0, 0), (100, 0), (100, 100), (0, 100)], "
            "score=1.0, difficult=False, occluded=False, background=False, content='test'"
            ")"
        )


if __name__ == "__main__":
    main()
