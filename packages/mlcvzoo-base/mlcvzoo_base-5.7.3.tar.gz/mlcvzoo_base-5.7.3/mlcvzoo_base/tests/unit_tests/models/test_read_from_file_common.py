# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3
import logging
import os
from unittest import main

from related import to_model

from mlcvzoo_base.models.model_registry import ModelRegistry
from mlcvzoo_base.models.read_from_file.configuration import ReadFromFileConfig
from mlcvzoo_base.models.read_from_file.model import ReadFromFileModel
from mlcvzoo_base.tests.unit_tests.test_template import TestTemplate

logger = logging.getLogger(__name__)


class TestReadFromFileCommon(TestTemplate):
    def test_build_config_from_yaml(self) -> None:
        configuration = ReadFromFileModel.create_configuration(
            from_yaml=os.path.join(
                self.project_root,
                "test_data/test_ReadFromFileObjectDetectionModel/",
                "read-from-file_cvat_test.yaml",
            ),
            string_replacement_map=self.string_replacement_map,
        )

        assert configuration is not None

        config_dict = configuration.to_dict()

        configuration_2 = to_model(ReadFromFileConfig, config_dict)

        assert configuration_2 is not None

    def test_build_config(self) -> None:
        configuration = ReadFromFileModel.create_configuration(
            from_yaml=os.path.join(
                self.project_root,
                "test_data/test_ReadFromFileObjectDetectionModel/",
                "read-from-file_coco_test.yaml",
            ),
            string_replacement_map=self.string_replacement_map,
        )

        print(configuration)

    def test_read_from_file_registry(self) -> None:
        model_registry = ModelRegistry()

        # We are testing mlcvzoo-base code here, but this code only
        # works when the mlcvzoo-mmocr package project is installed
        # in the python environment
        assert model_registry.config_registry["read_from_file_config"] == ReadFromFileConfig


if __name__ == "__main__":
    main()
