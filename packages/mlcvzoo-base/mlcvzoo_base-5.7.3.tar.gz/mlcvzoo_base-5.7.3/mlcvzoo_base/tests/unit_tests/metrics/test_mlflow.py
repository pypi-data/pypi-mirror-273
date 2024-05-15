# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3
import logging
import os
from typing import Optional

import cv2
import mlflow
from config_builder import ConfigBuilder

from mlcvzoo_base.configuration.structs import MLFlowExperimentTypes
from mlcvzoo_base.metrics.mlflow.mlflow_runner import MLFLowRunner
from mlcvzoo_base.metrics.mlflow.utils import (
    mlflow_log_config_to_yaml,
    mlflow_log_git_info,
    mlflow_log_pip_package_versions,
)
from mlcvzoo_base.models.read_from_file.configuration import ReadFromFileConfig
from mlcvzoo_base.tests.unit_tests.test_template import TestTemplate
from mlcvzoo_base.utils.versioning_utils import (
    get_installed_package_versions,
    get_installed_pip_package_versions,
)

logger = logging.getLogger(__name__)


class TestMLFlow(TestTemplate):
    def setUp(self) -> None:
        TestTemplate.setUp(self)
        self.mlflow_runner: Optional[MLFLowRunner] = None

    def __init_mlflow_runner(self) -> None:
        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_mlflow_runner/test_mlflow_file_config.yaml",
        )

        self.mlflow_runner = MLFLowRunner(
            yaml_config_path=yaml_config_path,
            string_replacement_map=self.string_replacement_map,
        )

        self.mlflow_runner.create_mlflow_experiments()

    def test_mlflow_runner_create_experiments_file_based(self) -> None:
        logger.info(
            "############################################################\n"
            "# TEST creation of mlflow experiments:\n"
            "#      test_mlflow_runner_create_experiments_file_based(self)\n"
            "############################################################"
        )

        if self.mlflow_runner is None:
            self.__init_mlflow_runner()

        assert self.mlflow_runner is not None

        self.mlflow_runner.start_mlflow_run(
            experiment_name=MLFlowExperimentTypes.DATA_GENERATION,
            run_name="test_mlflow",
        )

        mlflow.log_metric(key="test_metric", value=1, step=0)

        image_path = os.path.join(
            self.project_root,
            "test_data/images/dummy_task/truck.jpg",
        )

        image = cv2.imread(filename=image_path)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        mlflow.log_image(image=image, artifact_file="test.jpg")

        MLFLowRunner.end_run()

    def test_mlflow_log_config_to_yaml(self) -> None:
        logger.info(
            "############################################################\n"
            "# TEST mlflow logging of a given configuration object to a yaml file :\n"
            "#      test_mlflow_log_config_to_yaml(self)\n"
            "############################################################"
        )

        if self.mlflow_runner is None:
            self.__init_mlflow_runner()

        assert self.mlflow_runner is not None

        self.mlflow_runner.start_mlflow_run(
            experiment_name=MLFlowExperimentTypes.TRAIN,
            run_name="test_mlflow",
        )

        read_from_file_config_path = os.path.join(
            self.project_root,
            "test_data/test_ReadFromFileObjectDetectionModel/",
            "read-from-file_coco_test.yaml",
        )

        config_builder = ConfigBuilder(
            class_type=ReadFromFileConfig,
            yaml_config_path=read_from_file_config_path,
            string_replacement_map=self.string_replacement_map,
        )

        output_yaml_config_path = os.path.join(
            self.project_root, "test_output/read-from-file_coco_test.yaml"
        )

        mlflow_log_config_to_yaml(
            config=config_builder.configuration,
            output_yaml_config_path=output_yaml_config_path,
        )

        MLFLowRunner.end_run()

    def test_mlflow_log_pip_package_version(self) -> None:
        logger.info(
            "############################################################\n"
            "# TEST mlflow logging of a currently installed pip package versions to a file :\n"
            "#      test_mlflow_log_pip_package_version(self)\n"
            "############################################################"
        )

        if self.mlflow_runner is None:
            self.__init_mlflow_runner()

        assert self.mlflow_runner is not None

        self.mlflow_runner.start_mlflow_run(
            experiment_name=MLFlowExperimentTypes.TRAIN,
            run_name="test_mlflow",
        )

        output_requirements_path = os.path.join(
            self.project_root, "test_output/sample_requirements.txt"
        )

        logger.debug("get_installed_package_versions: {}".format(get_installed_package_versions()))
        logger.debug(
            "get_installed_pip_package_versions: {}".format(get_installed_pip_package_versions())
        )

        mlflow_log_pip_package_versions(output_requirements_path=output_requirements_path)

        MLFLowRunner.end_run()

    def test_mlflow_log_git_info(self) -> None:
        logger.info(
            "############################################################\n"
            "# TEST mlflow logging of git informations of the current project:\n"
            "#      test_mlflow_log_git_info(self)\n"
            "############################################################"
        )

        if self.mlflow_runner is None:
            self.__init_mlflow_runner()

        assert self.mlflow_runner is not None

        self.mlflow_runner.start_mlflow_run(
            experiment_name=MLFlowExperimentTypes.TRAIN,
            run_name="test_mlflow",
        )

        mlflow_log_git_info()

        MLFLowRunner.end_run()

    def test_mlflow_runner_create_experiments_postgressql_based(self) -> None:
        logger.info(
            "############################################################\n"
            "# TEST creation of mlflow experiments:\n"
            "#      test_mlflow_runner_create_experiments_postgressql_based(self)\n"
            "############################################################"
        )
        # NOTE: This test only works when you have a valid setup of a mlflow postgresql database
        yaml_config_path = os.path.join(
            self.project_root,
            "test_data/test_mlflow_runner/test_mlflow_postgressql_config.yaml",
        )

        try:
            mlflow_runner = MLFLowRunner(
                yaml_config_path=yaml_config_path,
                string_replacement_map=self.string_replacement_map,
                create_experiments=True,
            )
            mlflow_runner.start_mlflow_run(
                experiment_name=MLFlowExperimentTypes.DATA_GENERATION,
                run_name="test_mlflow",
            )

        except ModuleNotFoundError:
            logger.warning(
                "WARNING: Postgresql database is not running, this test will be skipped"
            )
            return

        mlflow.log_metric(key="test_metric", value=1, step=0)

        image_path = os.path.join(
            self.project_root,
            "test_data/images/dummy_tasktruck.jpg",
        )
        image = cv2.imread(filename=image_path)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mlflow.log_image(image=image, artifact_file="test.jpg")

        MLFLowRunner.end_run()
