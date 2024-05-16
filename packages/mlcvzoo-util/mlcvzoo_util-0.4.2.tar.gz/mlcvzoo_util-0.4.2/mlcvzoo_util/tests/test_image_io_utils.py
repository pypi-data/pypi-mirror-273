# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

import logging
from unittest import main
from unittest.mock import MagicMock

from pytest import fixture, mark
from pytest_mock import MockerFixture
from test_template import TestTemplate

from mlcvzoo_util.image_io_utils import VideoLiveOutput

logger = logging.getLogger(__name__)


@fixture(scope="function")
def cv2_named_window(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        "cv2.namedWindow",
        return_value=None,
    )


class TestImageIOUtils(TestTemplate):
    @mark.usefixtures("cv2_named_window")
    def test_video_live_output_constructor(self) -> None:
        VideoLiveOutput()

    @mark.usefixtures("cv2_named_window")
    def test_video_live_output_constructor_mode(self) -> None:
        VideoLiveOutput(mode=VideoLiveOutput.MODE_GO)

    @mark.usefixtures("cv2_named_window")
    def test_video_live_output_constructor_mode_fail(self) -> None:
        with self.assertRaises(ValueError) as value_error:
            VideoLiveOutput(mode="other")

            assert (
                str(value_error) == "Invalid mode='other' "
                "has to be one of '['terminate', 'go', 'step']'"
            )


if __name__ == "__main__":
    main()
