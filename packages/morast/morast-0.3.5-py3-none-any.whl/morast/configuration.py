# -*- coding: utf-8 -*-

"""

morast.configuration

Configuration handling


Copyright (C) 2024 Rainer Schwarzbach

This file is part of morast.

morast is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

morast is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""

import dataclasses
import logging
import pathlib
import unicodedata

from typing import Any, Dict, List

import yaml

from morast import commons


#
# Constants
#


MORAST_BASE_PATH = pathlib.Path(commons.MORAST_CONFIG_DIR)

DEFAULT_ADVERTISE = False
DEFAULT_SOURCE = pathlib.Path(commons.SRC)
DEFAULT_DESTINATION = pathlib.Path(commons.DOCS) / commons.REFERENCE
DEFAULT_CONFIG_FILE = MORAST_BASE_PATH / commons.CONFIG_FILE_NAME
DEFAULT_OVERRIDES_BASEPATH = MORAST_BASE_PATH / commons.OVERRIDES
DEFAULT_CONFIG_SOURCE = "defaults"

KW_ADVERTISE = "advertise"
KW_SOURCE_PATH = "source_path"
KW_DESTINATION_PATH = "destination_path"
KW_OVERRIDES_BASEPATH = "overrides_basepath"
KW_EXCLUDED_MODULES = "excluded_modules"
KW_CONFIG_SOURCE = "configuration_source"
KW_EMOJI = "emoji"
KW_ENABLED = "enabled"


def default_excluded_module_patterns() -> List[str]:
    """Return the default excluded modules patterns list
    (factory function for the GlobalOptions() dataclass)
    """
    return ["*.__*__"]


#
# classes
#


# pylint: disable=too-many-instance-attributes


@dataclasses.dataclass(frozen=True)
class EmojiConfiguration:
    """Configuration of emoji for documentation output"""

    enabled: bool = True
    module_prefix: str = unicodedata.lookup("JIGSAW PUZZLE PIECE")
    constants_prefix: str = unicodedata.lookup("PUSHPIN")
    #
    # alternative prefix for missing documentation:
    # BLACK QUESTION MARK ORNAMENT
    missing_documentation_prefix: str = unicodedata.lookup("CONSTRUCTION SIGN")
    #
    # alternative prefix for inheritance: SEEDLING
    inheritance_prefix: str = unicodedata.lookup("HATCHING CHICK")
    signature_prefix: str = unicodedata.lookup("OPEN BOOK")
    class_attributes_prefix: str = unicodedata.lookup("ROUND PUSHPIN")
    instance_attributes_prefix: str = unicodedata.lookup("PAPERCLIP")
    property_prefix: str = unicodedata.lookup("CLIPBOARD")
    advertisement_prefix: str = unicodedata.lookup("PUBLIC ADDRESS LOUDSPEAKER")

    def get_serializable(self) -> Dict[str, Any]:
        """Return a serializable variant
        as a dict having the characters replaced by ther unicode names
        """
        output_config: Dict[str, Any] = {}
        as_dict = dataclasses.asdict(self)
        for key, value in as_dict.items():
            if isinstance(value, str):
                logging.debug("Resolving %s: %r", key, value)
                output_config[key] = unicodedata.name(value)
            else:
                output_config[key] = value
            #
        #
        return output_config


class EmojiProxy:
    """Object providing emoji if enabled."""

    def __init__(self, emoji: EmojiConfiguration) -> None:
        r"""
        Initialization argument:

        *   _emoji_: a configuration.[EmojiConfiguration]
            instance
        """
        self.__emoji = emoji
        self.__cache: Dict[str, str] = {}
        self.__provide_preset("todo_prefix", "missing_documentation_prefix", "TODO:")

    def __provide_preset(self, name: str, emoji_name: str, default: str) -> None:
        """Provide a preset in the cache"""
        self.__cache[name] = self[emoji_name] or default

    def __getitem__(self, name: str) -> str:
        """Get the matching emoji by name if enabled,
        else an empty string
        """
        try:
            return self.__cache[name]
        except KeyError:
            pass
        #
        if not self.__emoji.enabled:
            return self.__cache.setdefault(name, "")
        #
        found_emoji = getattr(self.__emoji, name)
        if isinstance(found_emoji, str):
            return self.__cache.setdefault(name, found_emoji)
        #
        raise KeyError(name)

    def __getattr__(self, name: str) -> str:
        """Get the matching emoji by name if enabled,
        else an empty string
        """
        try:
            return self[name]
        except KeyError as error:
            raise AttributeError(f"no attribute {name!r}") from error
        #


@dataclasses.dataclass
class GlobalOptions:
    """Global program options"""

    configuration_source: str = DEFAULT_CONFIG_SOURCE
    source_path: pathlib.Path = DEFAULT_SOURCE
    excluded_modules: List[str] = dataclasses.field(
        default_factory=default_excluded_module_patterns
    )
    destination_path: pathlib.Path = DEFAULT_DESTINATION
    overrides_basepath: pathlib.Path = DEFAULT_OVERRIDES_BASEPATH
    emoji: EmojiConfiguration = EmojiConfiguration()
    advertise: bool = DEFAULT_ADVERTISE

    def get_serializable(self) -> Dict[str, Any]:
        r"""Return a serializable variant
        as a dict having the pathlib.Path objects converted to strings
        and the _configuration\_source_ attribute removed
        """
        output_config: Dict[str, Any] = {}
        for field in dataclasses.fields(self):
            key = field.name
            if key == KW_CONFIG_SOURCE:
                continue
            #
            value = getattr(self, key)
            logging.debug("Resolving %s: %r", key, value)
            if isinstance(value, pathlib.Path):
                output_config[key] = value.as_posix()
            elif isinstance(value, EmojiConfiguration):
                output_config[key] = value.get_serializable()
            else:
                output_config[key] = value
            #
        #
        return output_config

    def dump(self, include_source_comment: bool = True) -> str:
        r"""Return the configuration as a YAML dump as provided by the
        **.get_serializable()** method
        (ie. excluding _configuration\\_source_),
        with a comment in the top line
        including the _configuration\_source_ value
        if _include\_source\_comment_ is True (the default)
        """
        source_comment = ""
        if include_source_comment:
            source_comment = f"# Source: {self.configuration_source}\n"
        #
        data_dump = yaml.dump(
            self.get_serializable(),
            sort_keys=False,
            default_flow_style=False,
            indent=2,
        )
        return f"{source_comment}{data_dump}"

    @classmethod
    def from_file(
        cls,
        path: pathlib.Path = DEFAULT_CONFIG_FILE,
    ) -> "GlobalOptions":
        """Factory method:
        read the config file at _path_ and return
        a GlobalOptions instance
        """
        if not path.exists():
            return cls()
        #
        pre_config: Dict[str, Any] = {}
        raw_config = yaml.safe_load(path.read_text(encoding=commons.UTF8))
        for key, value in raw_config.items():
            if key in (
                KW_DESTINATION_PATH,
                KW_OVERRIDES_BASEPATH,
                KW_SOURCE_PATH,
            ):
                try:
                    value = raw_config[key]
                except KeyError:
                    logging.info(
                        "Keyword %r missing in configuration file"
                        " – using hardcoded preset",
                        key,
                    )
                else:
                    pre_config[key] = pathlib.Path(value)
                #
            elif key == KW_EMOJI:
                emoji_collect: Dict[str, Any] = {}
                if isinstance(value, dict):
                    for subkey, subvalue in value.items():
                        if subkey == KW_ENABLED:
                            emoji_collect[subkey] = bool(subvalue)
                            continue
                        #
                        try:
                            emoji_collect[subkey] = unicodedata.lookup(subvalue)
                        except KeyError as error:
                            logging.warning(str(error.args[0]))
                            continue
                        #
                    #
                else:
                    logging.warning("Invalid value for %s: %r", key, value)
                #
                pre_config[key] = EmojiConfiguration(**emoji_collect)
            else:
                pre_config[key] = value
            #
        #
        pre_config[KW_CONFIG_SOURCE] = f"configuration file {path}"
        return cls(**pre_config)


DUMMY_OPTIONS = GlobalOptions()


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
