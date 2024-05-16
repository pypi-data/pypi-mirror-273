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

from pytest import fixture, mark
from pytest_mock import MockerFixture
from test_template import TestTemplate

from mlcvzoo_util.model_timer.model_timer import ModelTimer
from mlcvzoo_util.model_timer.model_timer import main as model_timer_main

logger = logging.getLogger(__name__)


@fixture(scope="function")
def set_inference_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        "mlcvzoo_base.configuration.model_config.ModelConfig.set_inference",
        return_value=None,
    )


class TestModelTimer(TestTemplate):
    @mark.usefixtures(
        "set_inference_mock",
    )
    def test_on_read_from_file_object_detection_with_mlflow_logging(self) -> None:
        yaml_config_path_with_mlflow = os.path.join(
            self.project_root,
            "test_data",
            "test_model_timer",
            "model_timer-read-from-file-with-mlfow-logging.yaml",
        )

        model_timer = ModelTimer(
            configuration=ModelTimer.create_configuration(
                yaml_config_path=yaml_config_path_with_mlflow,
                string_replacement_map=self.string_replacement_map,
            )
        )

        model_timer.run()

    @mark.usefixtures(
        "set_inference_mock",
    )
    def test_on_read_from_file_object_detection_without_mlflow_logging(self) -> None:
        yaml_config_path_without_mlflow = os.path.join(
            self.project_root,
            "test_data",
            "test_model_timer",
            "model_timer-read-from-file-without-mlfow-logging.yaml",
        )

        model_timer = ModelTimer(
            configuration=ModelTimer.create_configuration(
                yaml_config_path=yaml_config_path_without_mlflow,
                string_replacement_map=self.string_replacement_map,
            )
        )

        model_timer.run()

    @mark.usefixtures(
        "set_inference_mock",
    )
    def test_model_timer_main(self):
        argv_copy = copy.deepcopy(sys.argv)

        sys.argv = [sys.argv[0]]

        sys.argv.extend(
            [
                os.path.join(
                    self.project_root,
                    "test_data/test_model_timer/"
                    "model_timer-read-from-file-with-mlfow-logging.yaml",
                ),
                "--replacement-config-path",
                self._gen_replacement_config(),
                "--log-dir",
                os.path.join(self.project_root, "test_output", "logs"),
                "--log-level",
                "DEBUG",
            ]
        )

        model_timer_main()

        sys.argv = argv_copy


if __name__ == "__main__":
    main()
