# Copyright 2024 Nikolas Achatz (github.com/nachatz)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Classes managing poetryx configuration files."""

import os
from pathlib import Path
from typing import Dict

from .file_manager import write_file, delete_file, read_file


class FileConfig:
    """Manages the configuration file for poetryx at the user's root directory.

    By default when instantiated validates the configuration file exists, and
    if not, creates it from a template.

    Attributes:
        config_file (str): The name of the configuration file.
        config_template_toml (str): The name of the template configuration file.
        config_path (str): The path to the user's configuration file.
        config_toml_path (str): The path to the template configuration file.
    """

    config_file: str = ".poetryx"
    config_template_toml: str = "config.toml"
    config_path: str = str(Path.home().joinpath(config_file))
    config_toml_path: str = str(
        Path(__file__).resolve().parent.joinpath(config_template_toml)
    )

    def __init__(self) -> None:
        self._validate_configuration()

    def _validate_configuration(self) -> None:
        if not os.path.exists(self.config_path):
            write_file(self.config_path, read_file(self.config_toml_path))

    def clean_configuration(self) -> None:
        delete_file(self.config_path)

    def set_configuration(self, config: Dict) -> None:
        write_file(self.config_path, config, toml=True)
