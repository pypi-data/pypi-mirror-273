# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

import logging
import os
from typing import Optional, cast
from unittest import main

from mlcvzoo_base.configuration.model_config import ModelConfig
from mlcvzoo_base.models.model_registry import ModelRegistry
from mlcvzoo_base.models.read_from_file.model import (
    ReadFromFileClassificationModel,
    ReadFromFileObjectDetectionModel,
    ReadFromFileSegmentationModel,
)
from mlcvzoo_base.tests.unit_tests.test_template import TestTemplate

logger = logging.getLogger(__name__)


class TestModel:
    def __init__(
        self, from_yaml: Optional[str], test_int_parameter: int, test_bool_parameter: bool
    ):
        pass


class TestModel2:
    def __init__(
        self, from_yaml: Optional[str], test_int_parameter: int, test_bool_parameter: bool
    ):
        pass


class TestModelRegistry(TestTemplate):
    def test_determine_config_class(self) -> None:
        assert (
            ModelRegistry().determine_config_class_name(
                model_type_name="read_from_file_classification"
            )
            == "read_from_file_config"
        )
        assert (
            ModelRegistry().determine_config_class_name(
                model_type_name="read_from_file_object_detection"
            )
            == "read_from_file_config"
        )
        assert (
            ModelRegistry().determine_config_class_name(
                model_type_name="read_from_file_segmentation"
            )
            == "read_from_file_config"
        )
        assert (
            ModelRegistry().determine_config_class_name(model_type_name="yolox") == "yolox_config"
        )
        assert (
            ModelRegistry().determine_config_class_name(model_type_name="yolov4_darknet")
            == "darknet_config"
        )
        assert (
            ModelRegistry().determine_config_class_name(model_type_name="darknet_object_detection")
            == "darknet_config"
        )
        assert (
            ModelRegistry().determine_config_class_name(
                model_type_name="mmdetection_object_detection"
            )
            == "mmdet_config"
        )
        assert (
            ModelRegistry().determine_config_class_name(model_type_name="mmocr_text_detection")
            == "mmocr_config"
        )
        assert (
            ModelRegistry().determine_config_class_name(model_type_name="mmocr_text_recognition")
            == "mmocr_config"
        )
        assert (
            ModelRegistry().determine_config_class_name(
                model_type_name="tf_classification_custom_block"
            )
            == "tf_classification_custom_block_config"
        )
        assert (
            ModelRegistry().determine_config_class_name(
                model_type_name="tf_classification_xception"
            )
            == "tf_classification_xception_config"
        )

    def test_init_model_with_string_replacement_map(self) -> None:
        """
        Ensure that the init_model(...) method works when defining the
        string_replacement map in the model_config.constructor_parameters attribute

        Returns:
            None
        """

        model_registry = ModelRegistry()

        model_config: ModelConfig = ModelConfig(
            class_type="read_from_file_object_detection",
            constructor_parameters={
                "from_yaml": os.path.join(
                    self.project_root,
                    "test_data/test_ReadFromFileObjectDetectionModel/",
                    "read-from-file_coco_test.yaml",
                ),
                "string_replacement_map": self.string_replacement_map,
            },
        )

        read_from_file_model = cast(
            ReadFromFileObjectDetectionModel,
            model_registry.init_model(model_config=model_config),
        )

        assert read_from_file_model is not None

    def test_init_model_with_string_replacement_map_2(self) -> None:
        """
        Ensure that the init_model(...) method works by handing over a
        string_replacement map.

        Returns:
            None
        """
        model_registry = ModelRegistry()

        model_config: ModelConfig = ModelConfig(
            class_type="read_from_file_object_detection",
            constructor_parameters={
                "from_yaml": os.path.join(
                    self.project_root,
                    "test_data/test_ReadFromFileObjectDetectionModel/",
                    "read-from-file_coco_test.yaml",
                ),
            },
        )

        read_from_file_model = cast(
            ReadFromFileObjectDetectionModel,
            model_registry.init_model(
                model_config=model_config,
                string_replacement_map=self.string_replacement_map,
            ),
        )

        assert read_from_file_model is not None

    def test_init_model_without_string_replacement_map(self) -> None:
        """
        Ensure that the init_model(...) method works without handing over a
        string_replacement map.

        Returns:
            None
        """
        model_registry = ModelRegistry()

        __string_replacement_map_os_values = self.string_replacement_map.copy()

        # Set the os environment variables for this test cast
        for key, value in self.string_replacement_map.items():
            __string_replacement_map_os_values[key] = os.environ.get(key=key)

            os.environ.setdefault(key=key, value=value)
            os.environ[key] = value

        model_config: ModelConfig = ModelConfig(
            class_type="read_from_file_object_detection",
            constructor_parameters={
                "from_yaml": os.path.join(
                    self.project_root,
                    "test_data/test_ReadFromFileObjectDetectionModel/",
                    "read-from-file_coco_test.yaml",
                ),
            },
        )

        read_from_file_model = cast(
            ReadFromFileObjectDetectionModel,
            model_registry.init_model(model_config=model_config),
        )

        # Reset the values of the modified os environment variables to their original value
        for key, value in __string_replacement_map_os_values.items():
            if os.environ[key] is not None and value is not None:
                os.environ[key] = value

        assert read_from_file_model is not None

    def test_model_init_wrong_constructor_parameter(self) -> None:
        with self.assertRaises(TypeError):
            ModelRegistry().init_model(
                model_config=ModelConfig(
                    class_type="read_from_file_object_detection",
                    constructor_parameters={
                        "from_yaml": os.path.join(
                            self.project_root,
                            "test_data/test_ReadFromFileObjectDetectionModel/"
                            "read-from-file_pascal-voc_test.yaml",
                        ),
                        "wrong_parameter": 10,
                    },
                )
            )

    def test_model_init_not_registered(self) -> None:
        with self.assertRaises(ValueError):
            ModelRegistry().init_model(
                model_config=ModelConfig(
                    class_type="not_registered",
                    constructor_parameters={
                        "from_yaml": os.path.join(
                            self.project_root,
                            "test_data/test_ReadFromFileObjectDetectionModel/"
                            "read-from-file_pascal-voc_test.yaml",
                        )
                    },
                )
            )

    def test_register_existing_model_force(self) -> None:
        model_registry = ModelRegistry()

        model_registry.register_model(
            model_type_name="test_model",
            model_constructor=TestModel,
        )

        model_registry.register_model(
            model_type_name="test_model", model_constructor=TestModel2, force=True
        )

        assert model_registry.get_registered_models()["test_model"] is TestModel2

    def test_register_existing_model_key_error(self) -> None:
        model_registry = ModelRegistry()

        model_registry.register_model(
            model_type_name="test_model",
            model_constructor=TestModel,
        )

        with self.assertRaises(KeyError):
            model_registry.register_model(
                model_type_name="test_model",
                model_constructor=TestModel2,
            )

    def test_get_registered_models(self) -> None:
        registered = ModelRegistry().get_registered_models()
        assert registered["read_from_file_classification"] is ReadFromFileClassificationModel
        assert registered["read_from_file_object_detection"] is ReadFromFileObjectDetectionModel
        assert registered["read_from_file_segmentation"] is ReadFromFileSegmentationModel


if __name__ == "__main__":
    main()
