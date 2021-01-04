#!/usr/bin/env python
# pylint: disable=no-member

""" Configuration file class """

# import json
from typing import Optional
from pathlib import Path
import platform

import yaml

from cli import Style


msg_style = Style(fg="green")


def home_path():
    return Path(f"~").expanduser()


class Config:
    """
    Configuration class.

    At construction
      if config file exists for basename, the file is read into the object.
      Otherwise, the object is populated by kwarge adn the config file is written.

    Whenever the object is modified, the config file is over-written.
    """

    def __init__(self, basename, **kwargs):

        # config_path = f"{basename}.yaml"  # json"

        self.__dict__["_data"] = kwargs
        self.__dict__["_path"] = self._find_config_file(basename)

        if self._path:
            self._read()
        else:
            self.__dict__["_path"] = self._config_path(basename)
            self._write()

    def __getattr__(self, name):
        assert name in self._data, f"{name} not in config"
        return self._data[name]

    def __setattr__(self, name, value):
        assert name in self._data, f"{name} not in config"
        self._data[name] = value
        self._write()

    def __delattr__(self, name):
        assert False, "Cannot delete from config"

    def set(self, **kwargs):
        """ TODO """
        for name, value in kwargs.items():
            assert name in self._data, f"{name} not in config"
            self._data[name] = value
        self._write()

    def _write(self):
        output_folder = self._path.parent
        if not output_folder.exists():
            output_folder.mkdir()
            msg_style.echo(f"Created folder {output_folder} to hold your configuration")

        with open(self._path, "w") as output:
            output.write(yaml.safe_dump(self._data, default_flow_style=False))
            # json.dump(self._data, output, sort_keys=True, indent=4)

    def _read(self):
        with open(self._path) as input:
            data = yaml.safe_load(input)  # json.load(input)
            # data = json.load(input)

        # check to make sure keys are the same
        data_keys = set(data.keys())
        default_keys = set(self._data.keys())
        assert (
            data_keys == default_keys
        ), f"{self._path} and Config default keys do not match: {(default_keys ^ data_keys)}"

        self.__dict__["_data"] = data

    @staticmethod
    def _filename(basename) -> str:
        """ where to try finding the file in order """

        return f"{basename}.yaml"

    @classmethod
    def _find_config_file(cls, basename) -> Optional[Path]:
        """ where to try finding the file in order """

        home = home_path()
        filename = cls._filename(basename)

        for path in (
            f".{filename}",
            f".config/{basename}/{filename}",
            f"Library/Application Support/{basename}/{filename}",
            f".local/etc/{filename}",
            f".local/etc/{basename}/{filename}",
        ):
            file_path = home / path
            if file_path.is_file():
                return file_path
        return None

    @classmethod
    def _config_path(cls, basename: str) -> Path:
        """Do some platform detection and suggest a place for the users' config file to go"""

        home = home_path()
        filename = cls._filename(basename)

        system = platform.system()

        if system == "Darwin":
            return home / "Library/Application Support" / basename / filename
        if system == "Linux":
            return home / ".config" / basename / filename
        return home / f".{filename}"


def demo():
    """ Demonstrate Config class """

    config = Config("test", version=1, TOKEN="c5bffe0e")
    print(f"Version was {config.version}")
    config.version += 1
    print(f"Version is now {config.version}")


if __name__ == "__main__":
    demo()
