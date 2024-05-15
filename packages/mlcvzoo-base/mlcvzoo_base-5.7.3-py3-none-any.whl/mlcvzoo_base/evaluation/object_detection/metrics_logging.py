# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""
Gathering of utility methods that are generating metric output in any
kind of form.
"""

import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

import mlflow
from mlflow import MlflowClient
from tensorboardX import SummaryWriter

from mlcvzoo_base.configuration.structs import FileNamePlaceholders
from mlcvzoo_base.evaluation.object_detection.configuration import (
    TensorboardLoggingConfig,
)
from mlcvzoo_base.evaluation.object_detection.data_classes import (
    METRIC_DICT_TYPE,
    METRIC_IMAGE_INFO_TYPE,
    ODModelEvaluationMetrics,
)
from mlcvzoo_base.evaluation.object_detection.structs import BBoxSizeTypes
from mlcvzoo_base.evaluation.object_detection.utils import (
    __create_tf_image,
    generate_img_id_map,
    generate_metric_table,
)
from mlcvzoo_base.utils import ensure_dir

logger = logging.getLogger(__name__)


def log_od_metrics_to_mlflow(
    model_specifier: str,
    metrics_dict: METRIC_DICT_TYPE,
    iou_threshold: float,
    score_threshold: Optional[float] = None,
    nms_threshold: Optional[float] = None,
    step: Optional[int] = None,
) -> None:
    """
    Log the object detection metrics for the given iou threshold with mlflow.
    This includes the logging of any metric that is defined by the
    dataclass mlcvzoo.evaluation.object_detection.data_classes.ODMetrics
    for any bounding box size type defined in the class
    mlcvzoo.evaluation.object_detection.structs.BBoxSizeTypes

    Args:
        model_specifier: String identifying a model
        metrics_dict: The metrics dictionary where to take the metrics from
        iou_threshold: The iou threshold for which the metrics should be logged
        score_threshold: Optionally hand over the score threshold with which the
                         metrics have been generated
        nms_threshold: Optionally hand over the nms threshold with which the
                      metrics have been generated
        step: Metric step that is handed over to mlflow

    Returns:
        None
    """

    if mlflow.active_run() is not None:
        mlflow.log_param("algorithm_type", "Object Detection")

        logger.debug("Log mlflow metrics for model '%s'", model_specifier)

        if score_threshold is not None:
            mlflow.log_param(key="score_threshold", value=score_threshold)
        if nms_threshold is not None:
            mlflow.log_param(key="nms_threshold", value=nms_threshold)

        for bbox_size_type in BBoxSizeTypes.get_values_as_list(class_type=BBoxSizeTypes):
            for class_name, od_metric in metrics_dict[iou_threshold][bbox_size_type].items():
                mlflow.log_metric(
                    key=f"{class_name}_TP_{bbox_size_type}",
                    value=od_metric.TP,
                    step=step,
                )
                mlflow.log_metric(
                    key=f"{class_name}_FP_{bbox_size_type}",
                    value=od_metric.FP,
                    step=step,
                )
                mlflow.log_metric(
                    key=f"{class_name}_FN_{bbox_size_type}",
                    value=od_metric.FN,
                    step=step,
                )
                mlflow.log_metric(
                    key=f"{class_name}_COUNT_{bbox_size_type}",
                    value=od_metric.COUNT,
                    step=step,
                )
                mlflow.log_metric(
                    key=f"{class_name}_RC_{bbox_size_type}",
                    value=od_metric.RC,
                    step=step,
                )
                mlflow.log_metric(
                    key=f"{class_name}_PR_{bbox_size_type}",
                    value=od_metric.PR,
                    step=step,
                )
                mlflow.log_metric(
                    key=f"{class_name}_F1_{bbox_size_type}",
                    value=od_metric.F1,
                    step=step,
                )
                mlflow.log_metric(
                    key=f"{class_name}_AP_{bbox_size_type}",
                    value=od_metric.AP,
                    step=step,
                )
    else:
        logger.warning(
            "Can not log metrics with 'log_od_metrics_to_mlflow' for model '%s' "
            "since no mlflow run is active",
            model_specifier,
        )


def log_od_metrics_to_mlflow_run(
    mlflow_client: MlflowClient,
    run_id: str,
    model_specifier: str,
    metrics_dict: METRIC_DICT_TYPE,
    iou_threshold: float,
    score_threshold: Optional[float] = None,
    nms_threshold: Optional[float] = None,
    step: Optional[int] = None,
) -> None:
    """
    Log the object detection metrics for the given iou threshold with mlflow.
    This includes the logging of any metric that is defined by the
    dataclass mlcvzoo.evaluation.object_detection.data_classes.ODMetrics
    for any bounding box size type defined in the class
    mlcvzoo.evaluation.object_detection.structs.BBoxSizeTypes

    Args:
        mlflow_client: The MlflowClient object that should be used for logging to mlflow
        run_id: The run-id of the mlflow run where the metrics should be logged to
        model_specifier: String identifying a model
        metrics_dict: The metrics dictionary where to take the metrics from
        iou_threshold: The iou threshold for which the metrics should be logged
        score_threshold: Optionally hand over the score threshold with which the
                         metrics have been generated
        nms_threshold: Optionally hand over the nms threshold with which the
                      metrics have been generated
        step: Metric step that is handed over to mlflow

    Returns:
        None
    """

    logger.debug("Log mlflow metrics for model '%s'", model_specifier)

    mlflow_client.log_param(run_id=run_id, key="algorithm_type", value="Object Detection")

    if score_threshold is not None:
        mlflow_client.log_param(run_id=run_id, key="score_threshold", value=score_threshold)
    if nms_threshold is not None:
        mlflow_client.log_param(run_id=run_id, key="nms_threshold", value=nms_threshold)

    for bbox_size_type in BBoxSizeTypes.get_values_as_list(class_type=BBoxSizeTypes):
        for class_name, od_metric in metrics_dict[iou_threshold][bbox_size_type].items():
            mlflow_client.log_metric(
                run_id=run_id,
                key=f"{class_name}_TP_{bbox_size_type}",
                value=od_metric.TP,
                step=step,
            )
            mlflow_client.log_metric(
                run_id=run_id,
                key=f"{class_name}_FP_{bbox_size_type}",
                value=od_metric.FP,
                step=step,
            )
            mlflow_client.log_metric(
                run_id=run_id,
                key=f"{class_name}_FN_{bbox_size_type}",
                value=od_metric.FN,
                step=step,
            )
            mlflow_client.log_metric(
                run_id=run_id,
                key=f"{class_name}_COUNT_{bbox_size_type}",
                value=od_metric.COUNT,
                step=step,
            )
            mlflow_client.log_metric(
                run_id=run_id,
                key=f"{class_name}_RC_{bbox_size_type}",
                value=od_metric.RC,
                step=step,
            )
            mlflow_client.log_metric(
                run_id=run_id,
                key=f"{class_name}_PR_{bbox_size_type}",
                value=od_metric.PR,
                step=step,
            )
            mlflow_client.log_metric(
                run_id=run_id,
                key=f"{class_name}_F1_{bbox_size_type}",
                value=od_metric.F1,
                step=step,
            )
            mlflow_client.log_metric(
                run_id=run_id,
                key=f"{class_name}_AP_{bbox_size_type}",
                value=od_metric.AP,
                step=step,
            )


def log_false_positive_info(
    model_specifier: str,
    metric_image_info_dict: METRIC_IMAGE_INFO_TYPE,
) -> None:
    """
    TODO

    Args:
        model_specifier:
        metric_image_info_dict:

    Returns:
        None
    """

    for class_name, image_dict in metric_image_info_dict.items():
        for image_path, metric_image_info in image_dict.items():
            if metric_image_info.false_positive_annotation is not None:
                bounding_boxes = metric_image_info.false_positive_annotation.get_bounding_boxes(
                    include_segmentations=True
                )

                logger.debug(
                    "\nFALSE POSITIVE for model %s: \n"
                    "  - image-path: '%s' \n"
                    "  - image-annotation: %s \n"
                    "  - bounding_boxes:   %s \n",
                    model_specifier,
                    metric_image_info.false_positive_annotation.image_path,
                    metric_image_info.false_positive_annotation.annotation_path,
                    bounding_boxes,
                )

            if metric_image_info.false_negative_annotation is not None:
                bounding_boxes = metric_image_info.false_negative_annotation.get_bounding_boxes(
                    include_segmentations=True
                )

                logger.debug(
                    "\nFALSE NEGATIVE for model %s: \n"
                    "  - image-path:       "
                    "%s\n"
                    "  - image-annotation: "
                    "%s\n"
                    "  - bounding_boxes:   %s\n",
                    model_specifier,
                    metric_image_info.false_negative_annotation.image_path,
                    metric_image_info.false_negative_annotation.annotation_path,
                    bounding_boxes,
                )


def log_false_positive_info_to_tb(
    model_name: str,
    metric_image_info_dict: METRIC_IMAGE_INFO_TYPE,
    tb_logging_config: TensorboardLoggingConfig,
) -> None:
    """
    Writes evaluation metrics and images to tensorboard directory.

    Args:
        model_name: Name of the model
        metric_image_info_dict: Dictionary mapping of string to a image dictionary
        tb_logging_config: configuration object defining the behavior of logging the
                           false positive information to tensorboard

    Returns:
        None
    """

    timestamp = datetime.now().strftime("%Y-%m-%dT_%H-%M")

    tb_dir = os.path.join(
        tb_logging_config.tensorboard_dir.replace(FileNamePlaceholders.TIMESTAMP, timestamp),
        model_name,
    )
    writer = SummaryWriter(tb_dir) if tb_dir != "" else SummaryWriter()
    ensure_dir(file_path=tb_dir, verbose=True)

    logger.debug("Write evaluation metrics/images to tensorboard-dir: '{}'".format(tb_dir))

    img_directory_id_dict: Dict[str, int] = dict()

    for class_name, image_dict in metric_image_info_dict.items():
        for image_path, metric_image_info in image_dict.items():
            image_id, img_directory_id_dict = generate_img_id_map(
                image_path=image_path, img_directory_id_dict=img_directory_id_dict
            )

            if metric_image_info.ground_truth_annotation is not None:
                gt_count = len(
                    metric_image_info.ground_truth_annotation.get_bounding_boxes(
                        include_segmentations=True
                    )
                )
            else:
                gt_count = 0

            if metric_image_info.false_positive_annotation is not None:
                fp_count = len(
                    metric_image_info.false_positive_annotation.get_bounding_boxes(
                        include_segmentations=True
                    )
                )
            else:
                fp_count = 0

            if metric_image_info.false_negative_annotation is not None:
                fn_count = len(
                    metric_image_info.false_negative_annotation.get_bounding_boxes(
                        include_segmentations=True
                    )
                )
            else:
                fn_count = 0

            if gt_count > 0 or fp_count > 0 or fn_count > 0:
                writer.add_images(
                    tag=f"metric_image_info_{class_name}/"
                    f"{os.path.basename(image_path)}_"
                    f"ID_{image_id}_"
                    f"GT_{gt_count}_"
                    f"FP_{fp_count}_"
                    f"FN_{fn_count}",
                    img_tensor=__create_tf_image(
                        image_path=image_path,
                        metric_image_info=metric_image_info,
                        false_positive_image_size=tb_logging_config.false_positive_image_size,
                    ),
                    global_step=0,
                    dataformats="HWC",
                )

        writer.close()


def output_evaluation_results(
    model_metrics: ODModelEvaluationMetrics,
    iou_thresholds: List[float],
    score_threshold: Optional[float] = None,
    nms_threshold: Optional[float] = None,
    tensorboard_logging: Optional[TensorboardLoggingConfig] = None,
) -> None:
    """
    Generate logging output.
    - python logging
    - log object detection metrics to mlflow
    - visualize information about false positives and false negatives by logging
      images to tensorboard

    Args:
        model_metrics: An ODModelEvaluationMetrics object storing the information of an
                       evaluation computation
        iou_thresholds: Iou thresholds for which to output_evaluation_results. They will be
                        used to extract the information out of the model_metrics
        score_threshold: Optionally hand over the score threshold, indicating the score
                         threshold that has been used to filter predicted bounding boxes
        nms_threshold: Optionally hand over the nms threshold, indicating the nms
                       threshold that has been used to filter predicted bounding boxes
        tensorboard_logging: A TensorboardLoggingConfig object defining the behavior for logging
                             the visualizations of false-positives and false-negatives to
                             tensorboard

    Returns:
        None
    """

    for iou_threshold in iou_thresholds:
        metric_table = generate_metric_table(
            metrics_dict=model_metrics.metrics_dict,
            iou_threshold=iou_threshold,
        )

        score_string = f"{score_threshold:.2f}" if score_threshold is not None else "NONE"
        nms_string = f"{nms_threshold:.2f}" if nms_threshold is not None else "NONE"

        logger.info(
            "\n\n"
            " Evaluation result for "
            "model '%s', "
            "IOU= %.2f, "
            "SCORE= %s, "
            "NMS= %s: \n"
            "%s"
            "\n\n",
            model_metrics.model_specifier,
            iou_threshold,
            score_string,
            nms_string,
            metric_table.table,
        )

        log_od_metrics_to_mlflow(
            model_specifier=model_metrics.model_specifier,
            metrics_dict=model_metrics.metrics_dict,
            score_threshold=score_threshold,
            nms_threshold=nms_threshold,
            iou_threshold=iou_threshold,
        )

    log_false_positive_info(
        model_specifier=model_metrics.model_specifier,
        metric_image_info_dict=model_metrics.metrics_image_info_dict,
    )

    if tensorboard_logging is not None:
        log_false_positive_info_to_tb(
            model_name=model_metrics.model_specifier,
            metric_image_info_dict=model_metrics.metrics_image_info_dict,
            tb_logging_config=tensorboard_logging,
        )
