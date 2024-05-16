# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

import copy
import logging
import os
import sys
from typing import Dict, Optional
from unittest import TestCase, main
from unittest.mock import MagicMock

from mlcvzoo_base.api.interfaces import NetBased, Trainable
from mlcvzoo_base.models.read_from_file.configuration import ReadFromFileConfig
from mlcvzoo_base.models.read_from_file.model import ReadFromFileObjectDetectionModel
from pytest import fixture, mark
from pytest_mock import MockerFixture
from test_template import TestTemplate

from mlcvzoo_util.model_trainer.model_trainer import ModelTrainer
from mlcvzoo_util.model_trainer.model_trainer import main as model_trainer_main

logger = logging.getLogger(__name__)


@fixture(scope="function")
def create_model_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        "mlcvzoo_util.model_trainer.model_trainer.ModelTrainer.create_model",
        return_value=TestModel(
            from_yaml="",
        ),
    )


class TestModel(ReadFromFileObjectDetectionModel, NetBased, Trainable):
    def __init__(
        self,
        from_yaml: str,
        configuration: Optional[ReadFromFileConfig] = None,
        string_replacement_map: Optional[Dict[str, str]] = None,
        init_for_inference: bool = True,
    ):
        pass

    def get_training_output_dir(self) -> Optional[str]:
        return None

    def get_checkpoint_filename_suffix(self) -> str:
        return ""

    def restore(self, checkpoint_path: str) -> None:
        pass

    def train(self) -> None:
        pass

    def store(self, checkpoint_path: str) -> None:
        pass


class TestModelTrainer(TestTemplate):
    @mark.usefixtures(
        "create_model_mock",
    )
    def test_run_training_model_trainer_read_from_file(self) -> None:
        model_trainer = ModelTrainer(
            configuration=ModelTrainer.create_configuration(
                yaml_config_path=os.path.join(
                    self.project_root,
                    "test_data/test_model_trainer/"
                    "test_model-trainer_config_read-from-file_coco_test.yaml",
                ),
                string_replacement_map=self.string_replacement_map,
            )
        )

        model_trainer.run_training()

    @mark.usefixtures(
        "create_model_mock",
    )
    def test_model_trainer_main(self):
        argv_copy = copy.deepcopy(sys.argv)

        sys.argv = [sys.argv[0]]

        sys.argv.extend(
            [
                os.path.join(
                    self.project_root,
                    "test_data/test_model_trainer/"
                    "test_model-trainer_config_read-from-file_coco_test.yaml",
                ),
                "--replacement-config-path",
                self._gen_replacement_config(),
                "--log-dir",
                os.path.join(self.project_root, "test_output", "logs"),
                "--log-level",
                "DEBUG",
            ]
        )

        model_trainer_main()

        sys.argv = argv_copy


if __name__ == "__main__":
    main()
