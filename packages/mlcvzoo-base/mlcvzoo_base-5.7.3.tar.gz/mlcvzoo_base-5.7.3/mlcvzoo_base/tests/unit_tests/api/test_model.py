# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

# pylint: disable=abstract-class-instantiated

import logging
from unittest import main, mock

from mlcvzoo_base.api.model import (
    ClassificationModel,
    Model,
    OCRModel,
    SegmentationModel,
)
from mlcvzoo_base.api.structs import Runtime
from mlcvzoo_base.tests.unit_tests.test_template import TestTemplate

logger = logging.getLogger(__name__)

RUNTIMES = [
    Runtime.DEFAULT,
    Runtime.ONNXRUNTIME,
    Runtime.ONNXRUNTIME_FLOAT16,
    Runtime.TENSORRT,
    Runtime.TENSORRT_INT8,
]


class TestMLCVZooModel(TestTemplate):
    def test_model_runtime_default_value(self) -> None:
        """Test that the default value is DEFAULT."""
        # Make the abstract class instantiable
        Model.__abstractmethods__ = set()
        model = Model(None, False)

        assert model.runtime == Runtime.DEFAULT

    def test_model_runtime_values(self) -> None:
        """Test that the runtime value is saved."""
        # Make the abstract class instantiable
        Model.__abstractmethods__ = set()

        for runtime in RUNTIMES:
            model = Model(None, False, runtime)
            assert model.runtime == runtime

    def test_model_runtime_invalid_value(self) -> None:
        """Test that an exception is raised, if an invalid runtime is provided."""
        # Make the abstract class instantiable
        Model.__abstractmethods__ = set()

        with self.assertRaisesRegex(ValueError, "Runtime 'FOOBAR' is not supported."):
            Model(None, False, "FOOBAR")


class TestMLCVZooClassificationModel(TestTemplate):
    @mock.patch("mlcvzoo_base.api.model.Model.__init__")
    def test_model_runtime_default_value(self, model_init) -> None:
        """Test that the constructor of Model is called with the DEFAULT runtime if no runtime is provided."""

        # Make the abstract class instantiable
        ClassificationModel.__abstractmethods__ = set()
        ClassificationModel(None, None, False)

        model_init.assert_called_once_with(
            mock.ANY,
            configuration=None,
            init_for_inference=False,
            runtime=Runtime.DEFAULT,
        )

    @mock.patch("mlcvzoo_base.api.model.Model.__init__")
    def test_model_runtime_values(self, model_init) -> None:
        """Test that the constructor of Model is called with the correct runtime."""

        # Make the abstract class instantiable
        ClassificationModel.__abstractmethods__ = set()

        for runtime in RUNTIMES:
            model_init.reset_mock()
            ClassificationModel(None, None, False, runtime)
            model_init.assert_called_once_with(
                mock.ANY,
                configuration=None,
                init_for_inference=False,
                runtime=runtime,
            )


class TestMLCVZooSegmentationModel(TestTemplate):
    @mock.patch("mlcvzoo_base.api.model.Model.__init__")
    def test_model_runtime_default_value(self, model_init) -> None:
        """Test that the constructor of Model is called with the DEFAULT runtime if no runtime is provided."""

        # Make the abstract class instantiable
        SegmentationModel.__abstractmethods__ = set()
        SegmentationModel(None, None, False)

        model_init.assert_called_once_with(
            mock.ANY,
            configuration=None,
            init_for_inference=False,
            runtime=Runtime.DEFAULT,
        )

    @mock.patch("mlcvzoo_base.api.model.Model.__init__")
    def test_model_runtime_values(self, model_init) -> None:
        """Test that the constructor of Model is called with the correct runtime."""

        # Make the abstract class instantiable
        SegmentationModel.__abstractmethods__ = set()

        for runtime in RUNTIMES:
            model_init.reset_mock()
            SegmentationModel(None, None, False, runtime)
            model_init.assert_called_once_with(
                mock.ANY,
                configuration=None,
                init_for_inference=False,
                runtime=runtime,
            )


class TestMLCVZooOCRModel(TestTemplate):
    @mock.patch("mlcvzoo_base.api.model.Model.__init__")
    def test_model_runtime_default_value(self, model_init) -> None:
        """Test that the constructor of Model is called with the DEFAULT runtime if no runtime is provided."""

        # Make the abstract class instantiable
        OCRModel.__abstractmethods__ = set()
        OCRModel(None, False)

        model_init.assert_called_once_with(
            mock.ANY,
            configuration=None,
            init_for_inference=False,
            runtime=Runtime.DEFAULT,
        )

    @mock.patch("mlcvzoo_base.api.model.Model.__init__")
    def test_model_runtime_values(self, model_init) -> None:
        """Test that the constructor of Model is called with the correct runtime."""

        # Make the abstract class instantiable
        OCRModel.__abstractmethods__ = set()

        for runtime in RUNTIMES:
            model_init.reset_mock()
            OCRModel(None, False, runtime)
            model_init.assert_called_once_with(
                mock.ANY,
                configuration=None,
                init_for_inference=False,
                runtime=runtime,
            )


if __name__ == "__main__":
    main()
