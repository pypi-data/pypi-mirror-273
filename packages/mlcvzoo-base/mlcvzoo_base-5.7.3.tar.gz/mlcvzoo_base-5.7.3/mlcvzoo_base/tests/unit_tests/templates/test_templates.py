# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

import logging
import os
from typing import Dict, List, Type
from unittest import main

from config_builder import BaseConfigClass, ConfigBuilder

from mlcvzoo_base.configuration.annotation_handler_config import AnnotationHandlerConfig
from mlcvzoo_base.configuration.class_mapping_config import ClassMappingConfig
from mlcvzoo_base.configuration.mlfow_config import MLFlowConfig
from mlcvzoo_base.configuration.replacement_config import ReplacementConfig
from mlcvzoo_base.models.read_from_file.configuration import ReadFromFileConfig
from mlcvzoo_base.tests.unit_tests.test_template import TestTemplate

logger = logging.getLogger(__name__)


class TestTemplates(TestTemplate):
    def test_config_templates(self) -> None:
        template_path_dict: Dict[Type[BaseConfigClass], List[str]] = {
            ReplacementConfig: [
                os.path.join(
                    self.project_root,
                    "config",
                    "templates",
                    "replacement_config_template.yaml",
                )
            ],
            ClassMappingConfig: [
                os.path.join(
                    self.project_root,
                    "config",
                    "templates",
                    "data_preparation",
                    "class-mapping_config_template.yaml",
                )
            ],
            ReadFromFileConfig: [
                os.path.join(
                    self.project_root,
                    "config",
                    "templates",
                    "models",
                    "read-from-file.yaml",
                )
            ],
            AnnotationHandlerConfig: [
                os.path.join(
                    self.project_root,
                    "config",
                    "templates",
                    "data_preparation",
                    "annotation-handler_coco-config-template.yaml",
                ),
                os.path.join(
                    self.project_root,
                    "config",
                    "templates",
                    "data_preparation",
                    "annotation-handler_cvat-config-template.yaml",
                ),
                os.path.join(
                    self.project_root,
                    "config",
                    "templates",
                    "data_preparation",
                    "annotation-handler_pascal-voc-config-template.yaml",
                ),
            ],
            MLFlowConfig: [
                os.path.join(
                    self.project_root,
                    "config",
                    "templates",
                    "evaluation",
                    "mlflow_runner_config_template.yaml",
                )
            ],
        }

        for config_class_type, template_path_list in template_path_dict.items():
            for template_path in template_path_list:
                logger.info(
                    "=================================================================\n"
                    "CHECK correct build of configuration class %s "
                    "with template-config-path '%s'\n",
                    config_class_type,
                    template_path,
                )

                config_builder = ConfigBuilder(
                    class_type=config_class_type,
                    yaml_config_path=template_path,
                    string_replacement_map=self.string_replacement_map,
                    no_checks=True,
                )

                logger.info("=================================================================")
                assert config_builder.configuration is not None


if __name__ == "__main__":
    main()
