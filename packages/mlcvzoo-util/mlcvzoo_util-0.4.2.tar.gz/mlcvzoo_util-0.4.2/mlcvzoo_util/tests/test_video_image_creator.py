# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

import copy
import logging
import os
import sys
from unittest import main
from unittest.mock import MagicMock

from mlcvzoo_base.utils.file_utils import get_file_list
from pytest import fixture, mark
from pytest_mock import MockerFixture
from test_template import TestTemplate

from mlcvzoo_util.video_image_creator.video_image_creator import VideoImageCreator
from mlcvzoo_util.video_image_creator.video_image_creator import (
    main as video_image_creator_main,
)

logger = logging.getLogger(__name__)


@fixture(scope="function")
def cv2_waitKey_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        "cv2.waitKey",
        return_value=ord("s"),
    )


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


class TestVideoImageCreator(TestTemplate):
    @mark.usefixtures(
        "cv2_waitKey_mock", "cv2_named_window", "cv2_resize_window", "cv2_imshow"
    )
    def test_video_image_creator_video_path(self) -> None:
        video_image_creator = VideoImageCreator(
            configuration=VideoImageCreator.create_configuration(
                yaml_config_path=os.path.join(
                    self.project_root,
                    "test_data",
                    "test_video_image_creator",
                    "test_video-image-creator_video-path.yaml",
                ),
                string_replacement_map=self.string_replacement_map,
            )
        )
        video_image_creator.run()

        written_video_images = get_file_list(
            input_dir=os.path.join(self.project_root, "test_data/test_video"),
            file_extension=".jpg",
        )

        assert len(written_video_images) == 10

    @mark.usefixtures(
        "cv2_waitKey_mock", "cv2_named_window", "cv2_resize_window", "cv2_imshow"
    )
    def test_video_image_creator_video_dir(self) -> None:
        video_image_creator = VideoImageCreator(
            configuration=VideoImageCreator.create_configuration(
                yaml_config_path=os.path.join(
                    self.project_root,
                    "test_data",
                    "test_video_image_creator",
                    "test_video-image-creator_video-dir.yaml",
                ),
                string_replacement_map=self.string_replacement_map,
            )
        )
        video_image_creator.run()

        written_video_images = get_file_list(
            input_dir=os.path.join(self.project_root, "test_data/test_video"),
            file_extension=".jpg",
        )

        assert len(written_video_images) == 10

    @mark.usefixtures(
        "cv2_waitKey_mock", "cv2_named_window", "cv2_resize_window", "cv2_imshow"
    )
    def test_video_image_creator_no_video_files(self) -> None:
        with self.assertRaises(ValueError):
            VideoImageCreator(
                configuration=VideoImageCreator.create_configuration(
                    yaml_config_path=os.path.join(
                        self.project_root,
                        "test_data",
                        "test_video_image_creator",
                        "test_video-image-creator_no-video-files.yaml",
                    ),
                    string_replacement_map=self.string_replacement_map,
                )
            )

    @mark.usefixtures(
        "cv2_waitKey_mock", "cv2_named_window", "cv2_resize_window", "cv2_imshow"
    )
    def test_video_image_creator_main(self):
        argv_copy = copy.deepcopy(sys.argv)

        sys.argv = [sys.argv[0]]

        sys.argv.extend(
            [
                os.path.join(
                    self.project_root,
                    "test_data/test_video_image_creator/",
                    "test_video-image-creator_video-path.yaml",
                ),
                "--replacement-config-path",
                self._gen_replacement_config(),
                "--log-dir",
                os.path.join(self.project_root, "test_output", "logs"),
                "--log-level",
                "DEBUG",
            ]
        )

        video_image_creator_main()

        sys.argv = argv_copy


if __name__ == "__main__":
    main()
