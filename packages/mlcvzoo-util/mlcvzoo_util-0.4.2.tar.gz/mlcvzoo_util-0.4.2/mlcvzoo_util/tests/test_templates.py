# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

import logging
import os
from typing import Dict, List, Type
from unittest import main

from config_builder import BaseConfigClass, ConfigBuilder
from test_template import TestTemplate

from mlcvzoo_util.model_timer.configuration import ModelTimerConfig
from mlcvzoo_util.model_trainer.configuration import ModelTrainerConfig
from mlcvzoo_util.video_image_creator.configuration import VideoImageCreatorConfig

logger = logging.getLogger(__name__)


class TestTemplates(TestTemplate):
    def test_config_templates(self) -> None:
        template_path_dict: Dict[Type[BaseConfigClass], List[str]] = {
            VideoImageCreatorConfig: [
                os.path.join(
                    self.project_root,
                    "config",
                    "templates",
                    "tools",
                    "video-image-creator_template.yaml",
                )
            ],
            ModelTrainerConfig: [
                os.path.join(
                    self.project_root,
                    "config",
                    "templates",
                    "tools",
                    "model-trainer_config_template.yaml",
                )
            ],
            ModelTimerConfig: [
                os.path.join(
                    self.project_root,
                    "config",
                    "templates",
                    "tools",
                    "model-timer_config_template.yaml",
                )
            ],
        }

        for config_class_type, template_path_list in template_path_dict.items():
            for template_path in template_path_list:
                logger.info(
                    "=================================================================\n"
                    "CHECK correct build of configuration class %s "
                    "with template-config-path '%s'\n",
                    config_class_type,
                    template_path,
                )

                config_builder = ConfigBuilder(
                    class_type=config_class_type,
                    yaml_config_path=template_path,
                    string_replacement_map=self.string_replacement_map,
                    no_checks=True,
                )

                logger.info(
                    "================================================================="
                )
                assert config_builder.configuration is not None


if __name__ == "__main__":
    main()
