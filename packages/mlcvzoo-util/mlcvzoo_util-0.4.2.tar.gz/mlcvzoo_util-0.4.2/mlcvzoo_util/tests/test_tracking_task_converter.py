# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""
Tests for the LabelStudioTrackingTaskConverter
"""


import argparse
import logging
import os
from unittest import main, mock
from unittest.mock import MagicMock

from parametrize import parametrize
from test_template import TestTemplate

from mlcvzoo_util.ls_tracking_task_converter.ls_tracking_task_converter import (
    LabelStudioTrackingTaskConverter,
)
from mlcvzoo_util.ls_tracking_task_converter.ls_tracking_task_converter import (
    main as tracking_task_converter_main,
)

logger = logging.getLogger(__name__)


class TestLabelStudioTrackingTaskConverter(TestTemplate):
    """
    Tests for the LabelStudioTrackingTaskConverter
    """

    def setUp(self) -> None:
        """
        Setup file paths.
        """

        super().setUp()

        self.video_path = os.path.join(
            self.project_root,
            "test_data",
            "test_video.mp4",
        )
        self.tracking_annotations_path = os.path.join(
            self.project_root,
            "test_data",
            "test_tracking_task_converter",
            "tracking_annotations.json",
        )
        self.image_archive_path = os.path.join(
            self.project_root,
            "test_data",
            "test_tracking_task_converter",
            "image_archive.zip",
        )
        self.annotations_path = os.path.join(
            self.project_root,
            "test_data",
            "test_tracking_task_converter",
            "annotations.json",
        )

    def test_video_path_does_not_exist(self) -> None:
        """
        Test that an exception is raised, if the video file does not exist.
        """

        with self.assertRaisesRegex(ValueError, "Path to video '.*' does not exist."):
            LabelStudioTrackingTaskConverter(
                video_path=os.path.join(
                    self.project_root,
                    "test_data",
                    "test_video_invalid.mp4",
                ),
                tracking_annotations_path=self.tracking_annotations_path,
                image_archive_path=self.image_archive_path,
                annotations_path=self.annotations_path,
            )

    def test_tracking_annotations_path_does_not_exist(self) -> None:
        """
        Test that an exception is raised, if the file for the tracking annotations does not exist.
        """

        with self.assertRaisesRegex(
            ValueError, "Path to tracking annotations '.*' does not exist."
        ):
            LabelStudioTrackingTaskConverter(
                video_path=self.video_path,
                tracking_annotations_path=os.path.join(
                    self.project_root,
                    "test_data",
                    "test_tracking_task_converter",
                    "tracking_annotations_invalid.json",
                ),
                image_archive_path=self.image_archive_path,
                annotations_path=self.annotations_path,
            )

    def test_parse_video_specs_invalid_video(self) -> None:
        """
        Test that an exception is raised, if the video file is not valid.
        """

        with self.assertRaisesRegex(RuntimeError, "Could not open video '.*'"):
            tracking_converter = LabelStudioTrackingTaskConverter(
                video_path=self.tracking_annotations_path,
                tracking_annotations_path=self.tracking_annotations_path,
                image_archive_path=self.image_archive_path,
                annotations_path=self.annotations_path,
            )

            tracking_converter._parse_video_specs()

    def test_parse_video_specs(self) -> None:
        """
        Test that the video specs are parsed correctly.
        """

        tracking_converter = LabelStudioTrackingTaskConverter(
            video_path=self.video_path,
            tracking_annotations_path=self.tracking_annotations_path,
            image_archive_path=self.image_archive_path,
            annotations_path=self.annotations_path,
        )

        tracking_converter._parse_video_specs()

        self.assertEqual(tracking_converter.video_specs.width, 374)
        self.assertEqual(tracking_converter.video_specs.height, 500)
        self.assertEqual(tracking_converter.video_specs.frame_count, 10)
        self.assertEqual(tracking_converter.video_specs.frame_rate, 2.0)

    def test_build_image_filename(self) -> None:
        """
        Test that filenames for the image archive are built correctly.
        """

        tracking_converter = LabelStudioTrackingTaskConverter(
            video_path=self.video_path,
            tracking_annotations_path=self.tracking_annotations_path,
            image_archive_path=self.image_archive_path,
            annotations_path=self.annotations_path,
        )

        tracking_converter._parse_video_specs()

        self.assertEqual(
            tracking_converter._build_image_filename(0), "test_video_00.png"
        )
        self.assertEqual(
            tracking_converter._build_image_filename(9), "test_video_09.png"
        )

    @parametrize(
        "video_name",
        [
            ("test_video.mp4",),
            ("test_video_2.mp4",),
        ],
    )
    def test_find_task(self, video_name) -> None:
        """
        Test that the correct task is returned.
        """

        tracking_converter = LabelStudioTrackingTaskConverter(
            video_path=os.path.join(
                self.project_root,
                "test_data",
                video_name,
            ),
            tracking_annotations_path=self.tracking_annotations_path,
            image_archive_path=self.image_archive_path,
            annotations_path=self.annotations_path,
        )

        task = tracking_converter._find_task()
        self.assertEqual(task["file_upload"], video_name)

    @parametrize(
        "tracking_annotations_file,error_message_regex",
        [
            (
                "tracking_annotations_empty.json",
                "Invalid annotation file. Task for video 'test_video.mp4' is missing.",
            ),
            (
                "tracking_annotations_no_annotations.json",
                "Invalid task. Key annotations is missing or is empty.",
            ),
            (
                "tracking_annotations_no_result.json",
                "Invalid task. Key annotations.result is missing or is empty.",
            ),
            (
                "tracking_annotations_wrong_frame_count.json",
                "Invalid task.",
            ),
            (
                "tracking_annotations_no_labels.json",
                "Invalid task. Key annotations.result.value.labels is missing or is empty.",
            ),
            (
                "tracking_annotations_no_sequence.json",
                "Invalid task. Key annotations.result.value.sequence is missing or is empty.",
            ),
            (
                "tracking_annotations_no_file_upload.json",
                "Invalid task. Key file_upload is missing for a task.",
            ),
            (
                "tracking_annotations_task_missing.json",
                "Invalid annotation file. Task for video 'test_video.mp4' is missing.",
            ),
            (
                "tracking_annotations_wrong_annotation_format.json",
                "Annotation must contain keys 'frame', 'time', 'x', 'y', 'width', 'height' and "
                "'rotation'.",
            ),
        ],
    )
    def test_parse_tracking_annotations_file_invalid_annotations_file(
        self, tracking_annotations_file, error_message_regex
    ) -> None:
        """
        Test that exceptions are raised if the tracking annotations are invalid.
        """

        with self.assertRaisesRegex(ValueError, error_message_regex):
            tracking_converter = LabelStudioTrackingTaskConverter(
                video_path=self.video_path,
                tracking_annotations_path=os.path.join(
                    self.project_root,
                    "test_data",
                    "test_tracking_task_converter",
                    tracking_annotations_file,
                ),
                image_archive_path=self.image_archive_path,
                annotations_path=self.annotations_path,
            )

            tracking_converter._parse_video_specs()
            tracking_converter._parse_tracking_annotations_file()

    def test_parse_tracking_annotations_file(self) -> None:
        """
        Test that the tracking annotations are parsed correctly.
        """

        tracking_converter = LabelStudioTrackingTaskConverter(
            video_path=self.video_path,
            tracking_annotations_path=self.tracking_annotations_path,
            image_archive_path=self.image_archive_path,
            annotations_path=self.annotations_path,
        )

        tracking_converter._parse_video_specs()

        self.assertEqual(len(tracking_converter.annotations), 0)

        tracking_converter._parse_tracking_annotations_file()

        self.assertEqual(len(tracking_converter.annotations), 3)
        self.assertIn(0, tracking_converter.annotations)
        self.assertIn(1, tracking_converter.annotations)
        self.assertIn(2, tracking_converter.annotations)
        self.assertEqual(len(tracking_converter.annotations[0]), 2)
        self.assertEqual(len(tracking_converter.annotations[1]), 1)
        self.assertEqual(len(tracking_converter.annotations[2]), 1)

    @mock.patch(
        "mlcvzoo_util.ls_tracking_task_converter.ls_tracking_task_converter.json.dump"
    )
    def test_save_annotations(self, json_dump_mock) -> None:
        """
        Test that the parsed tracking annotations are saved correctly.
        """

        tracking_converter = LabelStudioTrackingTaskConverter(
            video_path=self.video_path,
            tracking_annotations_path=self.tracking_annotations_path,
            image_archive_path=self.image_archive_path,
            annotations_path=self.annotations_path,
        )

        # we want to mock open to prevent save_annotations to create a file
        # but open must return the correct data for the read in parse_annotations
        tracking_converter._parse_video_specs()
        tracking_converter._parse_tracking_annotations_file()
        with mock.patch(
            "mlcvzoo_util.ls_tracking_task_converter.ls_tracking_task_converter.open",
            mock.mock_open(),
        ):
            tracking_converter._save_annotations()

        data = json_dump_mock.call_args.kwargs["obj"]

        # assertCountEqual actually also checks equality of items
        self.assertCountEqual(
            data,
            [
                {
                    "annotations": [
                        {
                            "result": [
                                {
                                    "original_width": 374,
                                    "original_height": 500,
                                    "image_rotation": 0,
                                    "value": {
                                        "x": 42,
                                        "y": 42,
                                        "width": 42,
                                        "height": 42,
                                        "rotation": 0,
                                        "rectanglelabels": ["LabelA"],
                                    },
                                    "from_name": "label",
                                    "to_name": "image",
                                    "type": "rectanglelabels",
                                    "origin": "manual",
                                },
                                {
                                    "original_width": 374,
                                    "original_height": 500,
                                    "image_rotation": 0,
                                    "value": {
                                        "x": 84,
                                        "y": 84,
                                        "width": 84,
                                        "height": 84,
                                        "rotation": 0,
                                        "rectanglelabels": ["LabelB"],
                                    },
                                    "from_name": "label",
                                    "to_name": "image",
                                    "type": "rectanglelabels",
                                    "origin": "manual",
                                },
                            ]
                        }
                    ],
                    "data": {"image": "test_video_00.png"},
                },
                {
                    "annotations": [
                        {
                            "result": [
                                {
                                    "original_width": 374,
                                    "original_height": 500,
                                    "image_rotation": 0,
                                    "value": {
                                        "x": 42,
                                        "y": 42,
                                        "width": 42,
                                        "height": 42,
                                        "rotation": 0,
                                        "rectanglelabels": ["LabelA"],
                                    },
                                    "from_name": "label",
                                    "to_name": "image",
                                    "type": "rectanglelabels",
                                    "origin": "manual",
                                },
                            ]
                        }
                    ],
                    "data": {"image": "test_video_01.png"},
                },
                {
                    "annotations": [
                        {
                            "result": [
                                {
                                    "original_width": 374,
                                    "original_height": 500,
                                    "image_rotation": 0,
                                    "value": {
                                        "x": 84,
                                        "y": 84,
                                        "width": 84,
                                        "height": 84,
                                        "rotation": 0,
                                        "rectanglelabels": ["LabelB"],
                                    },
                                    "from_name": "label",
                                    "to_name": "image",
                                    "type": "rectanglelabels",
                                    "origin": "manual",
                                },
                            ]
                        }
                    ],
                    "data": {"image": "test_video_02.png"},
                },
            ],
        )

    @mock.patch(
        "mlcvzoo_util.ls_tracking_task_converter.ls_tracking_task_converter.zipfile.ZipFile",
        autospec=True,
    )
    @mock.patch(
        "mlcvzoo_util.ls_tracking_task_converter.ls_tracking_task_converter.cv2.imwrite"
    )
    def test_extract_images(self, cv2_imwrite_mock, zipfile_mock) -> None:
        """
        Test that the correct video frames are saved in the image archive.
        """

        zipfile_mock.return_value.__enter__.return_value.write = MagicMock()
        zipfile_write_mock = zipfile_mock.return_value.__enter__.return_value.write

        tracking_converter = LabelStudioTrackingTaskConverter(
            video_path=self.video_path,
            tracking_annotations_path=self.tracking_annotations_path,
            image_archive_path=self.image_archive_path,
            annotations_path=self.annotations_path,
        )

        tracking_converter._parse_video_specs()
        tracking_converter._parse_tracking_annotations_file()
        tracking_converter._extract_images()

        # assert cv2.imwrite
        self.assertEqual(len(cv2_imwrite_mock.call_args_list), 3)
        self.assertIn("test_video_00.png", cv2_imwrite_mock.call_args_list[0].args[0])
        self.assertIn("test_video_01.png", cv2_imwrite_mock.call_args_list[1].args[0])
        self.assertIn("test_video_02.png", cv2_imwrite_mock.call_args_list[2].args[0])

        # assert zipfile.ZipFile.write
        self.assertEqual(len(zipfile_write_mock.call_args_list), 3)
        self.assertIn("test_video_00.png", zipfile_write_mock.call_args_list[0].args[0])
        self.assertEqual(
            zipfile_write_mock.call_args_list[0].args[1], "test_video_00.png"
        )
        self.assertIn("test_video_01.png", zipfile_write_mock.call_args_list[1].args[0])
        self.assertEqual(
            zipfile_write_mock.call_args_list[1].args[1], "test_video_01.png"
        )
        self.assertIn("test_video_02.png", zipfile_write_mock.call_args_list[2].args[0])
        self.assertEqual(
            zipfile_write_mock.call_args_list[2].args[1], "test_video_02.png"
        )

    def test_extract_images_invalid_video(self) -> None:
        """
        Test that an exception is raised, if the video file is not valid.
        """

        with self.assertRaisesRegex(RuntimeError, "Could not open video '.*'"):
            tracking_converter = LabelStudioTrackingTaskConverter(
                video_path=self.tracking_annotations_path,
                tracking_annotations_path=self.tracking_annotations_path,
                image_archive_path=self.image_archive_path,
                annotations_path=self.annotations_path,
            )

            tracking_converter._extract_images()

    @mock.patch(
        "mlcvzoo_util.ls_tracking_task_converter.ls_tracking_task_converter"
        ".LabelStudioTrackingTaskConverter._parse_video_specs"
    )
    @mock.patch(
        "mlcvzoo_util.ls_tracking_task_converter.ls_tracking_task_converter"
        ".LabelStudioTrackingTaskConverter._parse_tracking_annotations_file"
    )
    @mock.patch(
        "mlcvzoo_util.ls_tracking_task_converter.ls_tracking_task_converter"
        ".LabelStudioTrackingTaskConverter._extract_images"
    )
    @mock.patch(
        "mlcvzoo_util.ls_tracking_task_converter.ls_tracking_task_converter."
        "LabelStudioTrackingTaskConverter._save_annotations"
    )
    def test_run(
        self,
        save_annotations_mock,
        extract_images_mock,
        parse_annotations_mock,
        get_video_specs_mock,
    ) -> None:
        """
        Test that the correct methods are called
        """

        tracking_converter = LabelStudioTrackingTaskConverter(
            video_path=self.video_path,
            tracking_annotations_path=self.tracking_annotations_path,
            image_archive_path=self.image_archive_path,
            annotations_path=self.annotations_path,
        )

        tracking_converter.run()

        self.assertEqual(get_video_specs_mock.called, True)
        self.assertEqual(parse_annotations_mock.called, True)
        self.assertEqual(extract_images_mock.called, True)
        self.assertEqual(save_annotations_mock.called, True)

    @mock.patch(
        "mlcvzoo_util.ls_tracking_task_converter.ls_tracking_task_converter"
        ".LabelStudioTrackingTaskConverter"
    )
    @mock.patch(
        "mlcvzoo_util.ls_tracking_task_converter.ls_tracking_task_converter.parse_args"
    )
    def test_main(
        self, parse_args_mock, label_studio_tracking_task_converter_mock
    ) -> None:
        """
        Test the main function instantiates the LabelStudioTrackingTaskConverter with the correct
        parameters.
        """

        parse_args_mock.return_value = argparse.Namespace(
            video_path=self.video_path,
            tracking_annotations_path=self.tracking_annotations_path,
            image_archive_path=self.image_archive_path,
            annotations_path=self.annotations_path,
        )

        tracking_task_converter_main()

        self.assertDictEqual(
            label_studio_tracking_task_converter_mock.call_args.kwargs,
            {
                "video_path": self.video_path,
                "tracking_annotations_path": self.tracking_annotations_path,
                "image_archive_path": self.image_archive_path,
                "annotations_path": self.annotations_path,
            },
        )


if __name__ == "__main__":
    main()
