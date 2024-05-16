# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

import logging
import os
from pathlib import Path
from unittest import TestCase, main

from config_builder.replacement_map import (
    get_current_replacement_map,
    set_replacement_map_value,
    update_replacement_map_from_os,
)
from mlcvzoo_base.configuration.replacement_config import ReplacementConfig

import mlcvzoo_util

logger = logging.getLogger(__name__)


class TestTemplate(TestCase):
    def setUp(self) -> None:
        self.this_dir = Path(os.path.dirname(os.path.abspath(__file__))).resolve()

        setup_path = self.this_dir
        while setup_path.exists() and not setup_path.name == mlcvzoo_util.__name__:
            if setup_path == setup_path.parent:
                raise RuntimeError("Could not find setup_path!")
            else:
                setup_path = setup_path.parent
        # One more to be above the target directory
        setup_path = setup_path.parent

        self.project_root = str(setup_path)
        self.code_root = str(setup_path)

        set_replacement_map_value(
            ReplacementConfig.PROJECT_ROOT_DIR_KEY, self.project_root
        )
        update_replacement_map_from_os()
        self.string_replacement_map = get_current_replacement_map()

        logger.debug(
            "Setup finished: \n"
            " - this_dir: %s\n"
            " - project_root: %s\n"
            " - code_root: %s\n"
            % (
                self.this_dir,
                self.project_root,
                self.code_root,
            )
        )
        os.chdir(self.code_root)
        logger.info("Changed working directory to: '%s'", self.code_root)

    def _gen_replacement_config(self) -> str:
        path = Path("%s/test_output/" % self.project_root)
        # project_root should point to an already existing location, so do not create parents here
        path.mkdir(exist_ok=True, parents=False)
        path = path / "replacement_config.yaml"
        with open(path, "w", encoding="utf-8") as file:
            file.write("PROJECT_ROOT_DIR: %s\n" % self.project_root)
            return str(path)


if __name__ == "__main__":
    main()
