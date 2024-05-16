# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

import copy
import logging
import os
import shutil
import sys
from typing import NamedTuple
from unittest import main
from unittest.mock import MagicMock

from pytest import fixture, mark, raises
from pytest_mock import MockerFixture
from test_template import TestTemplate

from mlcvzoo_util.image_io_utils import VideoLiveOutput
from mlcvzoo_util.pre_annotation_tool.pre_annotation_tool import (
    main as pre_annotation_tool_main,
)

logger = logging.getLogger(__name__)


class ProcessResult(NamedTuple):
    returncode: int


@fixture(scope="function")
def cv2_named_window(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        "cv2.namedWindow",
        return_value=None,
    )


@fixture(scope="function")
def cv2_resize_window(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        "cv2.resizeWindow",
        return_value=None,
    )


@fixture(scope="function")
def cv2_imshow(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        "cv2.imshow",
        return_value=None,
    )


@fixture(scope="function")
def video_live_output_mock(mocker: MockerFixture) -> str:
    mocker.patch(
        "cv2.resizeWindow",
        return_value=None,
    )
    mocker.patch(
        "cv2.namedWindow",
        return_value=None,
    )
    mocker.patch(
        "cv2.imshow",
        return_value=None,
    )

    return mocker.patch(
        target="mlcvzoo_util.pre_annotation_tool.pre_annotation_tool.VideoLiveOutput",
        return_value=VideoLiveOutput(mode=VideoLiveOutput.MODE_GO),
    )


@fixture(scope="function")
def subprocess_run_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        "mlcvzoo_util.cvat_annotation_handler.utils.subprocess.run",
        return_value=ProcessResult(0),
    )


@fixture(scope="function")
def set_inference_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        "mlcvzoo_base.configuration.model_config.ModelConfig.set_inference",
        return_value=None,
    )


class TestPreAnnotationTool(TestTemplate):
    def __copy_test_data(self):
        original_zip_path = os.path.join(
            self.project_root,
            "test_data/test_cvat_annotation_handler/test_download/mlcvzoo-test.zip",
        )

        os.makedirs(
            os.path.join(self.project_root, "test_output/pre_annotation_tool"),
            exist_ok=True,
        )

        copy_download_zip_path = os.path.join(
            self.project_root,
            "test_output/pre_annotation_tool/mlcvzoo-test_download.zip",
        )

        copy_upload_zip_path = os.path.join(
            self.project_root,
            "test_output/pre_annotation_tool/mlcvzoo-test_upload.zip",
        )

        shutil.copy(original_zip_path, copy_download_zip_path)
        shutil.copy(original_zip_path, copy_upload_zip_path)

    @mark.usefixtures("set_inference_mock", "subprocess_run_mock")
    def test_pre_annotation_tool(self):
        self.__copy_test_data()

        argv_copy = copy.deepcopy(sys.argv)

        sys.argv = [sys.argv[0]]

        sys.argv = [
            os.path.join(
                self.project_root,
                "mlcvzoo_util/pre_annotation_tool/pre_annotation_tool.py",
            ),
            os.path.join(
                self.project_root,
                "test_data/test_pre_annotation_tool/" "test_pre_annotation_tool.yaml",
            ),
            "--replacement-config-path",
            self._gen_replacement_config(),
            "--log-dir",
            os.path.join(self.project_root, "test_output", "logs"),
            "--log-level",
            "DEBUG",
        ]

        pre_annotation_tool_main()

        sys.argv = argv_copy

    @mark.usefixtures(
        "video_live_output_mock",
        "cv2_named_window",
        "cv2_resize_window",
        "cv2_imshow",
        "subprocess_run_mock",
        "set_inference_mock",
    )
    def test_pre_annotation_tool_with_visualization(self):
        self.__copy_test_data()

        argv_copy = copy.deepcopy(sys.argv)

        sys.argv = [
            os.path.join(
                self.project_root,
                "mlcvzoo_util/pre_annotation_tool/pre_annotation_tool.py",
            ),
            os.path.join(
                self.project_root,
                "test_data/test_pre_annotation_tool",
                "test_pre_annotation_tool_with_visualization.yaml",
            ),
            "--replacement-config-path",
            self._gen_replacement_config(),
            "--log-level",
            "DEBUG",
        ]

        pre_annotation_tool_main()

        sys.argv = argv_copy

    @mark.usefixtures(
        "video_live_output_mock",
        "cv2_named_window",
        "cv2_resize_window",
        "cv2_imshow",
        "subprocess_run_mock",
        "set_inference_mock",
    )
    def test_pre_annotation_tool_wrong_model(self):
        self.__copy_test_data()

        argv_copy = copy.deepcopy(sys.argv)

        sys.argv = [
            os.path.join(
                self.project_root,
                "mlcvzoo_util/pre_annotation_tool/pre_annotation_tool.py",
            ),
            os.path.join(
                self.project_root,
                "test_data/test_pre_annotation_tool/"
                "test_pre_annotation_tool_wrong_model.yaml",
            ),
            "--replacement-config-path",
            self._gen_replacement_config(),
            "--log-level",
            "DEBUG",
        ]

        with self.assertRaises(ValueError) as value_error:
            pre_annotation_tool_main()

            assert (
                str(value_error) == "This evaluation can only be used with models "
                "that inherit from 'mlcvzoo.api.model.ObjectDetectionModel'"
            )

        sys.argv = argv_copy


if __name__ == "__main__":
    main()
