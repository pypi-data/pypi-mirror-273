# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

import json
import logging
import math
import os
from typing import Any, Dict, List
from unittest import main

from mlflow import MlflowClient
from mlflow.entities.run import Run

from mlcvzoo_base.api.data.annotation import BaseAnnotation
from mlcvzoo_base.api.data.class_identifier import ClassIdentifier
from mlcvzoo_base.api.model import ObjectDetectionModel
from mlcvzoo_base.configuration.mlfow_config import MLFlowConfig, MLFlowFileConfig
from mlcvzoo_base.configuration.model_config import ModelConfig
from mlcvzoo_base.configuration.structs import MLFlowExperimentTypes
from mlcvzoo_base.data_preparation.annotation_handler import AnnotationHandler
from mlcvzoo_base.evaluation.object_detection.configuration import (
    TensorboardLoggingConfig,
)
from mlcvzoo_base.evaluation.object_detection.data_classes import (
    METRIC_DICT_TYPE,
    ODMetrics,
    ODModelEvaluationMetrics,
    build_metric_dict_from_dict,
)
from mlcvzoo_base.evaluation.object_detection.metrics_computation import (
    MetricsComputation,
)
from mlcvzoo_base.evaluation.object_detection.metrics_logging import (
    log_od_metrics_to_mlflow_run,
    output_evaluation_results,
)
from mlcvzoo_base.evaluation.object_detection.model_evaluation import (
    evaluate_with_model,
    evaluate_with_precomputed_data,
)
from mlcvzoo_base.evaluation.object_detection.structs import MetricTypes
from mlcvzoo_base.evaluation.object_detection.utils import (
    generate_fn_fp_confusion_matrix_table,
    generate_fn_fp_confusion_matrix_table_from_dict,
)
from mlcvzoo_base.metrics.mlflow.mlflow_runner import MLFLowRunner
from mlcvzoo_base.models.model_registry import ModelRegistry
from mlcvzoo_base.tests.unit_tests.test_template import TestTemplate
from mlcvzoo_base.utils.common_utils import CustomJSONEncoder
from mlcvzoo_base.utils.file_utils import ensure_dir

logger = logging.getLogger(__name__)


class TestODEvaluation(TestTemplate):
    def test_od_evaluation_with_precomputed(self) -> None:
        annotation_handler = AnnotationHandler(
            yaml_config_path=os.path.join(
                self.project_root,
                "test_data/test_AnnotationHandler/"
                "annotation-handler_pascal-voc_evaluation.yaml",
            ),
            string_replacement_map=self.string_replacement_map,
        )

        annotations: List[BaseAnnotation] = annotation_handler.parse_annotations_from_xml()

        iou_thresholds = [0.5]

        # Compute Metrics
        model_metrics = evaluate_with_precomputed_data(
            model_specifier="test_od_evaluation_with_precomputed",
            classes_id_dict=None,
            gt_annotations=annotations,
            predicted_bounding_boxes_list=[
                annotation.get_bounding_boxes(include_segmentations=True)
                for annotation in annotations
            ],
            iou_thresholds=iou_thresholds,
            mapper=annotation_handler.mapper,
        )

        output_evaluation_results(model_metrics=model_metrics, iou_thresholds=iou_thresholds)

        predicted_metrics_file_dir = os.path.join(
            self.project_root,
            "test_output",
            "evaluation",
            "test_od_evaluation",
            "predicted_metrics",
        )

        wanted_metrics_file_dir = os.path.join(
            self.project_root,
            "test_data/test_od_evaluation/",
            "wanted_metrics",
        )

        predicted_metrics_file_name = f"metrics-dict_precomputed.json"
        wanted_metrics_file_name = f"wanted_{predicted_metrics_file_name}"

        predicted_metrics_file_path = os.path.join(
            predicted_metrics_file_dir, predicted_metrics_file_name
        )

        wanted_metrics_file_path = os.path.join(wanted_metrics_file_dir, wanted_metrics_file_name)

        ensure_dir(file_path=predicted_metrics_file_path, verbose=True)

        with open(file=predicted_metrics_file_path, mode="w") as predicted_metrics_file:
            logger.debug("Write predicted metrics-dict to: %s", predicted_metrics_file_path)
            json.dump(
                obj=model_metrics.metrics_dict,
                fp=predicted_metrics_file,
                indent=2,
                cls=CustomJSONEncoder,
            )

        wanted_metrics: Dict[float, Dict[str, Dict[str, Any]]]
        with open(file=wanted_metrics_file_path, mode="r") as wanted_metrics_file:
            logger.debug("Read wanted metrics-dict from: %s", wanted_metrics_file_path)
            wanted_metrics_dict = json.load(fp=wanted_metrics_file)

        assert TestODEvaluation.__check_metrics_equal(
            metrics_dict=model_metrics.metrics_dict,
            wanted_metrics_dict=wanted_metrics_dict,
        )

    def test_od_evaluation_with_precomputed_deprecated(self) -> None:
        annotation_handler = AnnotationHandler(
            yaml_config_path=os.path.join(
                self.project_root,
                "test_data/test_AnnotationHandler/"
                "annotation-handler_pascal-voc_evaluation.yaml",
            ),
            string_replacement_map=self.string_replacement_map,
        )

        annotations: List[BaseAnnotation] = annotation_handler.parse_annotations_from_xml()

        iou_thresholds = [0.5]

        # Compute Metrics
        model_metrics = evaluate_with_precomputed_data(
            model_specifier="test_od_evaluation_with_precomputed",
            classes_id_dict=annotation_handler.mapper.annotation_class_id_to_model_class_name_map,
            gt_annotations=annotations,
            predicted_bounding_boxes_list=[
                annotation.get_bounding_boxes(include_segmentations=True)
                for annotation in annotations
            ],
            iou_thresholds=iou_thresholds,
        )

        output_evaluation_results(model_metrics=model_metrics, iou_thresholds=iou_thresholds)

        predicted_metrics_file_dir = os.path.join(
            self.project_root,
            "test_output",
            "evaluation",
            "test_od_evaluation",
            "predicted_metrics",
        )

        wanted_metrics_file_dir = os.path.join(
            self.project_root,
            "test_data/test_od_evaluation/",
            "wanted_metrics",
        )

        predicted_metrics_file_name = f"metrics-dict_precomputed.json"
        wanted_metrics_file_name = f"wanted_{predicted_metrics_file_name}"

        predicted_metrics_file_path = os.path.join(
            predicted_metrics_file_dir, predicted_metrics_file_name
        )

        wanted_metrics_file_path = os.path.join(wanted_metrics_file_dir, wanted_metrics_file_name)

        ensure_dir(file_path=predicted_metrics_file_path, verbose=True)

        with open(file=predicted_metrics_file_path, mode="w") as predicted_metrics_file:
            logger.debug("Write predicted metrics-dict to: %s", predicted_metrics_file_path)
            json.dump(
                obj=model_metrics.metrics_dict,
                fp=predicted_metrics_file,
                indent=2,
                cls=CustomJSONEncoder,
            )

        wanted_metrics: Dict[float, Dict[str, Dict[str, Any]]]
        with open(file=wanted_metrics_file_path, mode="r") as wanted_metrics_file:
            logger.debug("Read wanted metrics-dict from: %s", wanted_metrics_file_path)
            wanted_metrics_dict = json.load(fp=wanted_metrics_file)

            real_wanted_metrics_dict = build_metric_dict_from_dict(input_dict=wanted_metrics_dict)

        assert TestODEvaluation.__check_metrics_equal(
            metrics_dict=model_metrics.metrics_dict,
            wanted_metrics_dict=wanted_metrics_dict,
        )

    def test_od_evaluation_with_precomputed_neither_dict_nor_mapper_error(self) -> None:
        annotation_handler = AnnotationHandler(
            yaml_config_path=os.path.join(
                self.project_root,
                "test_data/test_AnnotationHandler/" "annotation-handler_pascal-voc_test.yaml",
            ),
            string_replacement_map=self.string_replacement_map,
        )

        annotations: List[BaseAnnotation] = annotation_handler.parse_annotations_from_xml()

        iou_thresholds = [0.5]

        # Compute Metrics
        with self.assertRaises(ValueError):
            evaluate_with_precomputed_data(
                model_specifier="test_od_evaluation_with_precomputed",
                classes_id_dict=None,
                gt_annotations=annotations,
                predicted_bounding_boxes_list=[
                    annotation.get_bounding_boxes(include_segmentations=True)
                    for annotation in annotations
                ],
                iou_thresholds=iou_thresholds,
                mapper=None,
            )

    def test_od_evaluation_model_based(self) -> None:
        annotation_handler = AnnotationHandler(
            yaml_config_path=os.path.join(
                self.project_root,
                "test_data/test_od_evaluation/"
                "test_od_evaluation_model_based_annotation_handler.yaml",
            ),
            string_replacement_map=self.string_replacement_map,
        )

        annotations: List[BaseAnnotation] = annotation_handler.parse_annotations_from_csv(
            csv_file_path=os.path.join(
                self.project_root,
                "test_data/annotations/csv_annotations/test-evaluation.csv",
            )
        )

        model_registry = ModelRegistry()

        model_config = ModelConfig(
            class_type="read_from_file_object_detection",
            constructor_parameters={
                "from_yaml": os.path.join(
                    self.project_root,
                    "test_data/test_ReadFromFileObjectDetectionModel/"
                    "read-from-file_pascal-voc_test.yaml",
                ),
            },
        )

        iou_thresholds = [0.5]

        model: Model[PredictionType, ConfigurationType, DataType]  # type: ignore
        model = model_registry.init_model(
            model_config=model_config,
            string_replacement_map=self.string_replacement_map,
        )

        if not isinstance(model, ObjectDetectionModel):
            raise ValueError(
                "This evaluation can only be used with models that "
                "inherit from 'mlcvzoo.api.model.ObjectDetectionModel'"
            )

        model_metrics_list: List[ODModelEvaluationMetrics] = [
            evaluate_with_model(
                gt_annotations=annotations, iou_thresholds=iou_thresholds, model=model
            )
        ]

        mlflow_runner = MLFLowRunner(
            configuration=MLFlowConfig(
                mlflow_file_config=MLFlowFileConfig(
                    logging_dir=os.path.join(self.project_root, "test_output/logs/mlflow_logs/")
                ),
                artifact_location=os.path.join(self.project_root, "test_output/logs/mlflow_logs/"),
            )
        )

        # CHECK RESULTS
        for model_metrics in model_metrics_list:
            if mlflow_runner is not None:
                mlflow_runner.start_mlflow_run(
                    experiment_name=MLFlowExperimentTypes.EVAL,
                    run_name=model_metrics.model_specifier,
                    end_runs_in_advance=True,
                )

            tb_logging_dir = os.path.join(
                self.project_root,
                "test_output",
                "evaluation",
                "test_od_evaluation",
                "tb_logging",
            )

            output_evaluation_results(
                model_metrics=model_metrics,
                iou_thresholds=iou_thresholds,
                tensorboard_logging=TensorboardLoggingConfig(tensorboard_dir=tb_logging_dir),
            )

            (
                _,
                confusion_matrix_as_dict,
            ) = MetricsComputation.match_false_negatives_and_false_positives_as_dict(
                metrics_image_info_dict=model_metrics.metrics_image_info_dict,
                iou_threshold=iou_thresholds[0],
            )
            print(
                generate_fn_fp_confusion_matrix_table_from_dict(
                    confusion_matrix=confusion_matrix_as_dict,
                ).table
            )

            person_class_identifier = ClassIdentifier(class_id=0, class_name="person")
            truck_class_identifier = ClassIdentifier(class_id=1, class_name="truck")
            car_class_identifier = ClassIdentifier(class_id=2, class_name="car")

            assert (
                confusion_matrix_as_dict[str(person_class_identifier)][str(truck_class_identifier)]
                == 1
            )
            assert (
                confusion_matrix_as_dict[str(truck_class_identifier)][str(car_class_identifier)]
                == 1
            )
            assert (
                confusion_matrix_as_dict[str(car_class_identifier)][str(truck_class_identifier)]
                == 2
            )

            predicted_metrics_file_dir = os.path.join(
                self.project_root,
                "test_output",
                "evaluation",
                "test_od_evaluation",
                "predicted_metrics",
            )

            predicted_metrics_file_name = f"metrics-dict_read-from-file_pascal-voc_test.json"
            predicted_metrics_file_path = os.path.join(
                predicted_metrics_file_dir, predicted_metrics_file_name
            )

            wanted_metrics_file_path = os.path.join(
                self.project_root,
                "test_data/test_od_evaluation/",
                "wanted_metrics",
                f"wanted_{predicted_metrics_file_name}",
            )

            ensure_dir(file_path=predicted_metrics_file_path, verbose=True)

            with open(file=predicted_metrics_file_path, mode="w") as predicted_metrics_file:
                logger.debug("Write predicted metrics-dict to: %s", predicted_metrics_file_path)
                json.dump(
                    obj=model_metrics.metrics_dict,
                    fp=predicted_metrics_file,
                    indent=2,
                    cls=CustomJSONEncoder,
                )

            wanted_metrics: Dict[float, Dict[str, Dict[str, Any]]]
            with open(file=wanted_metrics_file_path, mode="r") as wanted_metrics_file:
                logger.debug("Read wanted metrics-dict from: %s", wanted_metrics_file_path)
                wanted_metrics_dict = json.load(fp=wanted_metrics_file)

            assert TestODEvaluation.__check_metrics_equal(
                metrics_dict=model_metrics.metrics_dict,
                wanted_metrics_dict=wanted_metrics_dict,
            )

    def test_log_with_mlflow_client(self) -> None:
        annotation_handler = AnnotationHandler(
            yaml_config_path=os.path.join(
                self.project_root,
                "test_data/test_AnnotationHandler/"
                "annotation-handler_pascal-voc_evaluation.yaml",
            ),
            string_replacement_map=self.string_replacement_map,
        )

        annotations: List[BaseAnnotation] = annotation_handler.parse_annotations_from_xml()

        iou_thresholds = [0.5]

        # Compute Metrics
        model_metrics = evaluate_with_precomputed_data(
            model_specifier="test_od_evaluation_with_precomputed",
            classes_id_dict=None,
            gt_annotations=annotations,
            predicted_bounding_boxes_list=[
                annotation.get_bounding_boxes(include_segmentations=True)
                for annotation in annotations
            ],
            iou_thresholds=iou_thresholds,
            mapper=annotation_handler.mapper,
        )

        mlflow_client = MlflowClient()
        experiment = mlflow_client.get_experiment_by_name("TEST")

        if experiment:
            exp_id = experiment.experiment_id
        else:
            exp_id = mlflow_client.create_experiment("TEST")
        run: Run = mlflow_client.create_run(experiment_id=exp_id)

        log_od_metrics_to_mlflow_run(
            mlflow_client=mlflow_client,
            run_id=run.info.run_id,
            model_specifier="test-model",
            metrics_dict=model_metrics.metrics_dict,
            iou_threshold=0.5,
        )

    def test_ap_50_metric(self) -> None:
        wanted_metrics_file_path = os.path.join(
            self.project_root,
            "test_data/test_od_evaluation/wanted_metrics/"
            "wanted_metrics-dict_read-from-file_pascal-voc_test.json",
        )

        wanted_metrics: Dict[float, Dict[str, Dict[str, Any]]]
        with open(file=wanted_metrics_file_path, mode="r") as wanted_metrics_file:
            logger.debug("Read wanted metrics-dict from: %s", wanted_metrics_file_path)
            wanted_metrics_dict = build_metric_dict_from_dict(
                input_dict=json.load(fp=wanted_metrics_file)
            )

            ap_50 = MetricsComputation.get_overall_ap(
                metrics_dict=wanted_metrics_dict, iou_threshold=0.5
            )

            assert math.isclose(ap_50, 0.21, abs_tol=0.05)

    def test_od_evaluation_model_based_deprecated(self) -> None:
        annotation_handler = AnnotationHandler(
            yaml_config_path=os.path.join(
                self.project_root,
                "test_data/test_od_evaluation/"
                "test_od_evaluation_model_based_annotation_handler.yaml",
            ),
            string_replacement_map=self.string_replacement_map,
        )

        annotations: List[BaseAnnotation] = annotation_handler.parse_annotations_from_csv(
            csv_file_path=os.path.join(
                self.project_root,
                "test_data/annotations/csv_annotations/test-evaluation.csv",
            )
        )

        model_registry = ModelRegistry()

        model_config = ModelConfig(
            class_type="read_from_file_object_detection",
            constructor_parameters={
                "from_yaml": os.path.join(
                    self.project_root,
                    "test_data/test_ReadFromFileObjectDetectionModel/"
                    "read-from-file_pascal-voc_test.yaml",
                ),
            },
        )

        iou_thresholds = [0.5]

        model: Model[PredictionType, ConfigurationType, DataType]  # type: ignore
        model = model_registry.init_model(
            model_config=model_config,
            string_replacement_map=self.string_replacement_map,
        )

        if not isinstance(model, ObjectDetectionModel):
            raise ValueError(
                "This evaluation can only be used with models that "
                "inherit from 'mlcvzoo.api.model.ObjectDetectionModel'"
            )

        model_metrics_list: List[ODModelEvaluationMetrics] = [
            evaluate_with_model(
                gt_annotations=annotations, iou_thresholds=iou_thresholds, model=model
            )
        ]

        # CHECK RESULTS
        for model_metrics in model_metrics_list:
            (
                result_metrics_image_info_dict,
                confusion_matrix,
            ) = MetricsComputation.match_false_negatives_and_false_positives(
                metrics_image_info_dict=model_metrics.metrics_image_info_dict,
                iou_threshold=iou_thresholds[0],
            )
            print(
                generate_fn_fp_confusion_matrix_table(
                    confusion_matrix=confusion_matrix,
                    classes_id_dict=annotation_handler.mapper.annotation_class_id_to_model_class_name_map,
                ).table
            )

            assert confusion_matrix[0][1] == 1
            assert confusion_matrix[1][2] == 1
            assert confusion_matrix[2][1] == 2

            predicted_metrics_file_dir = os.path.join(
                self.project_root,
                "test_output",
                "evaluation",
                "test_od_evaluation",
                "predicted_metrics",
            )

            wanted_metrics_file_dir = os.path.join(
                self.project_root,
                "test_data/test_od_evaluation/",
                "wanted_metrics",
            )

            predicted_metrics_file_name = f"metrics-dict_read-from-file_pascal-voc_test.json"
            wanted_metrics_file_name = f"wanted_{predicted_metrics_file_name}"

            predicted_metrics_file_path = os.path.join(
                predicted_metrics_file_dir, predicted_metrics_file_name
            )

            wanted_metrics_file_path = os.path.join(
                wanted_metrics_file_dir, wanted_metrics_file_name
            )

            ensure_dir(file_path=predicted_metrics_file_path, verbose=True)

            with open(file=predicted_metrics_file_path, mode="w") as predicted_metrics_file:
                logger.debug("Write predicted metrics-dict to: %s", predicted_metrics_file_path)
                json.dump(
                    obj=model_metrics.metrics_dict,
                    fp=predicted_metrics_file,
                    indent=2,
                    cls=CustomJSONEncoder,
                )

            wanted_metrics: Dict[float, Dict[str, Dict[str, Any]]]
            with open(file=wanted_metrics_file_path, mode="r") as wanted_metrics_file:
                logger.debug("Read wanted metrics-dict from: %s", wanted_metrics_file_path)
                wanted_metrics_dict = json.load(fp=wanted_metrics_file)

            assert TestODEvaluation.__check_metrics_equal(
                metrics_dict=model_metrics.metrics_dict,
                wanted_metrics_dict=wanted_metrics_dict,
            )

            ap_50 = MetricsComputation.get_overall_ap(
                metrics_dict=model_metrics.metrics_dict, iou_threshold=0.5
            )

            assert math.isclose(ap_50, 0.21, abs_tol=0.05)

    def test_get_overall_ap_no_iou_threshold(self) -> None:
        metrics_dict = {0.5: {"ALL": {"test_class": ODMetrics()}}}

        with self.assertRaises(ValueError):
            MetricsComputation.get_overall_ap(metrics_dict=metrics_dict, iou_threshold=0.6)

    def test_compute_average_ap(self) -> None:
        metrics_dict = {
            0.5: {
                "ALL": {
                    "test_class": ODMetrics(
                        TP=2,
                        FP=1,
                        FN=0,
                        PR=2 / 3,
                        RC=2 / 4,
                        F1=1.0,
                        AP=0.9,
                        COUNT=4,
                    )
                }
            },
            0.6: {
                "ALL": {
                    "test_class": ODMetrics(
                        TP=5,
                        FP=1,
                        FN=0,
                        PR=2 / 6,
                        RC=2 / 4,
                        F1=1.0,
                        AP=0.95,
                        COUNT=10,
                    )
                }
            },
        }

        assert math.isclose(
            MetricsComputation.compute_average_ap(
                model_metrics=ODModelEvaluationMetrics(
                    model_specifier="test_model",
                    metrics_dict=metrics_dict,
                    metrics_image_info_dict={},
                )
            ),
            0.925,
            abs_tol=0.05,
        )

    def test_get_ap_50(self) -> None:
        metrics_dict = {
            0.5: {
                "ALL": {
                    "test_class": ODMetrics(
                        TP=2,
                        FP=1,
                        FN=0,
                        PR=2 / 3,
                        RC=2 / 4,
                        F1=1.0,
                        AP=0.9,
                        COUNT=4,
                    )
                }
            },
            0.6: {
                "ALL": {
                    "test_class": ODMetrics(
                        TP=5,
                        FP=1,
                        FN=0,
                        PR=2 / 6,
                        RC=2 / 4,
                        F1=1.0,
                        AP=0.95,
                        COUNT=10,
                    )
                }
            },
        }

        assert math.isclose(
            MetricsComputation.get_ap_50(
                model_metrics=ODModelEvaluationMetrics(
                    model_specifier="test_model",
                    metrics_dict=metrics_dict,
                    metrics_image_info_dict={},
                )
            ),
            0.9,
            abs_tol=0.05,
        )

    def test_get_ap_50_95(self) -> None:
        all_box_metrics = {
            "ALL": {
                "test_class": ODMetrics(
                    TP=2,
                    FP=1,
                    FN=0,
                    PR=2 / 3,
                    RC=2 / 4,
                    F1=1.0,
                    AP=0.9,
                    COUNT=4,
                )
            }
        }

        metrics_dict: METRIC_DICT_TYPE = {
            iou_threshold: all_box_metrics
            for iou_threshold in MetricsComputation.iou_thresholds_ap_50_95
        }

        assert math.isclose(
            MetricsComputation.get_ap_50_95(
                model_metrics=ODModelEvaluationMetrics(
                    model_specifier="test_model",
                    metrics_dict=metrics_dict,
                    metrics_image_info_dict={},
                )
            ),
            0.9,
            abs_tol=0.05,
        )

    def test_get_ap_50_95_incomplete_iou_thresholds(self) -> None:
        metrics_dict = {
            0.5: {
                "ALL": {
                    "test_class": ODMetrics(
                        TP=2,
                        FP=1,
                        FN=0,
                        PR=2 / 3,
                        RC=2 / 4,
                        F1=1.0,
                        AP=0.9,
                        COUNT=4,
                    )
                }
            },
            0.6: {
                "ALL": {
                    "test_class": ODMetrics(
                        TP=5,
                        FP=1,
                        FN=0,
                        PR=2 / 6,
                        RC=2 / 4,
                        F1=1.0,
                        AP=0.95,
                        COUNT=10,
                    )
                }
            },
        }

        with self.assertRaises(ValueError):
            MetricsComputation.get_ap_50_95(
                model_metrics=ODModelEvaluationMetrics(
                    model_specifier="test_model",
                    metrics_dict=metrics_dict,
                    metrics_image_info_dict={},
                )
            )

    @staticmethod
    def __check_metrics_equal(
        metrics_dict: METRIC_DICT_TYPE,
        wanted_metrics_dict: Dict,
    ) -> bool:
        for iou_threshold, iou_threshold_dict in metrics_dict.items():
            for bbox_size_type, bbox_size_type_dict in iou_threshold_dict.items():
                for class_name, metrics in bbox_size_type_dict.items():
                    if (
                        wanted_metrics_dict[str(iou_threshold)][bbox_size_type][class_name][
                            MetricTypes.TRUE_POSITIVES
                        ]
                        != metrics.TP
                    ):
                        return False
                    if (
                        wanted_metrics_dict[str(iou_threshold)][bbox_size_type][class_name][
                            MetricTypes.FALSE_POSITIVES
                        ]
                        != metrics.FP
                    ):
                        return False
                    if (
                        wanted_metrics_dict[str(iou_threshold)][bbox_size_type][class_name][
                            MetricTypes.PRECISION
                        ]
                        != metrics.PR
                    ):
                        return False
                    if (
                        wanted_metrics_dict[str(iou_threshold)][bbox_size_type][class_name][
                            MetricTypes.RECALL
                        ]
                        != metrics.RC
                    ):
                        return False
                    if (
                        wanted_metrics_dict[str(iou_threshold)][bbox_size_type][class_name][
                            MetricTypes.F1
                        ]
                        != metrics.F1
                    ):
                        return False
                    if (
                        wanted_metrics_dict[str(iou_threshold)][bbox_size_type][class_name][
                            MetricTypes.AP
                        ]
                        != metrics.AP
                    ):
                        return False

        return True

    def test_update_no_bounding_boxes(self):
        original_annotations_dict = {0: {}, 1: {}, 2: {}}
        all_annotations_dict = original_annotations_dict.copy()

        all_annotations_dict = MetricsComputation._MetricsComputation__update_annotation_data_dict(
            class_identifier_list=[],
            all_annotations_dict=all_annotations_dict,
            index=0,
            new_annotation=BaseAnnotation(image_path="", annotation_path="", image_shape=(0, 0)),
        )

        assert all_annotations_dict == original_annotations_dict


if __name__ == "__main__":
    # Run unittest main
    main()
