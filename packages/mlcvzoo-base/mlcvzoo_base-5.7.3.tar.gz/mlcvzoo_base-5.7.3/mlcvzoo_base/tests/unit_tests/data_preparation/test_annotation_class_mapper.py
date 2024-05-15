# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

import logging
import os
from typing import cast
from unittest import main

from config_builder import ConfigBuilder

from mlcvzoo_base.api.data.annotation_class_mapper import (
    AnnotationClassMapper,
    DuplicateOutputClassError,
)
from mlcvzoo_base.api.data.class_identifier import ClassIdentifier
from mlcvzoo_base.api.exceptions import ClassMappingNotFoundError, ForbiddenClassError
from mlcvzoo_base.configuration.class_mapping_config import ClassMappingConfig
from mlcvzoo_base.configuration.reduction_mapping_config import ReductionMappingConfig
from mlcvzoo_base.tests.unit_tests.test_template import TestTemplate

logger = logging.getLogger(__name__)


class TestAnnotationClassMapper(TestTemplate):
    def test_annotation_class_mapper_constructor(self) -> None:
        class_mapping_config: ClassMappingConfig = cast(
            ClassMappingConfig,
            ConfigBuilder(
                class_type=ClassMappingConfig,
                yaml_config_path=os.path.join(
                    self.project_root,
                    "test_data/test_annotation_class_mapper",
                    "test_constructor__class-mapping.yaml",
                ),
                string_replacement_map=self.string_replacement_map,
            ).configuration,
        )

        reduction_mapping: ReductionMappingConfig = cast(
            ReductionMappingConfig,
            ConfigBuilder(
                class_type=ReductionMappingConfig,
                yaml_config_path=os.path.join(
                    self.project_root,
                    "test_data/test_annotation_class_mapper",
                    "test_constructor__reduction-mapping.yaml",
                ),
                string_replacement_map=self.string_replacement_map,
            ).configuration,
        )

        mapper: AnnotationClassMapper = AnnotationClassMapper(
            class_mapping=class_mapping_config, reduction_mapping=reduction_mapping
        )

        assert mapper._AnnotationClassMapper__annotation_class_id_to_model_class_name_map == {
            0: "person",
            1: "truck",
            2: "car",
            3: "lion",
            4: "banana",
            5: "cherry",
            6: "unknown_6",
            7: "unknown_7",
            8: "unknown_8",
            9: "unknown_9",
        }

        assert mapper._AnnotationClassMapper__annotation_class_name_to_model_class_id_map == {
            "person": 0,
            "truck": 1,
            "car": 2,
            "lion": 3,
            "banana": 4,
            "cherry": 5,
            "unknown_6": 6,
            "unknown_7": 7,
            "unknown_8": 8,
            "unknown_9": 9,
        }

        assert mapper._AnnotationClassMapper__annotation_class_name_to_model_class_name_map == {
            "person": "person",
            "truck": "truck",
            "car": "car",
            "lion": "lion",
            "banana": "banana",
            "cherry": "cherry",
            "Person": "person",
            "LKW": "truck",
            "PKW": "car",
        }

        assert mapper._AnnotationClassMapper__model_class_id_to_class_identifier_map == {
            0: [ClassIdentifier(class_id=0, class_name="person")],
            1: [ClassIdentifier(class_id=1, class_name="vehicle")],
            2: [ClassIdentifier(class_id=1, class_name="vehicle")],
            3: [
                ClassIdentifier(class_id=15, class_name="animal"),
                ClassIdentifier(class_id=16, class_name="cat"),
            ],
            4: [ClassIdentifier(class_id=10, class_name="fruit")],
            5: [ClassIdentifier(class_id=10, class_name="fruit")],
            6: [ClassIdentifier(class_id=6, class_name="unknown_6")],
            7: [ClassIdentifier(class_id=7, class_name="unknown_7")],
            8: [ClassIdentifier(class_id=8, class_name="unknown_8")],
            9: [ClassIdentifier(class_id=9, class_name="unknown_9")],
        }

        assert mapper._AnnotationClassMapper__model_class_name_to_class_identifier_map == {
            "banana": [ClassIdentifier(class_id=10, class_name="fruit")],
            "car": [ClassIdentifier(class_id=1, class_name="vehicle")],
            "cherry": [ClassIdentifier(class_id=10, class_name="fruit")],
            "lion": [
                ClassIdentifier(class_id=15, class_name="animal"),
                ClassIdentifier(class_id=16, class_name="cat"),
            ],
            "person": [ClassIdentifier(class_id=0, class_name="person")],
            "truck": [ClassIdentifier(class_id=1, class_name="vehicle")],
            "unknown_6": [ClassIdentifier(class_id=6, class_name="unknown_6")],
            "unknown_7": [ClassIdentifier(class_id=7, class_name="unknown_7")],
            "unknown_8": [ClassIdentifier(class_id=8, class_name="unknown_8")],
            "unknown_9": [ClassIdentifier(class_id=9, class_name="unknown_9")],
        }

        assert mapper.get_model_class_names() == [
            "person",
            "truck",
            "car",
            "lion",
            "banana",
            "cherry",
            "unknown_6",
            "unknown_7",
            "unknown_8",
            "unknown_9",
        ]

        assert mapper.map_annotation_class_name_to_model_class_name("PKW") == "car"

        with self.assertRaises(ForbiddenClassError):
            mapper.map_annotation_class_name_to_model_class_name("cherry")

        with self.assertRaises(ClassMappingNotFoundError):
            mapper.map_annotation_class_name_to_model_class_name("Auto")

        assert mapper.map_annotation_class_name_to_model_class_id("person") == 0

        with self.assertRaises(ClassMappingNotFoundError):
            mapper.map_annotation_class_name_to_model_class_id("Auto")

        assert mapper.map_annotation_class_id_to_model_class_name(0) == "person"
        with self.assertRaises(ClassMappingNotFoundError):
            mapper.map_annotation_class_id_to_model_class_name(10)

        assert mapper.map_model_class_id_to_output_class_identifier(3)[0].class_id == 15
        assert mapper.map_model_class_id_to_output_class_identifier(3)[0].class_name == "animal"

        assert mapper.map_model_class_id_to_output_class_identifier(3)[1].class_id == 16
        assert mapper.map_model_class_id_to_output_class_identifier(3)[1].class_name == "cat"

        with self.assertRaises(ClassMappingNotFoundError):
            mapper.map_model_class_id_to_output_class_identifier(11)

        assert mapper.map_model_class_name_to_output_class_identifier("lion")[0].class_id == 15
        assert (
            mapper.map_model_class_name_to_output_class_identifier("lion")[0].class_name
            == "animal"
        )

        assert mapper.map_model_class_name_to_output_class_identifier("lion")[1].class_id == 16
        assert (
            mapper.map_model_class_name_to_output_class_identifier("lion")[1].class_name == "cat"
        )

        with self.assertRaises(ClassMappingNotFoundError):
            mapper.map_model_class_name_to_output_class_identifier("Auto")

        assert mapper.num_classes == 10

        logger.info("Successfully run test_annotation_class_mapper_constructor")

    def test_annotation_class_mapper_constructor_no_reduction_mapping(self) -> None:
        class_mapping_config: ClassMappingConfig = cast(
            ClassMappingConfig,
            ConfigBuilder(
                class_type=ClassMappingConfig,
                yaml_config_path=os.path.join(
                    self.project_root,
                    "test_data/test_annotation_class_mapper",
                    "test_constructor__class-mapping.yaml",
                ),
                string_replacement_map=self.string_replacement_map,
            ).configuration,
        )

        mapper: AnnotationClassMapper = AnnotationClassMapper(
            class_mapping=class_mapping_config, reduction_mapping=None
        )

        assert mapper._AnnotationClassMapper__annotation_class_id_to_model_class_name_map == {
            0: "person",
            1: "truck",
            2: "car",
            3: "lion",
            4: "banana",
            5: "cherry",
            6: "unknown_6",
            7: "unknown_7",
            8: "unknown_8",
            9: "unknown_9",
        }

        assert mapper._AnnotationClassMapper__annotation_class_name_to_model_class_id_map == {
            "person": 0,
            "truck": 1,
            "car": 2,
            "lion": 3,
            "banana": 4,
            "cherry": 5,
            "unknown_6": 6,
            "unknown_7": 7,
            "unknown_8": 8,
            "unknown_9": 9,
        }

        assert mapper._AnnotationClassMapper__annotation_class_name_to_model_class_name_map == {
            "person": "person",
            "truck": "truck",
            "car": "car",
            "lion": "lion",
            "banana": "banana",
            "cherry": "cherry",
            "Person": "person",
            "LKW": "truck",
            "PKW": "car",
        }

        assert mapper._AnnotationClassMapper__model_class_id_to_class_identifier_map == {
            0: [ClassIdentifier(class_id=0, class_name="person")],
            1: [ClassIdentifier(class_id=1, class_name="truck")],
            2: [ClassIdentifier(class_id=2, class_name="car")],
            3: [ClassIdentifier(class_id=3, class_name="lion")],
            4: [ClassIdentifier(class_id=4, class_name="banana")],
            5: [ClassIdentifier(class_id=5, class_name="cherry")],
            6: [ClassIdentifier(class_id=6, class_name="unknown_6")],
            7: [ClassIdentifier(class_id=7, class_name="unknown_7")],
            8: [ClassIdentifier(class_id=8, class_name="unknown_8")],
            9: [ClassIdentifier(class_id=9, class_name="unknown_9")],
        }

        assert mapper._AnnotationClassMapper__model_class_name_to_class_identifier_map == {
            "person": [ClassIdentifier(class_id=0, class_name="person")],
            "truck": [ClassIdentifier(class_id=1, class_name="truck")],
            "car": [ClassIdentifier(class_id=2, class_name="car")],
            "lion": [ClassIdentifier(class_id=3, class_name="lion")],
            "banana": [ClassIdentifier(class_id=4, class_name="banana")],
            "cherry": [ClassIdentifier(class_id=5, class_name="cherry")],
            "unknown_6": [ClassIdentifier(class_id=6, class_name="unknown_6")],
            "unknown_7": [ClassIdentifier(class_id=7, class_name="unknown_7")],
            "unknown_8": [ClassIdentifier(class_id=8, class_name="unknown_8")],
            "unknown_9": [ClassIdentifier(class_id=9, class_name="unknown_9")],
        }

        logger.info("Successfully run test_annotation_class_mapper_constructor")

    def test_annotation_class_mapper_annotation_class_not_in_model_classes_error(
        self,
    ) -> None:
        class_mapping_config: ClassMappingConfig = cast(
            ClassMappingConfig,
            ConfigBuilder(
                class_type=ClassMappingConfig,
                yaml_config_path=os.path.join(
                    self.project_root,
                    "test_data/test_annotation_class_mapper",
                    "test_annotation_class_not_in_model_classes_error__class-mapping.yaml",
                ),
                string_replacement_map=self.string_replacement_map,
            ).configuration,
        )

        value_error_message = ""

        try:
            AnnotationClassMapper(class_mapping=class_mapping_config, reduction_mapping=None)
        except ValueError as ve:
            value_error_message = str(ve)

        assert (
            value_error_message == "Invalid mapping config entry: "
            "mapping[4].output_class_name='vehicle', but has to be one of "
            "'['person', 'truck', 'car', 'lion', 'banana', 'cherry']'"
        )

    def test_annotation_class_mapper_class_id_out_of_range_error(
        self,
    ) -> None:
        class_mapping_config: ClassMappingConfig = cast(
            ClassMappingConfig,
            ConfigBuilder(
                class_type=ClassMappingConfig,
                yaml_config_path=os.path.join(
                    self.project_root,
                    "test_data/test_annotation_class_mapper",
                    "test_class_id_out_of_range_error__class-mapping.yaml",
                ),
                string_replacement_map=self.string_replacement_map,
            ).configuration,
        )

        value_error_message = ""

        try:
            AnnotationClassMapper(class_mapping=class_mapping_config, reduction_mapping=None)
        except ValueError as ve:
            value_error_message = str(ve)

        assert value_error_message == "Found class_ids='[11]' that exceed the number_classes=10"

    def test_annotation_class_mapper_duplicate_model_class_id_error(
        self,
    ) -> None:
        class_mapping_config: ClassMappingConfig = cast(
            ClassMappingConfig,
            ConfigBuilder(
                class_type=ClassMappingConfig,
                yaml_config_path=os.path.join(
                    self.project_root,
                    "test_data/test_annotation_class_mapper",
                    "test_duplicate_model_class_id_error__class-mapping.yaml",
                ),
                string_replacement_map=self.string_replacement_map,
            ).configuration,
        )

        value_error_message = ""

        try:
            AnnotationClassMapper(class_mapping=class_mapping_config, reduction_mapping=None)
        except ValueError as ve:
            value_error_message = str(ve)

        assert value_error_message == "Duplicate class_id='0' is not allowed in model_classes"

    def test_annotation_class_mapper_duplicate_output_class_id_error(self) -> None:
        class_mapping_config: ClassMappingConfig = cast(
            ClassMappingConfig,
            ConfigBuilder(
                class_type=ClassMappingConfig,
                yaml_config_path=os.path.join(
                    self.project_root,
                    "test_data/test_annotation_class_mapper",
                    "test_constructor__class-mapping.yaml",
                ),
                string_replacement_map=self.string_replacement_map,
            ).configuration,
        )

        reduction_mapping: ReductionMappingConfig = cast(
            ReductionMappingConfig,
            ConfigBuilder(
                class_type=ReductionMappingConfig,
                yaml_config_path=os.path.join(
                    self.project_root,
                    "test_data/test_annotation_class_mapper",
                    "test_duplicate_output_class_id_error__reduction-mapping.yaml",
                ),
                string_replacement_map=self.string_replacement_map,
            ).configuration,
        )

        with self.assertRaises(DuplicateOutputClassError):
            AnnotationClassMapper(
                class_mapping=class_mapping_config, reduction_mapping=reduction_mapping
            )

        logger.info(
            "Successfully run test_annotation_class_mapper_duplicate_output_class_id_error"
        )

    def test_annotation_class_mapper_duplicate_output_class_name_error(self) -> None:
        class_mapping_config: ClassMappingConfig = cast(
            ClassMappingConfig,
            ConfigBuilder(
                class_type=ClassMappingConfig,
                yaml_config_path=os.path.join(
                    self.project_root,
                    "test_data/test_annotation_class_mapper",
                    "test_constructor__class-mapping.yaml",
                ),
                string_replacement_map=self.string_replacement_map,
            ).configuration,
        )

        reduction_mapping: ReductionMappingConfig = cast(
            ReductionMappingConfig,
            ConfigBuilder(
                class_type=ReductionMappingConfig,
                yaml_config_path=os.path.join(
                    self.project_root,
                    "test_data/test_annotation_class_mapper",
                    "test_duplicate_output_class_name_error__reduction-mapping.yaml",
                ),
                string_replacement_map=self.string_replacement_map,
            ).configuration,
        )

        value_error_message = ""

        with self.assertRaises(DuplicateOutputClassError):
            AnnotationClassMapper(
                class_mapping=class_mapping_config, reduction_mapping=reduction_mapping
            )

        logger.info(
            "Successfully run test_annotation_class_mapper_duplicate_output_class_name_error"
        )

    def test_annotation_class_model_class_name_not_in_model_classes_error(self) -> None:
        class_mapping_config: ClassMappingConfig = cast(
            ClassMappingConfig,
            ConfigBuilder(
                class_type=ClassMappingConfig,
                yaml_config_path=os.path.join(
                    self.project_root,
                    "test_data/test_annotation_class_mapper",
                    "test_constructor__class-mapping.yaml",
                ),
                string_replacement_map=self.string_replacement_map,
            ).configuration,
        )

        reduction_mapping: ReductionMappingConfig = cast(
            ReductionMappingConfig,
            ConfigBuilder(
                class_type=ReductionMappingConfig,
                yaml_config_path=os.path.join(
                    self.project_root,
                    "test_data/test_annotation_class_mapper",
                    "test_model_class_name_not_in_model_classes_error__reduction-mapping.yaml",
                ),
                string_replacement_map=self.string_replacement_map,
            ).configuration,
        )

        value_error_message = ""

        try:
            AnnotationClassMapper(
                class_mapping=class_mapping_config, reduction_mapping=reduction_mapping
            )
        except ValueError as ve:
            value_error_message = str(ve)

        assert (
            value_error_message == "Invalid reduction-mapping config entry:\n"
            " - mapping[0].model_class_names='['apple']'\n"
            " - it can only contain values of: "
            "'['person', 'truck', 'car', 'lion', 'banana', 'cherry', "
            "'unknown_6', 'unknown_7', 'unknown_8', 'unknown_9']'\n"
            " - wrong model_class_names: '['apple']'"
        )

        logger.info(
            "Successfully run test_annotation_class_model_class_name_not_in_model_classes_error"
        )

    def test_annotation_class_model_class_id_not_in_model_classes_error(self) -> None:
        class_mapping_config: ClassMappingConfig = cast(
            ClassMappingConfig,
            ConfigBuilder(
                class_type=ClassMappingConfig,
                yaml_config_path=os.path.join(
                    self.project_root,
                    "test_data/test_annotation_class_mapper",
                    "test_constructor__class-mapping.yaml",
                ),
                string_replacement_map=self.string_replacement_map,
            ).configuration,
        )

        reduction_mapping: ReductionMappingConfig = cast(
            ReductionMappingConfig,
            ConfigBuilder(
                class_type=ReductionMappingConfig,
                yaml_config_path=os.path.join(
                    self.project_root,
                    "test_data/test_annotation_class_mapper",
                    "test_model_class_id_not_in_model_classes_error__reduction-mapping.yaml",
                ),
                string_replacement_map=self.string_replacement_map,
            ).configuration,
        )

        value_error_message = ""

        try:
            AnnotationClassMapper(
                class_mapping=class_mapping_config, reduction_mapping=reduction_mapping
            )
        except ValueError as ve:
            value_error_message = str(ve)

        assert (
            value_error_message == "Invalid reduction-mapping config entry:\n"
            " - mapping[0].model_class_ids='[11]'\n"
            " - it can only contain values of: "
            "'[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]'\n"
            " - wrong model_class_ids: '[11]'"
        )

        logger.info(
            "Successfully run test_annotation_class_model_class_name_not_in_model_classes_error"
        )


if __name__ == "__main__":
    main()
