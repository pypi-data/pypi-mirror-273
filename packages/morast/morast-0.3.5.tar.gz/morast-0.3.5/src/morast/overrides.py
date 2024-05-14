# -*- coding: utf-8 -*-

"""

morast.overrides

Override file handling


Copyright (C) 2024 Rainer Schwarzbach

This file is part of morast.

morast is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

morast is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""

import collections
import logging
import pathlib
import re

from typing import Iterator, List, Optional, Tuple

from morast import commons
from morast import configuration


#
# Module constants
#


__all__ = ["OverridesSection", "ModuleOverrides"]

ADDITIONS = "additions"
IGNORE = "ignore"
STRIP_VALUE = "strip-value"

KIND_CLASS_ATTRIBUTE = "class attribute"
KIND_CLASS_METHOD = "class method"
KIND_CLASS = "class"
KIND_CONSTANT = "module-level constant"
KIND_FUNCTION = "module-level function"
KIND_INSTANCE_ATTRIBUTE = "instance attribute"
KIND_INSTANCE_METHOD = "instance method"
KIND_MODULE = "module"
KIND_MORAST_SPECIAL = "(Morast special purpose)"
KIND_PROPERTY = "property"
KIND_REFINDEX = "of the package reference"
KIND_UNSPECIFIED = "(unspecified type)"

CLASS_CONTEXT_KINDS: Tuple[str, ...] = (
    KIND_CLASS_ATTRIBUTE,
    KIND_CLASS_METHOD,
    KIND_INSTANCE_ATTRIBUTE,
    KIND_INSTANCE_METHOD,
    KIND_PROPERTY,
)

SUPPORTED_KINDS: Tuple[str, ...] = (
    KIND_CLASS_ATTRIBUTE,
    KIND_CLASS_METHOD,
    KIND_CLASS,
    KIND_CONSTANT,
    KIND_FUNCTION,
    KIND_INSTANCE_ATTRIBUTE,
    KIND_INSTANCE_METHOD,
    KIND_MODULE,
    KIND_MORAST_SPECIAL,
    KIND_PROPERTY,
    KIND_REFINDEX,
    KIND_UNSPECIFIED,
)

PRX_HEADLINE = re.compile("\\A#{1,6}\\s")

MORAST_PREFIX = f"{commons.BRAND}:".lower()


class OverridesSection:
    r"""Overrides section for one syntax tree node"""

    def __init__(
        self,
        name: str,
        kind: str = KIND_UNSPECIFIED,
        namespace: str = commons.EMPTY,
    ) -> None:
        r"""Initialization arguments:

        *   _name_: the section name
        *   _kind_: the node kind (one of SUPPORTED\_KINDS)
        *   _namespace_: the section namespace
        """
        self.name = name
        self.__additions: List[str] = []
        self.__docstring: List[str] = []
        self.__is_ignored: bool = False
        self.__value_is_stripped: bool = False
        if kind not in SUPPORTED_KINDS:
            raise ValueError(f"Kind {kind!r} not supported")
        #
        self.kind = kind
        self.namespace = namespace
        logging.debug("section namespaced name: %r", self.name)

    def __str__(self):
        """Return the section as a string,
        suitable for overrides extraction
        """
        name_parts = self.name.split(commons.DOT)
        level = len(name_parts)
        headline = f"{commons.POUND * level} {name_parts[-1]} {self.kind}"
        if self.kind in CLASS_CONTEXT_KINDS:
            headline = f"{headline} of {self.namespace}"
        #
        if self.__is_ignored:
            headline = f"{headline} | {IGNORE}"
        #
        if self.__value_is_stripped:
            headline = f"{headline} | {STRIP_VALUE}"
        #
        contents = self.docstring
        if self.__additions:
            headline = f"{headline} | {ADDITIONS}"
            contents = self.additions
        #
        return commons.LF.join((headline, commons.EMPTY, contents))

    def __bool__(self) -> bool:
        """OverridesSection instances evaluate to `True`
        if the contain any contents,
        are ignored, or their value is stripped.
        """
        return (
            bool(self.additions.strip())
            or bool(self.docstring.strip())
            or self.is_ignored
            or self.value_is_stripped
        )

    @property
    def additions(self) -> str:
        """The additions that will be appended to the docstring
        retrieved from the source code,
        but only if the processing instruction contains `additions`
        """
        return commons.LF.join(self.__additions).rstrip()

    @property
    def docstring(self) -> str:
        """The text that will replace the docstring retrieved
        from the source code, only if the processing instruction
        _does not_ contain `additions`.
        """
        return commons.LF.join(self.__docstring).rstrip()

    @property
    def is_ignored(self) -> bool:
        """Flag indicating that the section will be ignored
        in the generated documentation;
        `True` if the processing instruction contains `ignore`.
        """
        return self.__is_ignored

    @property
    def value_is_stripped(self) -> bool:
        """Flag indicating that the value is stripped from
        the assigment in the generated documentation
        (making sense with objects displayed as assignments only,
        ie. attributes or constants);
        `True` if the processing instruction contains `strip-value`.
        """
        return self.__value_is_stripped

    def __add_to_lines_sequence(
        self, lines_sequence_name: str, lines_sequence: List[str], line: str
    ) -> None:
        r"""Append _line_ to the specified sequence _lines\_sequence_
        (which will be called _lines\_sequence\_name_ in log output)
        """
        if not line.rstrip() and not lines_sequence:
            return
        #
        if self.is_ignored:
            logging.info(
                "Appending line %r to ignored section %s’s %s",
                line,
                self.name,
                lines_sequence_name,
            )
        else:
            logging.info(
                "Appending line %r to section %s’s %s",
                line,
                self.name,
                lines_sequence_name,
            )
        #
        lines_sequence.append(line)

    def add_to_additions(self, line: str) -> None:
        """Append _line_ to additions"""
        self.__add_to_lines_sequence("additions", self.__additions, line)

    def add_to_docstring(self, line: str) -> None:
        """Append _line_ to docstring"""
        self.__add_to_lines_sequence("docstring", self.__docstring, line)

    def clear_docstring(self) -> None:
        """Clear the docstring"""
        self.__docstring.clear()

    def ignore(self) -> None:
        r"""Set the _is\_ignored_ flag"""
        self.__is_ignored = True
        if self.__docstring or self.__additions:
            fs_detail = "    %s"
            logging.info("Section %s contents already exist, but will be ignored:")
            if self.__docstring:
                logging.info("- docstring")
                for line in self.__docstring:
                    logging.debug(fs_detail, line)
                #
            #
            if self.__additions:
                logging.info("- additions")
                for line in self.__additions:
                    logging.debug(fs_detail, line)
                #
            #
        #

    def strip_value(self) -> None:
        r"""Set the _value\_is\_stripped_ flag"""
        self.__value_is_stripped = True


class ModuleOverrides:
    """Override sections for one module"""

    def __init__(self, external_namespace: str) -> None:
        r"""Initialization argument:

        *   _external\_namepsace_: the external namespace of the mudule
        """
        self.__external_namespace = external_namespace
        self.__contents: collections.OrderedDict[str, OverridesSection] = (
            collections.OrderedDict()
        )

    @property
    def external_namespace(self) -> str:
        """The external namespace of the module"""
        return self.__external_namespace

    def setdefault(
        self,
        name: str,
        kind: Optional[str] = None,
        namespace: Optional[str] = None,
    ) -> OverridesSection:
        """Lookup the OverridesSection instance stored as _name_,
        and set its _kind_ and _namepace_ attributes if provided.
        If no section had been stored under that name,
        create a new one from the provided arguments (or presets)
        and store it as _name_.

        Finally, return the section.
        """
        try:
            section = self.__contents[name]
            if kind is not None:
                section.kind = kind
            #
            if namespace is not None:
                section.namespace = namespace
            #
            logging.debug("SECTION NAME: %r", name)
            logging.debug("SECTION KIND: %r", kind)
            logging.debug("SECTION NAMESPACE: %r", namespace)
        except KeyError:
            logging.info(
                "%r not found in overrides, returning a new empty section",
                name,
            )
            logging.debug("SECTION NAME: %r", name)
            section = self.__contents.setdefault(
                name,
                OverridesSection(
                    name,
                    kind=kind or KIND_UNSPECIFIED,
                    namespace=namespace or commons.EMPTY,
                ),
            )
        #
        return section

    def __getitem__(
        self,
        name: str,
    ) -> OverridesSection:
        """Directly return the OverridesSection instance stored as _name_,
        or a default empty section if nothing had been stored as _name_ before.
        """
        if name.lower().startswith(MORAST_PREFIX):
            name = name.lower()
        #
        return self.setdefault(name)

    def items(self) -> Iterator[Tuple[str, OverridesSection]]:
        """Return an iterator over the internal dict’s items,
        ie. the section name and the section itself for each
        stored section.
        """
        yield from self.__contents.items()

    @staticmethod
    def get_external_namespace(
        base_path: pathlib.Path,
        module_override_path: pathlib.Path,
    ) -> str:
        """Return an external namespace
        determined from the path relative to base_path
        """
        absolute_base_path = base_path.resolve()
        relative_path = module_override_path.relative_to(absolute_base_path)
        external_namespace_parts: List[str] = []
        if len(relative_path.parts) > 1:
            external_namespace_parts.extend(relative_path.parent.parts)
        #
        external_namespace_parts.append(relative_path.stem)
        return commons.DOT.join(external_namespace_parts)

    # pylint: disable=too-many-branches
    # pylint: disable=too-many-locals
    @classmethod
    def from_string(
        cls,
        module_name: str,
        override_contents: str,
        external_namespace: str,
    ) -> "ModuleOverrides":
        r"""Create a new ModuleOverrides instance from the provided
        _external\_namespace_,
        parse _override\_contents_ into [OverrideSection] instances
        (checking if the first internal namespace part of each
        non-special section header matches _module\_name_),
        and store the sections by their name using [self.setdefault()]
        """
        mod_overrides = cls(external_namespace)
        internal_namespace: List[str] = []
        current_section = OverridesSection(commons.EMPTY)
        write_to_additions = False
        # special_override = False
        for line in override_contents.splitlines():
            headline_match = PRX_HEADLINE.match(line)
            if headline_match:
                headline_parts = line.split()
                level = len(headline_parts[0])
                section_name = headline_parts[1]  # TODO: sanitize
                remaining_headline = commons.BLANK.join(headline_parts[2:])
                if len(internal_namespace) < level - 1:
                    raise ValueError(
                        f"Cannot determine namespace of name {section_name!r}"
                        f" in level {level} in combination with the"
                        " previous internal namespace"
                        f" {commons.DOT.join(internal_namespace)!r}"
                    )
                #
                while len(internal_namespace) >= level:
                    internal_namespace.pop()
                #
                kind = KIND_UNSPECIFIED
                if section_name.lower().startswith(MORAST_PREFIX):
                    section_name = section_name.lower()
                    kind = KIND_MORAST_SPECIAL
                else:
                    for candidate in SUPPORTED_KINDS:
                        if remaining_headline.startswith(candidate):
                            kind = candidate
                            break
                        #
                    #
                #
                internal_namespace.append(section_name)
                namespaced_name = commons.DOT.join(internal_namespace)
                namespace = commons.EMPTY
                if kind in CLASS_CONTEXT_KINDS:
                    start_candidate = f"{kind} of "
                    sc_length = len(start_candidate)
                    if remaining_headline.startswith(start_candidate):
                        namespace = remaining_headline[:sc_length].split()[0]
                    #
                #
                current_section = mod_overrides.setdefault(
                    namespaced_name,
                    kind=kind,
                    namespace=namespace,
                )
                write_to_additions = ADDITIONS in remaining_headline
                if IGNORE in remaining_headline:
                    current_section.ignore()
                #
                if STRIP_VALUE in remaining_headline:
                    current_section.strip_value()
                #
                continue
            #
            if not internal_namespace:
                continue
            #
            if internal_namespace[0] != module_name and kind != KIND_MORAST_SPECIAL:
                raise ValueError(
                    f"{internal_namespace[0]!r} does not match"
                    f" the module name {module_name!r}"
                )
            #
            if write_to_additions:
                add_method = current_section.add_to_additions
            else:
                add_method = current_section.add_to_docstring
            #
            add_method(line)
        #
        return mod_overrides

    @classmethod
    def from_file(
        cls,
        config: configuration.GlobalOptions,
        path: pathlib.Path,
    ) -> "ModuleOverrides":
        r"""Read the file specified by _path_,
        determine its external namespace from the path relative to the
        **overrides\_basepath** setting in _config_
        and return a ModuleOverrides instance
        with sections parsed from the file’s contents.¸
        """
        full_path = path.resolve()
        external_namespace = cls.get_external_namespace(
            config.overrides_basepath,
            full_path,
        )
        ext_namespace_parts = external_namespace.split(commons.DOT)
        module_name = ext_namespace_parts[-1]
        module_contents = full_path.read_text(encoding=commons.UTF8)
        return cls.from_string(module_name, module_contents, external_namespace)


DUMMY_MOD_OVERRIDES = ModuleOverrides(commons.EMPTY)


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
