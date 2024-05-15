# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

import logging
import os
from typing import Optional
from unittest import main

from mlcvzoo_base.configuration.model_config import ModelConfig
from mlcvzoo_base.tests.unit_tests.test_template import TestTemplate

logger = logging.getLogger(__name__)

# TODO: add test that surrounding box is written to csv files


class TestModel:
    def __init__(
        self, from_yaml: Optional[str], test_int_parameter: int, test_bool_parameter: bool
    ):
        pass


class TestModelConfig(TestTemplate):
    def __create_test_model_config(self) -> ModelConfig:
        return ModelConfig(
            class_type="read_from_file_object_detection",
            constructor_parameters={
                "from_yaml": os.path.join(
                    self.project_root,
                    "test_data/test_ReadFromFileObjectDetectionModel/"
                    "read-from-file_pascal-voc_test.yaml",
                )
            },
        )

    def test_update_class_type(self) -> None:
        model_config = self.__create_test_model_config()

        model_config.update_class_type(
            args_dict={
                "class_type": "test_model",
            }
        )

        assert model_config.class_type == "test_model"

    def test_update_class_type_with_none(self) -> None:
        model_config = self.__create_test_model_config()

        model_config.update_class_type(
            args_dict={
                "class_type": None,
            }
        )

        assert model_config.class_type == "read_from_file_object_detection"

    def test_update_constructor_parameters(self) -> None:
        model_config = self.__create_test_model_config()

        model_config.update_constructor_parameters(
            args_dict={
                "class_type": "test_model",
                "constructor_parameters": [
                    {
                        "from_yaml": os.path.join(
                            self.project_root,
                            "test_data"
                            "test_ReadFromFileObjectDetectionModel"
                            "read-from-file_pascal-voc_test.yaml",
                        ),
                        "test_int_parameter": 10,
                        "test_bool_parameter": False,
                    }
                ],
            },
            model_type=TestModel,
        )

        assert type(model_config.constructor_parameters["from_yaml"]) is str
        assert type(model_config.constructor_parameters["test_int_parameter"]) is int
        assert type(model_config.constructor_parameters["test_bool_parameter"]) is bool

    def test_is_inference(self) -> None:
        assert self.__create_test_model_config().is_inference() is False

    def test_set_inference(self) -> None:
        model_config = self.__create_test_model_config()
        model_config.set_inference(inference=True)
        assert model_config.is_inference() is True


if __name__ == "__main__":
    main()
