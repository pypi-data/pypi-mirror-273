# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

import copy
import logging
import os
import sys
from typing import Dict, List, Optional, Tuple
from unittest import main
from unittest.mock import MagicMock

import mlflow
import related
from attr import define
from mlcvzoo_base.api.configuration import ModelConfiguration
from mlcvzoo_base.api.data.annotation_class_mapper import AnnotationClassMapper
from mlcvzoo_base.api.interfaces import Classifiable, NetBased
from mlcvzoo_base.api.model import ConfigurationType, DataType, Model, PredictionType
from mlcvzoo_base.configuration.class_mapping_config import ClassMappingConfig
from mlcvzoo_base.evaluation.object_detection.data_classes import (
    ODMetrics,
    ODModelEvaluationMetrics,
)
from pytest import fixture, mark
from pytest_mock import MockerFixture
from test_template import TestTemplate

from mlcvzoo_util.model_evaluator.configuration import CheckpointConfig
from mlcvzoo_util.model_evaluator.metric_factory import MetricFactory
from mlcvzoo_util.model_evaluator.model_evaluator import ModelEvaluator
from mlcvzoo_util.model_evaluator.model_evaluator import (
    __get_model_checkpoint as get_model_checkpoint,
)
from mlcvzoo_util.model_evaluator.model_evaluator import main as model_evaluator_main
from mlcvzoo_util.model_evaluator.structs import CheckpointInfo

logger = logging.getLogger(__name__)

# fmt: off
test_evaluated_checkpoint_metrics = {
    'test_model_checkpoint': ODModelEvaluationMetrics(
        model_specifier='test_model',
        metrics_dict={
            0.5: {
                'ALL': {
                    '0_person': ODMetrics.from_dict({"TP": 1, "FP": 0, "FN": 0, "PR": 1.0, "RC": 1.0, "F1": 1.0, "AP": 1.0, "COUNT": 1}),
                    '1_truck': ODMetrics.from_dict({"TP": 1, "FP": 0, "FN": 0, "PR": 1.0, "RC": 1.0, "F1": 1.0, "AP": 1.0, "COUNT": 1}),
                    '2_car': ODMetrics.from_dict({"TP": 1, "FP": 0, "FN": 0, "PR": 1.0, "RC": 1.0, "F1": 1.0, "AP": 1.0, "COUNT": 1}),
                    '3_lp': ODMetrics.from_dict({"TP": 0, "FP": 0, "FN": 0, "PR": 0.0, "RC": 0.0, "F1": 0.0, "AP": 0.0, "COUNT": 0}),
                },
                'S': {
                    '0_person': ODMetrics.from_dict({"TP": 0, "FP": 0, "FN": 0, "PR": 0.0, "RC": 0.0, "F1": 0.0, "AP": 0.0, "COUNT": 0}),
                    '1_truck': ODMetrics.from_dict({"TP": 0, "FP": 0, "FN": 0, "PR": 0.0, "RC": 0.0, "F1": 0.0, "AP": 0.0, "COUNT": 0}),
                    '2_car': ODMetrics.from_dict({"TP": 0, "FP": 0, "FN": 0, "PR": 0.0, "RC": 0.0, "F1": 0.0, "AP": 0.0, "COUNT": 0}),
                    '3_lp': ODMetrics.from_dict({"TP": 0, "FP": 0, "FN": 0, "PR": 0.0, "RC": 0.0, "F1": 0.0, "AP": 0.0, "COUNT": 0}),
                },
                'M': {
                    '0_person': ODMetrics.from_dict({"TP": 0, "FP": 0, "FN": 0, "PR": 0.0, "RC": 0.0, "F1": 0.0, "AP": 0.0, "COUNT": 0}),
                    '1_truck': ODMetrics.from_dict({"TP": 0, "FP": 0, "FN": 0, "PR": 0.0, "RC": 0.0, "F1": 0.0, "AP": 0.0, "COUNT": 0}),
                    '2_car': ODMetrics.from_dict({"TP": 0, "FP": 0, "FN": 0, "PR": 0.0, "RC": 0.0, "F1": 0.0, "AP": 0.0, "COUNT": 0}),
                    '3_lp': ODMetrics.from_dict({"TP": 0, "FP": 0, "FN": 0, "PR": 0.0, "RC": 0.0, "F1": 0.0, "AP": 0.0, "COUNT": 0}),
                },
                'L': {
                    '0_person': ODMetrics.from_dict({"TP": 1, "FP": 0, "FN": 0, "PR": 1.0, "RC": 1.0, "F1": 1.0, "AP": 1.0, "COUNT": 1}),
                    '1_truck': ODMetrics.from_dict({"TP": 1, "FP": 0, "FN": 0, "PR": 1.0, "RC": 1.0, "F1": 1.0, "AP": 1.0, "COUNT": 1}),
                    '2_car': ODMetrics.from_dict({"TP": 1, "FP": 0, "FN": 0, "PR": 1.0, "RC": 1.0, "F1": 1.0, "AP": 1.0, "COUNT": 1}),
                    '3_lp': ODMetrics.from_dict({"TP": 0, "FP": 0, "FN": 0, "PR": 0.0, "RC": 0.0, "F1": 0.0, "AP": 0.0, "COUNT": 0})
                }
            }
        },
        metrics_image_info_dict={'0_person': {}, '1_truck': {}, '2_car': {}, '3_lp': {}}
    )
}
# fmt: on


@fixture(scope="function")
def select_evaluation_checkpoints_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        "mlcvzoo_util.model_evaluator.model_evaluator."
        "ModelEvaluator.select_evaluation_checkpoints",
        return_value=["TEST_CHECKPOINT", "TEST_CHECKPOINT_2"],
    )


@fixture(scope="function")
def restore_checkpoint_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        "mlcvzoo_util.model_evaluator.model_evaluator.ModelEvaluator._restore_checkpoint",
        return_value=None,
    )


@fixture(scope="function")
def set_inference_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        "mlcvzoo_base.configuration.model_config.ModelConfig.set_inference",
        return_value=None,
    )


@fixture(scope="function")
def determine_best_checkpoint_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        "mlcvzoo_util.model_evaluator.metric_factory.ODMetricFactory.determine_best_checkpoint",
        return_value=CheckpointInfo(
            path=MetricFactory.MODEL_STATE_INDICATOR,
            score=1.0,
        ),
    )


@fixture(scope="function")
def get_model_checkpoint_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        "mlcvzoo_util.model_evaluator.model_evaluator.__get_model_checkpoint",
        return_value=[
            os.path.join(
                "test_data/test_model_evaluator/test-checkpoint.pth",
            )
        ],
    )


@define
class TestConfig(ModelConfiguration):
    test_config: str = related.StringField(required=False, default="Hello World")


@fixture(scope="function")
def create_model_mock(mocker: MockerFixture) -> MagicMock:
    class TestModel(Model, Classifiable):
        def __init__(self):
            Model.__init__(
                self,
                configuration=TestConfig(unique_name="test-model"),
                init_for_inference=True,
            )
            Classifiable.__init__(
                self,
                mapper=AnnotationClassMapper(
                    class_mapping=ClassMappingConfig(
                        model_classes=[],
                        number_model_classes=0,
                    ),
                ),
            )

        @property
        def num_classes(self) -> int:
            return 0

        def get_classes_id_dict(self) -> Dict[int, str]:
            pass

        def predict(self, data_item: DataType) -> Tuple[DataType, List[PredictionType]]:
            pass

        @staticmethod
        def create_configuration(
            from_yaml: Optional[str] = None,
            configuration: Optional[ConfigurationType] = None,
            string_replacement_map: Optional[Dict[str, str]] = None,
        ) -> ConfigurationType:
            pass

    return mocker.patch(
        "mlcvzoo_util.model_evaluator.model_evaluator.ModelEvaluator.create_model",
        return_value=TestModel(),
    )


class TestModelEvaluator(TestTemplate):
    def test_metric_factory_base(self) -> None:
        with self.assertRaises(NotImplementedError):
            MetricFactory.log_results(
                checkpoint_log_mode="all",
                evaluated_checkpoint_metrics=test_evaluated_checkpoint_metrics,
                best_checkpoint=CheckpointInfo(
                    path="test_model_checkpoint",
                    score=1.0,
                ),
                logging_configs=None,
            )
        with self.assertRaises(NotImplementedError):
            MetricFactory.log_results(
                checkpoint_log_mode="all",
                evaluated_checkpoint_metrics=test_evaluated_checkpoint_metrics,
                best_checkpoint=CheckpointInfo(
                    path="test_model_checkpoint",
                    score=1.0,
                ),
                logging_configs=None,
            )

    @mark.usefixtures(
        "select_evaluation_checkpoints_mock",
        "restore_checkpoint_mock",
        "set_inference_mock",
    )
    def test_model_evaluator_main(self):
        argv_copy = copy.deepcopy(sys.argv)

        sys.argv = [sys.argv[0]]

        sys.argv.extend(
            [
                os.path.join(
                    self.project_root,
                    "test_data/test_model_evaluator/"
                    "test_model_evaluator_without_mlflow.yaml",
                ),
                "--replacement-config-path",
                self._gen_replacement_config(),
                "--log-dir",
                os.path.join(self.project_root, "test_output", "logs"),
                "--log-level",
                "DEBUG",
            ]
        )

        model_evaluator_main()

        sys.argv = argv_copy

    @mark.usefixtures(
        "select_evaluation_checkpoints_mock",
        "restore_checkpoint_mock",
        "set_inference_mock",
        "create_model_mock",
    )
    def test_model_evaluator_wrong_model(self):
        argv_copy = copy.deepcopy(sys.argv)

        sys.argv = [sys.argv[0]]

        sys.argv.extend(
            [
                os.path.join(
                    self.project_root,
                    "test_data/test_model_evaluator/"
                    "test_model_evaluator_without_mlflow.yaml",
                ),
                "--replacement-config-path",
                self._gen_replacement_config(),
                "--log-dir",
                os.path.join(self.project_root, "test_output", "logs"),
                "--log-level",
                "DEBUG",
            ]
        )

        with self.assertRaises(ValueError):
            model_evaluator_main()

        sys.argv = argv_copy

    @mark.usefixtures(
        "select_evaluation_checkpoints_mock",
        "restore_checkpoint_mock",
        "set_inference_mock",
    )
    def test_model_evaluator_main_single_mode(self):
        argv_copy = copy.deepcopy(sys.argv)

        sys.argv = [sys.argv[0]]

        sys.argv.extend(
            [
                os.path.join(
                    self.project_root,
                    "test_data/test_model_evaluator/"
                    "test_model_evaluator_without_mlflow.yaml",
                ),
                "--replacement-config-path",
                self._gen_replacement_config(),
                "--log-dir",
                os.path.join(self.project_root, "test_output", "logs"),
                "--log-level",
                "DEBUG",
                "--single-mode",
            ]
        )

        model_evaluator_main()

        sys.argv = argv_copy

    @mark.usefixtures(
        "select_evaluation_checkpoints_mock",
        "restore_checkpoint_mock",
        "set_inference_mock",
    )
    def test_model_evaluator_main_single_mode_from_argparse(self):
        argv_copy = copy.deepcopy(sys.argv)

        sys.argv = [sys.argv[0]]

        from_yaml = os.path.join(
            self.project_root,
            "test_data/test_ReadFromFileObjectDetectionModel/"
            "read-from-file_pascal_voc_clean.yaml",
        )

        sys.argv.extend(
            [
                os.path.join(
                    self.project_root,
                    "test_data/test_model_evaluator/"
                    "test_model_evaluator_without_mlflow.yaml",
                ),
                "--constructor-parameters",
                f"from_yaml:{from_yaml}",
                "--replacement-config-path",
                self._gen_replacement_config(),
                "--log-dir",
                os.path.join(self.project_root, "test_output", "logs"),
                "--log-level",
                "DEBUG",
                "--single-mode",
            ]
        )

        model_evaluator_main()

        sys.argv = argv_copy

    @mark.usefixtures(
        "select_evaluation_checkpoints_mock",
        "restore_checkpoint_mock",
        "set_inference_mock",
    )
    def test_model_evaluator_main_single_mode_with_tb(self):
        mlflow.end_run()

        argv_copy = copy.deepcopy(sys.argv)

        sys.argv = [sys.argv[0]]

        sys.argv.extend(
            [
                os.path.join(
                    self.project_root,
                    "test_data/test_model_evaluator/"
                    "test_model_evaluator_tensorboard.yaml",
                ),
                "--replacement-config-path",
                self._gen_replacement_config(),
                "--log-dir",
                os.path.join(self.project_root, "test_output", "logs"),
                "--log-level",
                "DEBUG",
                "--single-mode",
            ]
        )

        model_evaluator_main()

        sys.argv = argv_copy

    @mark.usefixtures(
        "select_evaluation_checkpoints_mock",
        "restore_checkpoint_mock",
        "set_inference_mock",
    )
    def test_model_evaluator_main_single_mode_with_mlflow(self):
        argv_copy = copy.deepcopy(sys.argv)

        sys.argv = [sys.argv[0]]

        sys.argv.extend(
            [
                os.path.join(
                    self.project_root,
                    "test_data/test_model_evaluator/"
                    "test_model_evaluator_with_mlflow.yaml",
                ),
                "--replacement-config-path",
                self._gen_replacement_config(),
                "--log-dir",
                os.path.join(self.project_root, "test_output", "logs"),
                "--log-level",
                "DEBUG",
                "--single-mode",
            ]
        )

        model_evaluator_main()

        sys.argv = argv_copy

    @mark.usefixtures(
        "select_evaluation_checkpoints_mock",
        "restore_checkpoint_mock",
        "set_inference_mock",
    )
    def test_model_evaluator_main_single_mode_with_mlflow_all_checkpoints(self):
        argv_copy = copy.deepcopy(sys.argv)

        sys.argv = [sys.argv[0]]

        sys.argv.extend(
            [
                os.path.join(
                    self.project_root,
                    "test_data/test_model_evaluator/"
                    "test_model_evaluator_with_mlflow_all-checkpoint.yaml",
                ),
                "--replacement-config-path",
                self._gen_replacement_config(),
                "--log-dir",
                os.path.join(self.project_root, "test_output", "logs"),
                "--log-level",
                "DEBUG",
                "--single-mode",
            ]
        )

        model_evaluator_main()

        sys.argv = argv_copy

    @mark.usefixtures(
        "select_evaluation_checkpoints_mock",
        "restore_checkpoint_mock",
        "set_inference_mock",
        "determine_best_checkpoint_mock",
    )
    def test_model_evaluator_main_single_mode_with_mlflow_best_checkpoint(self):
        argv_copy = copy.deepcopy(sys.argv)

        sys.argv = [sys.argv[0]]

        sys.argv.extend(
            [
                os.path.join(
                    self.project_root,
                    "test_data/test_model_evaluator/"
                    "test_model_evaluator_with_mlflow_best-checkpoint.yaml",
                ),
                "--replacement-config-path",
                self._gen_replacement_config(),
                "--log-dir",
                os.path.join(self.project_root, "test_output", "logs"),
                "--log-level",
                "DEBUG",
                "--single-mode",
            ]
        )

        model_evaluator_main()

        sys.argv = argv_copy

    @mark.usefixtures(
        "select_evaluation_checkpoints_mock",
        "restore_checkpoint_mock",
        "set_inference_mock",
    )
    def test_model_evaluator_main_single_mode_with_mlflow_wrong_checkpoint(self):
        argv_copy = copy.deepcopy(sys.argv)

        sys.argv = [sys.argv[0]]

        sys.argv.extend(
            [
                os.path.join(
                    self.project_root,
                    "test_data/test_model_evaluator/"
                    "test_model_evaluator_with_mlflow_wrong-checkpoint.yaml",
                ),
                "--replacement-config-path",
                self._gen_replacement_config(),
                "--log-dir",
                os.path.join(self.project_root, "test_output", "logs"),
                "--log-level",
                "DEBUG",
                "--single-mode",
            ]
        )

        with self.assertRaises(ValueError):
            model_evaluator_main()

        sys.argv = argv_copy

    @mark.usefixtures(
        "select_evaluation_checkpoints_mock",
        "restore_checkpoint_mock",
        "set_inference_mock",
    )
    def test_model_evaluator_main_single_mode_with_mlflow_wrong_model(self):
        argv_copy = copy.deepcopy(sys.argv)

        sys.argv = [sys.argv[0]]

        sys.argv.extend(
            [
                os.path.join(
                    self.project_root,
                    "test_data/test_model_evaluator/"
                    "test_model_evaluator_with_mlflow_wrong-model.yaml",
                ),
                "--replacement-config-path",
                self._gen_replacement_config(),
                "--log-dir",
                os.path.join(self.project_root, "test_output", "logs"),
                "--log-level",
                "DEBUG",
                "--single-mode",
            ]
        )

        with self.assertRaises(ValueError):
            model_evaluator_main()

        sys.argv = argv_copy

    @mark.usefixtures(
        "select_evaluation_checkpoints_mock",
        "restore_checkpoint_mock",
        "set_inference_mock",
    )
    def test_model_evaluator_no_object_detection_model(self):
        argv_copy = copy.deepcopy(sys.argv)

        sys.argv = [sys.argv[0]]

        sys.argv.extend(
            [
                os.path.join(
                    self.project_root,
                    "test_data/test_model_evaluator/"
                    "test_model_evaluator_no_object_detection_model.yaml",
                ),
                "--replacement-config-path",
                self._gen_replacement_config(),
                "--log-dir",
                os.path.join(self.project_root, "test_output", "logs"),
                "--log-level",
                "DEBUG",
                "--single-mode",
            ]
        )

        with self.assertRaises(ValueError):
            model_evaluator_main()

        sys.argv = argv_copy

    @mark.usefixtures(
        "select_evaluation_checkpoints_mock",
        "restore_checkpoint_mock",
        "set_inference_mock",
        "get_model_checkpoint_mock",
    )
    def test_model_evaluator_get_model_checkpoint(self):
        argv_copy = copy.deepcopy(sys.argv)

        sys.argv = [sys.argv[0]]

        sys.argv.extend(
            [
                os.path.join(
                    self.project_root,
                    "test_data/test_model_evaluator/"
                    "test_model_evaluator_with_mlflow_best-checkpoint.yaml",
                ),
                "--replacement-config-path",
                self._gen_replacement_config(),
                "--log-dir",
                os.path.join(self.project_root, "test_output", "logs"),
                "--log-level",
                "DEBUG",
                "--single-mode",
            ]
        )

        model_evaluator_main()

        sys.argv = argv_copy

    @mark.usefixtures(
        "select_evaluation_checkpoints_mock",
        "restore_checkpoint_mock",
        "set_inference_mock",
    )
    def test_model_evaluator_no_factory(self):
        argv_copy = copy.deepcopy(sys.argv)

        sys.argv = [sys.argv[0]]

        sys.argv.extend(
            [
                os.path.join(
                    self.project_root,
                    "test_data/test_model_evaluator/"
                    "test_model_evaluator_no_factory.yaml",
                ),
                "--replacement-config-path",
                self._gen_replacement_config(),
                "--log-dir",
                os.path.join(self.project_root, "test_output", "logs"),
                "--log-level",
                "DEBUG",
            ]
        )

        with self.assertRaises(ValueError):
            model_evaluator_main()

        sys.argv = argv_copy

    def test_select_evaluation_checkpoints(self) -> None:
        assert ModelEvaluator.select_evaluation_checkpoints(
            checkpoint_config=CheckpointConfig(
                checkpoint_dir=os.path.join(self.project_root, "test_data/checkpoints"),
                checkpoint_filename_suffix=".pth",
            )
        ) == [
            os.path.join(self.project_root, "test_data/checkpoints/model.pth"),
            os.path.join(self.project_root, "test_data/checkpoints/model_2.pth"),
        ]

    def test_restore_checkpoint(self) -> None:
        class TestModel(Model, NetBased):
            def __init__(self):
                pass

            def predict(
                self, data_item: DataType
            ) -> Tuple[DataType, List[PredictionType]]:
                pass

            def store(self, checkpoint_path: str) -> None:
                pass

            def get_checkpoint_filename_suffix(self) -> str:
                return ""

            @staticmethod
            def create_configuration(
                from_yaml: Optional[str] = None,
                configuration: Optional[ConfigurationType] = None,
                string_replacement_map: Optional[Dict[str, str]] = None,
            ) -> ConfigurationType:
                pass

            def restore(self, checkpoint_path: str) -> None:
                pass

        ModelEvaluator._restore_checkpoint(
            checkpoint_path=os.path.join(
                self.project_root, "test_data/checkpoints/model.pth"
            ),
            model=TestModel(),
        )

    def test_restore_checkpoint_not_net_based(self) -> None:
        class TestModel(Model):
            def __init__(self):
                pass

            def predict(
                self, data_item: DataType
            ) -> Tuple[DataType, List[PredictionType]]:
                pass

            @staticmethod
            def create_configuration(
                from_yaml: Optional[str] = None,
                configuration: Optional[ConfigurationType] = None,
                string_replacement_map: Optional[Dict[str, str]] = None,
            ) -> ConfigurationType:
                pass

        with self.assertRaises(ValueError):
            ModelEvaluator._restore_checkpoint(
                checkpoint_path=os.path.join(
                    self.project_root, "test_data/checkpoints/model.pth"
                ),
                model=TestModel(),
            )

    def test_restore_checkpoint_wrong_path(self) -> None:
        class TestModel(Model):
            def __init__(self):
                pass

            def predict(
                self, data_item: DataType
            ) -> Tuple[DataType, List[PredictionType]]:
                pass

            @staticmethod
            def create_configuration(
                from_yaml: Optional[str] = None,
                configuration: Optional[ConfigurationType] = None,
                string_replacement_map: Optional[Dict[str, str]] = None,
            ) -> ConfigurationType:
                pass

        with self.assertRaises(ValueError):
            ModelEvaluator._restore_checkpoint(
                checkpoint_path=os.path.join(
                    self.project_root, "test_data/checkpoints/model.pt"
                ),
                model=TestModel(),
            )

    def test_model_evaluator_create_configuration(self) -> None:
        assert (
            ModelEvaluator.create_configuration(
                yaml_config_path=os.path.join(
                    self.project_root,
                    "test_data/test_model_evaluator/" "test_model_evaluator.yaml",
                ),
                string_replacement_map=self.string_replacement_map,
                no_checks=True,
            )
            is not None
        )

    def test_model_evaluator_get_model_checkpoint(self) -> None:
        class TestCheckpointConfig:
            def __init__(self) -> None:
                self.checkpoint_path: str = "test_checkpoint.pth"

        class TestInferenceConfig:
            def __init__(self) -> None:
                self.inference_config: TestCheckpointConfig = TestCheckpointConfig()

        class TestModel(Model, NetBased):
            def __init__(self) -> None:
                self.configuration = TestInferenceConfig()

            def predict(
                self, data_item: DataType
            ) -> Tuple[DataType, List[PredictionType]]:
                pass

            def store(self, checkpoint_path: str) -> None:
                pass

            def get_checkpoint_filename_suffix(self) -> str:
                return ""

            @staticmethod
            def create_configuration(
                from_yaml: Optional[str] = None,
                configuration: Optional[ConfigurationType] = None,
                string_replacement_map: Optional[Dict[str, str]] = None,
            ) -> ConfigurationType:
                pass

            def restore(self, checkpoint_path: str) -> None:
                pass

        assert get_model_checkpoint(model=TestModel()) == ["test_checkpoint.pth"]

    def test_model_evaluator_get_model_checkpoint_not_netbase(self) -> None:
        class TestModel(Model):
            def __init__(self) -> None:
                pass

            def predict(
                self, data_item: DataType
            ) -> Tuple[DataType, List[PredictionType]]:
                pass

            @staticmethod
            def create_configuration(
                from_yaml: Optional[str] = None,
                configuration: Optional[ConfigurationType] = None,
                string_replacement_map: Optional[Dict[str, str]] = None,
            ) -> ConfigurationType:
                pass

        assert get_model_checkpoint(model=TestModel()) is None

    def test_model_evaluator_get_model_checkpoint_accept_no_config(self) -> None:
        class TestModel(Model, NetBased):
            def __init__(self) -> None:
                pass

            def get_checkpoint_filename_suffix(self) -> str:
                return ""

            def predict(
                self, data_item: DataType
            ) -> Tuple[DataType, List[PredictionType]]:
                pass

            def store(self, checkpoint_path: str) -> None:
                pass

            @staticmethod
            def create_configuration(
                from_yaml: Optional[str] = None,
                configuration: Optional[ConfigurationType] = None,
                string_replacement_map: Optional[Dict[str, str]] = None,
            ) -> ConfigurationType:
                pass

            def restore(self, checkpoint_path: str) -> None:
                pass

        assert get_model_checkpoint(model=TestModel()) is None


if __name__ == "__main__":
    main()
