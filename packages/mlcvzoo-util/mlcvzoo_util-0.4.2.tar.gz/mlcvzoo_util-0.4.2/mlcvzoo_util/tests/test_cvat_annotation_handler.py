# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

import copy
import logging
import os
import shlex
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET_xml
from pathlib import Path
from typing import NamedTuple
from unittest import main
from unittest.mock import MagicMock

import pytest
from mlcvzoo_base.utils.file_utils import extract_zip_data
from pytest import fixture
from pytest_mock import MockerFixture
from test_template import TestTemplate

from mlcvzoo_util.cvat_annotation_handler.configuration import (
    CVATCLIConfig,
    CVATTaskDumpConfig,
    CVATTaskInfoConfig,
    CVATTaskUploadConfig,
)
from mlcvzoo_util.cvat_annotation_handler.cvat_annotation_handler import (
    CVATAnnotationHandler,
)
from mlcvzoo_util.cvat_annotation_handler.cvat_annotation_handler import (
    main as cvat_annotation_handler_main,
)
from mlcvzoo_util.cvat_annotation_handler.cvat_dumper import CVATDumper
from mlcvzoo_util.cvat_annotation_handler.cvat_uploader import PascalVOCUploader

logger = logging.getLogger(__name__)


def _xml_equal(xml_path_1: str, xml_path_2: str) -> bool:
    """
    Helper for comparison of two XML trees

    Args:
        xml_path_1: path to one xml file
        xml_path_2: path to the other xml file

    Returns:
        True if xml trees are identical, else False.
    """

    tree_1 = ET_xml.parse(xml_path_1)
    root_1 = tree_1.getroot()

    tree_2 = ET_xml.parse(xml_path_2)
    root_2 = tree_2.getroot()

    return _xml_root_compare(root_1=root_1, root_2=root_2)


def _xml_root_compare(root_1: ET_xml.Element, root_2: ET_xml.Element) -> bool:
    """
    Recursive helper function that compares tags and attributes of a tree and
     calls itself for each child.
    Args:
        root_1: xml.etree.ElementTree.Element object
        root_2: xml.etree.ElementTree.Element object

    Returns:
        True if trees are identical, else False.

    """

    if root_1.tag == root_2.tag:
        # NOTE: The local and gitlab-ci "path" tag are different, but are
        #       not relevant for this test
        if root_1.tag == "path":
            result = True
        elif root_1.tag == root_2.tag and root_1.text == root_2.text:
            result = True

            for index, child_1 in enumerate(root_1):
                if len(root_2) > index:
                    child_2 = root_2[index]
                    result = result and _xml_root_compare(child_1, child_2)
                else:
                    # If both roots do have the same length, they are not equal
                    result = False
                    break
        else:
            result = False
    else:
        result = False

    return result


class ProcessResult(NamedTuple):
    returncode: int


@fixture(scope="function")
def subprocess_run_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        "mlcvzoo_util.cvat_annotation_handler.utils.subprocess.run",
        return_value=ProcessResult(0),
    )


@fixture(scope="function")
def subprocess_run_failed_1_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        "mlcvzoo_util.cvat_annotation_handler.utils.subprocess.run",
        return_value=ProcessResult(1),
    )


@fixture(scope="function")
def os_path_isdir_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        "os.path.isdir",
        return_value=True,
    )


@fixture(scope="function")
def os_path_isdir_not_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        "os.path.isdir",
        return_value=False,
    )


@fixture(scope="function")
def shutil_rmtree_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        "shutil.rmtree",
    )


@fixture(scope="function")
def getpass_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        "mlcvzoo_util.cvat_annotation_handler.configuration.getpass",
        return_value="PASSWORD",
    )


class TestCVATAnnotationHandler(TestTemplate):
    def setUp(self) -> None:
        TestTemplate.setUp(self)
        self.string_replacement_map["HOME"] = str(Path.home())

    def tearDown(self) -> None:
        shutil.rmtree(
            path=os.path.join(
                self.project_root, "test_output/test_cvat_annotation_handler"
            ),
            ignore_errors=True,
        )

    def test_cvat_annotation_handler_correct_base_command(self):
        cvat_cli_config = CVATCLIConfig(
            cli_path="CVAT_DIR/utils/cli/cli.py",
            server_host="http://localhost",
            server_port=8080,
            disable_ssl_verify=True,
            auth="USERNAME:PASSWORD",
        )

        expected_base_command = (
            f"{sys.executable} "
            "CVAT_DIR/utils/cli/cli.py "
            "--server-host http://localhost "
            "--server-port 8080 "
            "--auth USERNAME:PASSWORD"
        )

        assert cvat_cli_config.create_base_command_string() == expected_base_command

    def test_cvat_annotation_handler_correct_base_command_from_password_file(self):
        cvat_cli_config = CVATCLIConfig(
            cli_path="CVAT_DIR/utils/cli/cli.py",
            server_host="http://localhost",
            server_port=8080,
            disable_ssl_verify=True,
            auth="USERNAME",
            password_path=os.path.join(
                self.project_root,
                "test_data/test_cvat_annotation_handler/cvat_password.txt",
            ),
        )

        expected_base_command = (
            f"{sys.executable} "
            "CVAT_DIR/utils/cli/cli.py "
            "--server-host http://localhost "
            "--server-port 8080 "
            "--auth USERNAME:PASSWORD"
        )

        assert cvat_cli_config.create_base_command_string() == expected_base_command

    def test_cvat_annotation_handler_correct_base_command_password_file_not_exist(self):
        cvat_cli_config = CVATCLIConfig(
            cli_path="CVAT_DIR/utils/cli/cli.py",
            server_host="http://localhost",
            server_port=8080,
            disable_ssl_verify=True,
            auth="USERNAME",
            password_path="NO_PATH",
        )

        expected_base_command = (
            f"{sys.executable} "
            "CVAT_DIR/utils/cli/cli.py "
            "--server-host http://localhost "
            "--server-port 8080 "
            "--auth USERNAME"
        )

        assert cvat_cli_config.create_base_command_string() == expected_base_command

    @pytest.mark.usefixtures("getpass_mock")
    def test_cvat_annotation_handler_correct_base_command_password_input(self):
        cvat_cli_config = CVATCLIConfig(
            cli_path="CVAT_DIR/utils/cli/cli.py",
            server_host="http://localhost",
            server_port=8080,
            disable_ssl_verify=True,
            auth="USERNAME",
        )

        expected_base_command = (
            f"{sys.executable} "
            "CVAT_DIR/utils/cli/cli.py "
            "--server-host http://localhost "
            "--server-port 8080 "
            "--auth USERNAME:PASSWORD"
        )

        assert cvat_cli_config.create_base_command_string() == expected_base_command

    def test_cvat_annotation_handler_correct_base_command_no_port(self):
        cvat_cli_config = CVATCLIConfig(
            cli_path="CVAT_DIR/utils/cli/cli.py",
            server_host="http://localhost",
            disable_ssl_verify=True,
            auth="USERNAME:PASSWORD",
        )

        expected_base_command = (
            f"{sys.executable} "
            "CVAT_DIR/utils/cli/cli.py "
            "--server-host http://localhost "
            "--auth USERNAME:PASSWORD"
        )

        assert cvat_cli_config.create_base_command_string() == expected_base_command

    def test_cvat_dump_cli_command(self):
        cvat_cli_config = CVATCLIConfig(
            cli_path="CVAT_DIR/utils/cli/cli.py",
            server_host="http://localhost",
            disable_ssl_verify=True,
            auth="USERNAME:PASSWORD",
        )

        assert CVATDumper._CVATDumper__create_cvat_dump_cli_command(
            base_command=cvat_cli_config.create_base_command_string(),
            target_zip_path="PATH_TO_ZIP/target.zip",
            task_info=CVATTaskInfoConfig(task_ID=0, annotation_format="PASCAL VOC 1.1"),
        ) == (
            f"{sys.executable} "
            "CVAT_DIR/utils/cli/cli.py "
            "--server-host http://localhost "
            "--auth USERNAME:PASSWORD "
            "dump 0 PATH_TO_ZIP/target.zip --format 'PASCAL VOC 1.1'"
        )

    def test_cvat_upload_cli_command(self):
        cvat_cli_config = CVATCLIConfig(
            cli_path="CVAT_DIR/utils/cli/cli.py",
            server_host="http://localhost",
            disable_ssl_verify=True,
            auth="USERNAME:PASSWORD",
        )

        assert PascalVOCUploader._PascalVOCUploader__create_cvat_upload_cli_command(
            base_command=cvat_cli_config.create_base_command_string(),
            target_zip_path="PATH_TO_ZIP/target.zip",
            task_info=CVATTaskInfoConfig(task_ID=0, annotation_format="PASCAL VOC 1.1"),
        ) == (
            f"{sys.executable} "
            "CVAT_DIR/utils/cli/cli.py "
            "--server-host http://localhost "
            "--auth USERNAME:PASSWORD "
            "upload 0 PATH_TO_ZIP/target.zip --format 'PASCAL VOC 1.1'"
        )

    def test_cvat_dumper_create_target_zip_path(self):
        assert CVATDumper._CVATDumper__create_target_zip_path(
            dump_task_config=CVATTaskDumpConfig(task_info=CVATTaskInfoConfig(task_ID=1))
        ) == os.path.join("tmp", "tmp-task.zip")

    @pytest.mark.usefixtures("subprocess_run_mock")
    def test_cvat_annotation_handler_download(self):
        cvat_annotation_handler = CVATAnnotationHandler(
            configuration=CVATAnnotationHandler.create_configuration(
                yaml_config_path=os.path.join(
                    self.project_root,
                    "test_data/test_cvat_annotation_handler/test_download/"
                    "test-download-task.yaml",
                ),
                string_replacement_map=self.string_replacement_map,
            )
        )

        if not os.path.isfile(
            cvat_annotation_handler.configuration.cvat_cli_config.password_path
        ):
            raise ValueError(
                "Please create the password file for your CVAT instance: %s"
                % cvat_annotation_handler.configuration.cvat_cli_config.password_path
            )

        cvat_annotation_handler.run()

    def test_cvat_annotation_handler_download_move_data(self):
        dataset_dir = os.path.join(self.project_root, "test_output", "dataset_dir")
        os.makedirs(dataset_dir, exist_ok=True)

        CVATDumper._CVATDumper__extract_and_copy_annotations_to_data_dir(
            target_zip_path=os.path.join(
                self.project_root,
                "test_data/test_cvat_annotation_handler/test_upload/mlcvzoo-test.zip",
            ),
            zip_extract_dir=os.path.join(self.project_root, "test_output"),
            dataset_dir=dataset_dir,
        )

    @pytest.mark.usefixtures("subprocess_run_failed_1_mock")
    def test_cvat_annotation_handler_download_failed(self):
        cvat_annotation_handler = CVATAnnotationHandler(
            configuration=CVATAnnotationHandler.create_configuration(
                yaml_config_path=os.path.join(
                    self.project_root,
                    "test_data/test_cvat_annotation_handler/test_download/"
                    "test-download-task.yaml",
                ),
                string_replacement_map=self.string_replacement_map,
            )
        )

        if not os.path.isfile(
            cvat_annotation_handler.configuration.cvat_cli_config.password_path
        ):
            raise ValueError(
                "Please create the password file for your CVAT instance: %s"
                % cvat_annotation_handler.configuration.cvat_cli_config.password_path
            )

        with self.assertRaises(OSError):
            cvat_annotation_handler.run()

    @pytest.mark.usefixtures("subprocess_run_mock")
    def test_cvat_annotation_handler_upload(self):
        cvat_annotation_handler = CVATAnnotationHandler(
            configuration=CVATAnnotationHandler.create_configuration(
                yaml_config_path=os.path.join(
                    self.project_root,
                    "test_data/test_cvat_annotation_handler/test_upload/"
                    "test-upload-task.yaml",
                ),
                string_replacement_map=self.string_replacement_map,
            )
        )

        if not os.path.isfile(
            cvat_annotation_handler.configuration.cvat_cli_config.password_path
        ):
            raise ValueError(
                "Please create the password file for your CVAT instance: %s"
                % cvat_annotation_handler.configuration.cvat_cli_config.password_path
            )

        cvat_annotation_handler.run()

        assert os.path.isfile(
            cvat_annotation_handler.configuration.upload_task_configs[0].target_zip_path
        )

        expected_extract_zip_dir = os.path.join(
            self.project_root,
            "test_output/test_cvat_annotation_handler/expected_extract_zip/",
        )
        test_extract_dir = os.path.join(
            self.project_root,
            "test_output/test_cvat_annotation_handler/test_extract_upload/",
        )

        extract_zip_data(
            zip_path=os.path.join(
                self.project_root,
                "test_data/test_cvat_annotation_handler/test_upload/mlcvzoo-test.zip",
            ),
            zip_extract_dir=expected_extract_zip_dir,
        )
        extract_zip_data(
            zip_path=cvat_annotation_handler.configuration.upload_task_configs[
                0
            ].target_zip_path,
            zip_extract_dir=test_extract_dir,
        )

        relative_test_path_1 = "Annotations/cars.xml"
        relative_test_path_2 = "Annotations/person.xml"
        relative_test_path_3 = "Annotations/truck.xml"

        assert _xml_equal(
            os.path.join(expected_extract_zip_dir, relative_test_path_1),
            os.path.join(test_extract_dir, relative_test_path_1),
        )

        assert _xml_equal(
            os.path.join(expected_extract_zip_dir, relative_test_path_2),
            os.path.join(test_extract_dir, relative_test_path_2),
        )

        assert _xml_equal(
            os.path.join(expected_extract_zip_dir, relative_test_path_3),
            os.path.join(test_extract_dir, relative_test_path_3),
        )

    @pytest.mark.usefixtures("subprocess_run_mock")
    def test_cvat_annotation_handler_upload_predictions(self):
        cvat_annotation_handler = CVATAnnotationHandler(
            configuration=CVATAnnotationHandler.create_configuration(
                yaml_config_path=os.path.join(
                    self.project_root,
                    "test_data/test_cvat_annotation_handler/test_upload/"
                    "test-upload-task-predictions.yaml",
                ),
                string_replacement_map=self.string_replacement_map,
            )
        )

        if not os.path.isfile(
            cvat_annotation_handler.configuration.cvat_cli_config.password_path
        ):
            raise ValueError(
                "Please create the password file for your CVAT instance: %s"
                % cvat_annotation_handler.configuration.cvat_cli_config.password_path
            )

        cvat_annotation_handler.run()

        assert os.path.isfile(
            cvat_annotation_handler.configuration.upload_task_configs[0].target_zip_path
        )

        test_extract_dir = os.path.join(
            self.project_root,
            "test_output/test_cvat_annotation_handler/test_extract_upload_predictions/",
        )

        extract_zip_data(
            zip_path=cvat_annotation_handler.configuration.upload_task_configs[
                0
            ].target_zip_path,
            zip_extract_dir=test_extract_dir,
        )

        assert _xml_equal(
            os.path.join(
                self.project_root,
                "test_data/annotations/pascal_voc/dummy_task/cars.xml",
            ),
            os.path.join(test_extract_dir, "Annotations/cars.xml"),
        )

        assert _xml_equal(
            os.path.join(
                self.project_root,
                "test_data/annotations/pascal_voc/dummy_task/person.xml",
            ),
            os.path.join(test_extract_dir, "Annotations/person.xml"),
        )

        assert _xml_equal(
            os.path.join(
                self.project_root,
                "test_data/annotations/pascal_voc/dummy_task/truck.xml",
            ),
            os.path.join(test_extract_dir, "Annotations/truck.xml"),
        )

    @pytest.mark.usefixtures("subprocess_run_mock")
    def test_cvat_annotation_handler_upload_predictions_only_create(self):
        cvat_annotation_handler = CVATAnnotationHandler(
            configuration=CVATAnnotationHandler.create_configuration(
                yaml_config_path=os.path.join(
                    self.project_root,
                    "test_data/test_cvat_annotation_handler/test_upload/"
                    "test-upload-task-predictions_only-create.yaml",
                ),
                string_replacement_map=self.string_replacement_map,
            )
        )

        if not os.path.isfile(
            cvat_annotation_handler.configuration.cvat_cli_config.password_path
        ):
            raise ValueError(
                "Please create the password file for your CVAT instance: %s"
                % cvat_annotation_handler.configuration.cvat_cli_config.password_path
            )

        cvat_annotation_handler.run()

        assert os.path.isfile(
            cvat_annotation_handler.configuration.upload_task_configs[0].target_zip_path
        )

        test_extract_dir = os.path.join(
            self.project_root,
            "test_output/test_cvat_annotation_handler/"
            "test_extract_upload_predictions_only_create/",
        )

        extract_zip_data(
            zip_path=cvat_annotation_handler.configuration.upload_task_configs[
                0
            ].target_zip_path,
            zip_extract_dir=test_extract_dir,
        )

        assert _xml_equal(
            os.path.join(
                self.project_root,
                "test_data/annotations/pascal_voc/dummy_task/cars.xml",
            ),
            os.path.join(test_extract_dir, "Annotations/cars.xml"),
        )

        assert _xml_equal(
            os.path.join(
                self.project_root,
                "test_data/annotations/pascal_voc/dummy_task/person.xml",
            ),
            os.path.join(test_extract_dir, "Annotations/person.xml"),
        )

        assert _xml_equal(
            os.path.join(
                self.project_root,
                "test_data/annotations/pascal_voc/dummy_task/truck.xml",
            ),
            os.path.join(test_extract_dir, "Annotations/truck.xml"),
        )

    @pytest.mark.usefixtures("subprocess_run_mock")
    def test_cvat_annotation_handler_download_and_upload(self):
        cvat_annotation_handler = CVATAnnotationHandler(
            configuration=CVATAnnotationHandler.create_configuration(
                yaml_config_path=os.path.join(
                    self.project_root,
                    "test_data/test_cvat_annotation_handler/"
                    "test-download-and-upload-task.yaml",
                ),
                string_replacement_map=self.string_replacement_map,
            )
        )

        if not os.path.isfile(
            cvat_annotation_handler.configuration.cvat_cli_config.password_path
        ):
            raise ValueError(
                "Please create the password file for your CVAT instance: %s"
                % cvat_annotation_handler.configuration.cvat_cli_config.password_path
            )

        cvat_annotation_handler.run()

    @pytest.mark.usefixtures("shutil_rmtree_mock", "os_path_isdir_mock")
    def test_extract_zip_data_remove_existing(self):
        extract_zip_data(
            zip_path=os.path.join(
                self.project_root,
                "test_data/test_cvat_annotation_handler/test_upload/mlcvzoo-test.zip",
            ),
            zip_extract_dir=os.path.join(
                self.project_root, "test_output", "zip_extract_dir"
            ),
        )

    @pytest.mark.usefixtures("os_path_isdir_mock")
    def test_extract_zip_data_skip(self):
        extract_zip_data(
            zip_path=os.path.join(
                self.project_root,
                "test_data/test_cvat_annotation_handler/test_upload/mlcvzoo-test.zip",
            ),
            zip_extract_dir=os.path.join(
                self.project_root, "test_output", "zip_extract_dir"
            ),
            remove_existing=False,
        )

    def test_cvat_annotation_handler_tool(self):
        command = "%s %s --replacement-config-path %s --log-level 'DEBUG'" % (
            os.path.join(
                self.project_root,
                "mlcvzoo_util/cvat_annotation_handler/cvat_annotation_handler.py",
            ),
            os.path.join(
                self.project_root,
                "test_data/test_cvat_annotation_handler/test_upload/"
                "test-upload-task-predictions_only-create.yaml",
            ),
            self._gen_replacement_config(),
        )

        command_split = [sys.executable]
        command_split.extend(shlex.split(command))

        result = subprocess.run(args=command_split, env=os.environ.copy(), check=False)

        assert result.returncode == 0

    def test_cvat_annotation_handler_too_wrong_parameter(self):
        command = "%s --wrong-parameter test" % (
            os.path.join(
                self.project_root,
                "mlcvzoo_util/mlcvzoo_util//cvat_annotation_handler.py",
            ),
        )

        command_split = [sys.executable]
        command_split.extend(shlex.split(command))

        result = subprocess.run(args=command_split, env=os.environ.copy(), check=False)

        assert result.returncode == 2

    def test_cvat_dumper_pre_cleanup(self):
        assert not CVATDumper._CVATDumper__pre_clean_up_and_determine_skip(
            overwrite_existing_zip=False,
            target_zip_path=os.path.join(
                self.project_root,
                "test_data/test_cvat_annotation_handler/test_download/NO_FILE.zip",
            ),
        )

    def test_cvat_dumper_pre_cleanup_not_overwrite_and_skip(self):
        assert CVATDumper._CVATDumper__pre_clean_up_and_determine_skip(
            overwrite_existing_zip=False,
            target_zip_path=os.path.join(
                self.project_root,
                "test_data/test_cvat_annotation_handler/test_download/mlcvzoo-test.zip",
            ),
        )

    def test_cvat_dumper_pre_cleanup_overwrite(self):
        target_zip_path = os.path.join(
            self.project_root,
            "test_data/test_cvat_annotation_handler/test_download/mlcvzoo-test.zip",
        )

        copy_target_zip_path = os.path.join(
            self.project_root,
            "test_data/test_cvat_annotation_handler/test_download/mlcvzoo-test_copy.zip",
        )

        shutil.copy(target_zip_path, copy_target_zip_path)

        assert not CVATDumper._CVATDumper__pre_clean_up_and_determine_skip(
            overwrite_existing_zip=True, target_zip_path=copy_target_zip_path
        )

        assert not os.path.isfile(copy_target_zip_path)

    def test_cvat_dumper_post_cleanup(self):
        target_zip_path = os.path.join(
            self.project_root,
            "test_data/test_cvat_annotation_handler/test_download/mlcvzoo-test.zip",
        )

        copy_target_zip_path = os.path.join(
            self.project_root,
            "test_data/test_cvat_annotation_handler/test_download/mlcvzoo-test_copy.zip",
        )

        zip_extract_dir = os.path.join(
            self.project_root,
            "test_data/test_cvat_annotation_handler/test_download/mlcvzoo-test/",
        )

        os.makedirs(zip_extract_dir, exist_ok=True)

        shutil.copy(target_zip_path, copy_target_zip_path)

        CVATDumper._CVATDumper__post_clean_up(
            target_zip_path=copy_target_zip_path, zip_extract_dir=zip_extract_dir
        )

        assert not os.path.isfile(copy_target_zip_path)
        assert not os.path.isdir(zip_extract_dir)

    def test_cvat_uploader_write_upload_zip_file_empty_target_zip_path(self):
        zip_path = os.path.join(
            self.project_root,
            "test_data/test_cvat_annotation_handler/test_download/mlcvzoo-test.zip",
        )

        target_zip_path = os.path.join(
            self.project_root,
            "test_data/test_cvat_annotation_handler/test_download/"
            "mlcvzoo-test_upload.zip",
        )

        shutil.copy(zip_path, target_zip_path)

        PascalVOCUploader.write_upload_zip_file(
            upload_task_config=CVATTaskUploadConfig(
                task_info=CVATTaskInfoConfig(task_ID=1),
                execute_upload=True,
                source_zip_path=zip_path,
                use_prediction_data=False,
                target_zip_path="",
                prediction_data_dir=os.path.join(
                    self.project_root, "test_data/annotations/pascal_voc/dummy_task"
                ),
            )
        )

        assert os.path.isfile(target_zip_path)

    def test_cvat_uploader_write_upload_zip_file_no_prediction_data_dir(self):
        zip_path = os.path.join(
            self.project_root,
            "test_data/test_cvat_annotation_handler/test_download/mlcvzoo-test.zip",
        )

        target_zip_path = os.path.join(
            self.project_root,
            "test_data/test_cvat_annotation_handler/test_download/"
            "mlcvzoo-test_upload.zip",
        )

        shutil.copy(zip_path, target_zip_path)

        with self.assertRaises(ValueError) as value_error:
            PascalVOCUploader.write_upload_zip_file(
                upload_task_config=CVATTaskUploadConfig(
                    task_info=CVATTaskInfoConfig(task_ID=1),
                    execute_upload=True,
                    source_zip_path=zip_path,
                    use_prediction_data=False,
                    target_zip_path=target_zip_path,
                    prediction_data_dir="",
                )
            )

            assert (
                str(value_error)
                == "prediction_data_dir='' does not exist! Please specify a "
                "directory in order to generatea prediction zip file for the upload to CVAT!"
            )

    def test_cvat_uploader_post_clean_up(self):
        zip_path = os.path.join(
            self.project_root,
            "test_data/test_cvat_annotation_handler/test_download/mlcvzoo-test.zip",
        )

        copy_source_zip_path = os.path.join(
            self.project_root,
            "test_data/test_cvat_annotation_handler/test_download/"
            "mlcvzoo-test_source-copy.zip",
        )

        copy_target_zip_path = os.path.join(
            self.project_root,
            "test_data/test_cvat_annotation_handler/test_download/"
            "mlcvzoo-test_target-copy.zip",
        )

        shutil.copy(zip_path, copy_source_zip_path)
        shutil.copy(zip_path, copy_target_zip_path)

        PascalVOCUploader._PascalVOCUploader__post_clean_up(
            source_zip_path=copy_source_zip_path, target_zip_path=copy_target_zip_path
        )

        assert not os.path.isfile(copy_source_zip_path)
        assert not os.path.isfile(copy_target_zip_path)

    def test_cvat_uploader_post_clean_up_no_files(self):
        PascalVOCUploader._PascalVOCUploader__post_clean_up(
            source_zip_path="source_zip_path", target_zip_path="target_zip_path"
        )

    def test_cvat_annotation_handler_failed_constructor(self):
        argv_copy = copy.deepcopy(sys.argv)

        sys.argv = [sys.argv[0]]

        with pytest.raises(SystemExit) as system_exit:
            cvat_annotation_handler_main()

        assert system_exit.value.code == 2

        sys.argv = argv_copy


if __name__ == "__main__":
    main()
