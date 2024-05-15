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
"""Class for overloading typer CLI functionality"""

from typing import List, Dict
import typer
import click
from poetryx.file import FileConfig
from poetryx.file.file_manager import read_file, write_file


class TyperCLI:
    """Custom Typer CLI for configuring poetryx.

    By default creates a typer CLI and adds poetryx configuration.

    Attributes:
        cli (typer.Typer): The Typer CLI instance.
        config (FileConfig): The FileConfig instance for managing configuration.
    """

    def __init__(self) -> None:
        self.cli = typer.Typer()
        self.config = FileConfig()

    def configure(self) -> None:
        toml = read_file(FileConfig.config_path, toml=True)
        if not isinstance(toml, dict):
            raise ValueError(f"Invalid configuration file: {FileConfig.config_path}")

        config = toml["poetryx"]["config"]

        def prompt(option: str, options: List[str] | None = None) -> None:
            """Manages the prompt for configuring poetryx, should match 1:1
            with the `poetryx.file.config.toml` file

            Args:
                option (str): The option to prompt for
                options (List[str], optional): The options to choose from. Defaults to [].
            """
            resp: click.Choice | str | None = None
            if options:
                click_choice = click.Choice(options)
                resp = typer.prompt(
                    f"{option.upper()}",
                    default=config[option],
                    show_choices=True,
                    type=click_choice,
                )
            else:
                resp = typer.prompt(f"{option.upper()}", default=config[option])

            config[option] = resp

        prompt("ide", ["vscode", "n/a"])
        result: Dict[str, Dict[str, Dict[str, str]]] = {"poetryx": {"config": config}}
        write_file(FileConfig.config_path, result, toml=True)
