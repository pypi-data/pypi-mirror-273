# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

import logging
import math
import os
from unittest import main
from unittest.mock import MagicMock

import cv2
from pytest import fixture, mark
from pytest_mock import MockerFixture

from mlcvzoo_base.api.data.box import Box, compute_iou, euclidean_distance
from mlcvzoo_base.configuration.structs import ObjectDetectionBBoxFormats
from mlcvzoo_base.tests.unit_tests.test_template import TestTemplate

logger = logging.getLogger(__name__)


@fixture(scope="function")
def crop_img_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        "mlcvzoo_base.api.data.box.Box.crop_img",
        return_value=None,
    )


# TODO: add test that surrounding box is written to csv files
class TestAPIBox(TestTemplate):
    def test_box_constructor_error_xmin_bigger_xmax(self) -> None:
        with self.assertRaises(ValueError):
            Box(xmin=13, ymin=2, xmax=10, ymax=12)

    def test_box_constructor_error_ymin_bigger_ymax(self) -> None:
        with self.assertRaises(ValueError):
            Box(xmin=1, ymin=22, xmax=10, ymax=12)

    def test_box_width(self) -> None:
        assert Box(xmin=1, ymin=2, xmax=10, ymax=12).width == 9

    def test_box_height(self) -> None:
        assert Box(xmin=1, ymin=2, xmax=10, ymax=12).height == 10

    def test_box_as_array(self) -> None:
        box_array = Box(xmin=1, ymin=2, xmax=10, ymax=12).as_array()

        assert box_array[0] == 1
        assert box_array[1] == 2
        assert box_array[2] == 10
        assert box_array[3] == 12

    def test_box_translation(self) -> None:
        box = Box(xmin=1, ymin=2, xmax=10, ymax=12)
        box.translation(x=10, y=10)

        assert box.xmin == 11
        assert box.ymin == 12
        assert box.xmax == 20
        assert box.ymax == 22

    def test_new_center(self) -> None:
        box = Box(xmin=0, ymin=0, xmax=10, ymax=10)
        box.new_center(x=10, y=10)

        assert box.xmin == 5
        assert box.ymin == 5
        assert box.xmax == 15
        assert box.ymax == 15

    def test_box_scale(self) -> None:
        box = Box(xmin=10, ymin=10, xmax=100, ymax=100)

        box.scale(src_shape=(100, 100), dst_shape=(200, 200))

        assert box.xmin == 20
        assert box.ymin == 20
        assert box.xmax == 200
        assert box.ymax == 200

    def test_box_iou(self) -> None:
        assert (
            compute_iou(
                box_1=Box(xmin=0, ymin=0, xmax=100, ymax=100),
                box_2=Box(xmin=0, ymin=0, xmax=50, ymax=50),
            )
            == 0.25
        )

        # No overlap
        assert (
            compute_iou(
                box_1=Box(xmin=0, ymin=0, xmax=100, ymax=100),
                box_2=Box(xmin=101, ymin=101, xmax=200, ymax=200),
            )
            == 0.0
        )

    def test_box_euclidian_distance(self) -> None:
        e_dist = euclidean_distance(
            box_1=Box(xmin=0, ymin=0, xmax=100, ymax=100),
            box_2=Box(xmin=0, ymin=0, xmax=50, ymax=50),
        )

        assert math.isclose(a=e_dist, b=35.3553, abs_tol=0.0001)

    def test_box_scale_wrong_src_shape(self) -> None:
        box = Box(xmin=10, ymin=10, xmax=100, ymax=100)

        with self.assertRaises(ValueError):
            box.scale(src_shape=(-10, 100), dst_shape=(200, 200))

        with self.assertRaises(ValueError):
            box.scale(src_shape=(-10, -5), dst_shape=(200, 200))

        with self.assertRaises(ValueError):
            box.scale(src_shape=(110, 100), dst_shape=(200, 200))

    def test_box_scale_wrong_dst_shape(self) -> None:
        box = Box(xmin=10, ymin=10, xmax=100, ymax=100)

        with self.assertRaises(ValueError):
            box.scale(src_shape=(200, 200), dst_shape=(-10, 100))

        with self.assertRaises(ValueError):
            box.scale(src_shape=(200, 200), dst_shape=(-10, -5))

        with self.assertRaises(ValueError):
            box.scale(src_shape=(200, 200), dst_shape=(110, 100))

    def test_box_not_equal_other_instance_type(self) -> None:
        assert (Box(xmin=1, ymin=2, xmax=10, ymax=12) == 1) is False

    def test_box_init_format_based_assert_error(self) -> None:
        with self.assertRaises(ValueError):
            Box.init_format_based(box_format="Any", box_list=[1, 2, 10, 12])

    def test_box_init_format_based_XYXY(self) -> None:
        box = Box.init_format_based(
            box_format=ObjectDetectionBBoxFormats.XYXY, box_list=[1, 2, 10, 12]
        )

        assert box.xmin == 1
        assert box.ymin == 2
        assert box.xmax == 10
        assert box.ymax == 12

    def test_box_init_format_based_XYXY_correct_xmin(self) -> None:
        box = Box.init_format_based(
            box_format=ObjectDetectionBBoxFormats.XYXY, box_list=[-1, 2, 10, 12]
        )

        assert box.xmin == 0
        assert box.ymin == 2
        assert box.xmax == 10
        assert box.ymax == 12

    def test_box_init_format_based_XYXY_correct_ymin(self) -> None:
        box = Box.init_format_based(
            box_format=ObjectDetectionBBoxFormats.XYXY, box_list=[1, -2, 10, 12]
        )

        assert box.xmin == 1
        assert box.ymin == 0
        assert box.xmax == 10
        assert box.ymax == 12

    def test_box_init_format_based_XYWH(self) -> None:
        box = Box.init_format_based(
            box_format=ObjectDetectionBBoxFormats.XYWH, box_list=[1, 2, 10, 12]
        )

        assert box.xmin == 1
        assert box.ymin == 2
        assert box.xmax == 11
        assert box.ymax == 14

    def test_box_init_format_based_XYWH_correct_xmin(self) -> None:
        box = Box.init_format_based(
            box_format=ObjectDetectionBBoxFormats.XYWH, box_list=[-1, 2, 10, 12]
        )

        assert box.xmin == 0
        assert box.ymin == 2
        assert box.xmax == 10
        assert box.ymax == 14

    def test_box_init_format_based_XYWH_correct_ymin(self) -> None:
        box = Box.init_format_based(
            box_format=ObjectDetectionBBoxFormats.XYWH, box_list=[1, -2, 10, 12]
        )

        assert box.xmin == 1
        assert box.ymin == 0
        assert box.xmax == 11
        assert box.ymax == 12

    def test_box_init_format_based_XYWH_negative_width(self) -> None:
        with self.assertRaises(ValueError):
            Box.init_format_based(
                box_format=ObjectDetectionBBoxFormats.XYWH, box_list=[1, 2, -10, 12]
            )

    def test_box_init_format_based_XYWH_negative_height(self) -> None:
        with self.assertRaises(ValueError):
            Box.init_format_based(
                box_format=ObjectDetectionBBoxFormats.XYWH, box_list=[1, 2, 10, -12]
            )

    def test_box_init_format_based_XYXY_scaled(self) -> None:
        box = Box.init_format_based(
            box_format=ObjectDetectionBBoxFormats.XYXY,
            box_list=[10, 10, 100, 100],
            src_shape=(200, 200),
            dst_shape=(400, 400),
        )

        assert box.xmin == 20
        assert box.ymin == 20
        assert box.xmax == 200
        assert box.ymax == 200

    def test_box_to_list(self) -> None:
        box = Box(xmin=1, ymin=2, xmax=10, ymax=12)

        assert box.to_list() == [1, 2, 10, 12]

    def test_box_to_center(self) -> None:
        box = Box(xmin=1, ymin=2, xmax=10, ymax=12)

        assert box.center() == (
            1 + (10 - 1) * 0.5,
            2 + (12 - 2) * 0.5,
        )

    def test_box_crop_img(self) -> None:
        image = cv2.imread(os.path.join(self.project_root, "test_data/images/dummy_task/cars.jpg"))

        box = Box(
            xmin=10,
            ymin=10,
            xmax=110,
            ymax=210,
        )

        cropped_image = box.crop_img(frame=image, margin_x=0.01, margin_y=0.01)

        assert cropped_image is not None

        # cv2 stores images as matrix with the row index as y-axis and columns index as x-axis
        assert cropped_image.shape[0] == 204 and cropped_image.shape[1] == 102

    def test_box_crop_img_wrong_input_image(self) -> None:
        box = Box(
            xmin=10,
            ymin=10,
            xmax=100,
            ymax=100,
        )

        cropped_image = box.crop_img(frame=None, margin_x=0.01, margin_y=0.01)

        assert cropped_image is None

    def test_box_crop_img_margin_to_large(self) -> None:
        image = cv2.imread(os.path.join(self.project_root, "test_data/images/dummy_task/cars.jpg"))

        box = Box(
            xmin=10,
            ymin=10,
            xmax=100,
            ymax=100,
        )

        cropped_image = box.crop_img(frame=image, margin_x=1.0, margin_y=1.0)

        assert cropped_image is not None

    def test_box_crop_img_negative_margin(self) -> None:
        image = cv2.imread(os.path.join(self.project_root, "test_data/images/dummy_task/cars.jpg"))

        box = Box(
            xmin=10,
            ymin=10,
            xmax=100,
            ymax=100,
        )

        cropped_image = box.crop_img(frame=image, margin_x=-0.01, margin_y=-0.01)

        assert cropped_image is not None

    def test_box_color_hist(self) -> None:
        image = cv2.imread(os.path.join(self.project_root, "test_data/images/dummy_task/cars.jpg"))

        box = Box(
            xmin=10,
            ymin=10,
            xmax=100,
            ymax=100,
        )

        cropped_image = box.color_hist(frame=image, margin_x=-0.01, margin_y=-0.01)

        assert cropped_image is not None

    @mark.usefixtures("crop_img_mock")
    def test_box_color_hist_no_crop(self) -> None:
        image = cv2.imread(os.path.join(self.project_root, "test_data/images/dummy_task/cars.jpg"))

        box = Box(
            xmin=10,
            ymin=10,
            xmax=100,
            ymax=100,
        )

        cropped_image = box.color_hist(frame=image, margin_x=-0.01, margin_y=-0.01)

        assert cropped_image is None

    def test_to_dict(self) -> None:
        box: Box = Box(
            xmin=10,
            ymin=10,
            xmax=100,
            ymax=100,
        )

        assert box.to_dict() == {"xmin": 10, "ymin": 10, "xmax": 100, "ymax": 100}

    def test_to_json(self) -> None:
        box: Box = Box(
            xmin=10,
            ymin=10,
            xmax=100,
            ymax=100,
        )

        assert box.to_json() == {"xmin": 10, "ymin": 10, "xmax": 100, "ymax": 100}


if __name__ == "__main__":
    main()
