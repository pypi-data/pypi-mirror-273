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
"""Utilities for reading and writing files."""

from typing import Dict, Any
import os
from toml import load, dump


def read_file(path: str, toml: bool = False) -> str | Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as file:
        if toml:
            return load(file)
        return file.read()


def write_file(path: str, content: str | Dict[str, Any], toml: bool = False) -> None:
    with open(path, "w", encoding="utf-8") as file:
        if toml and isinstance(content, dict):
            dump(content, file)
        elif not toml and isinstance(content, str):
            file.write(content)
        else:
            raise ValueError(
                "Invalid content type. Expected str when 'toml' is False and dict when 'toml' is True."
            )


def delete_file(path: str) -> None:
    os.remove(path)
