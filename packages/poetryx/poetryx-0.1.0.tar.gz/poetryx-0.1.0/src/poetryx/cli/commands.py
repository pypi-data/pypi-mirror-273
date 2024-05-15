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
"""Commands interface that provide the entry point for poetryx."""

import typer
from .typer_cli import TyperCLI

app = TyperCLI()
cli = app.cli


@cli.command()
def configure() -> None:
    """Configure poetryx configuration file"""
    app.configure()


@cli.command()
def clean() -> None:
    """Cleans up and resets poetryx to its initial state.
    Helpful if anything ever goes wrong!
    """
    confirmed = typer.confirm(
        "🚨 Are you sure you want to wipe your config file (.poetryx)?"
    )

    if confirmed:
        app.config.clean_configuration()
        typer.echo("Successfully reset poetryx")
    else:
        typer.echo("Cancelled reset")
