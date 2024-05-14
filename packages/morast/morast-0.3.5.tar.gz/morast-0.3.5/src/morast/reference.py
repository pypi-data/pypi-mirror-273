# pylint: disable=too-many-lines
# -*- coding: utf-8 -*-

"""

morast.reference

MorastModule and IndexPage classes


Copyright (C) 2024 Rainer Schwarzbach

This file is part of morast.

morast is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

morast is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""

import ast
import logging
import pathlib

from typing import Dict, Iterator, List

from smdg import elements as mde
from smdg import strings as mds

from morast import commons
from morast import core
from morast import nodes
from morast import overrides


#
# Constants
#


_MORAST_ADVERTISEMENT = f"{commons.BRAND}:generator"


#
# Classes
#


class BasePage(core.MorastSection):
    """Base class for Module and IndexPage"""

    def __init__(
        self,
        name: str,
        superconfig=core.DUMMY_SUPERCONFIG,
        headline: str = commons.EMPTY,
    ) -> None:
        r"""
        Initialization arguments:

        *   _name_: the name (public attribute)
        *   _superconfig_: a [SuperConfig] instance that is also passed through
            to to all contained [MorastDocumentableItem] subclass instances
        *   _headline_: the headline contents
        """
        super().__init__(
            name,
            superconfig=superconfig,
            headline=headline,
        )

    def markdown_elements(self) -> Iterator[mde.BaseElement]:
        """Iterator over MarkDown elements,
        appending a verbatim section if defined in the overrides
        """
        if self.sc.advertise:
            self.add_subnode(
                _MORAST_ADVERTISEMENT,
                nodes.Advertisement(self.sc.emoji.advertisement_prefix),
            )
        #
        yield from super().markdown_elements()
        verbatim_section = self.sc.mor[core.MORAST_VERBATIM]
        if verbatim_section:
            yield mde.BlockElement(mds.declare_as_safe(verbatim_section.docstring))
        #

    def render(self) -> str:
        """Generate MarkDown output from this instance"""
        return mde.render(*self.markdown_elements())

    def get_extracted_overrides(self) -> str:
        """Return extracted overrides for the extract subcommand"""
        overrides_list: List[str] = []
        for section in self.sc.get_nested_sections(self.name):
            overrides_list.extend((str(section).rstrip(), commons.EMPTY))
        #
        verbatim_section = self.sc.mor[core.MORAST_VERBATIM]
        if verbatim_section:
            overrides_list.extend((str(verbatim_section).rstrip(), commons.EMPTY))
        #
        return commons.LF.join(overrides_list)


class MorastModule(BasePage):
    """Represents a module

    Stores a sequence of MorastSection instances internally
    in the following order:

    1.  module contents
    2.  module-level functions
    3.  classes
    """

    kind = overrides.KIND_MODULE

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        module: ast.Module,
        name: str,
        namespace: str = "",
        superconfig=core.DUMMY_SUPERCONFIG,
    ) -> None:
        r"""
        Initialization arguments:

        *   _module_: an ast.Module instance from which this instance is built
        *   _name_: the module name (public attribute)
        *   _namespace_: the (external) module namespace,
             only used in the headline
        *   _superconfig_: a [SuperConfig] instance that is also passed through
            to to all contained [MorastDocumentableItem] subclass instances
        """
        self._namespace_prefix = f"{namespace}." if namespace else ""
        headline_prefix = superconfig.emoji.module_prefix or "Module"
        super().__init__(
            name,
            superconfig=superconfig,
            headline=f"{headline_prefix} {self._namespace_prefix}{name}",
        )
        self.module_contents = core.MorastAttributesList(
            "Module contents", superconfig=superconfig
        )
        self.classes = core.MorastSection(
            "Classes", namespace=name, superconfig=superconfig, level=2
        )
        self.functions = core.MorastSection(
            "Functions", namespace=name, superconfig=superconfig, level=2
        )
        for element in module.body:
            if isinstance(element, ast.Expr):
                if self.docstring:
                    continue
                #
                if isinstance(element.value, ast.Constant):
                    self.docstring = element.value.value
                    continue
                #
            else:
                try:
                    self._add_element(element)
                except TypeError as error:
                    logging.info(str(error))
                #
            #
        #
        self.set_docstring_from_override()
        self.add_subnode(core.MORAST_DOCSTRING, nodes.DocString(self.docstring))
        for subsection in (self.module_contents, self.functions, self.classes):
            if len(subsection):
                self.add_subsection(subsection=subsection)
            #
        #

    @property
    def namespaced_module(self) -> str:
        """Return the name prefixed by the namespace prefix"""
        return f"{self._namespace_prefix}{self.name}"

    def _add_element(
        self,
        element: ast.AST,
    ) -> None:
        """Add _element_ to the body blocks if not ignored.

        Currently, ast assignment (ie. ast.Assign, ast.AnnAssign),
        ast.ClassDef and ast.FunctionDef instances are supported.
        """
        if isinstance(element, (ast.Assign, ast.AnnAssign)):
            try:
                module_constant = core.MorastAttribute(
                    element,
                    namespace=self.name,
                    scope=core.SCOPE_MODULE,
                    superconfig=self.sc,
                )
            except core.IgnoredItemError as ignored:
                logging.info(ignored.message)
                return
            #
            self.module_contents.add(module_constant)
        elif isinstance(element, ast.ClassDef):
            try:
                class_sub = core.MorastClassDef(
                    element,
                    namespace=self.name,
                    superconfig=self.sc,
                )
            except core.IgnoredItemError as ignored:
                logging.info(ignored.message)
                return
            #
            self.classes.add_subsection(subsection=class_sub)
        elif isinstance(element, ast.FunctionDef):
            try:
                func_sub = core.MorastFunctionDef(
                    element,
                    namespace=self.name,
                    scope=core.SCOPE_MODULE,
                    superconfig=self.sc,
                )
            except core.IgnoredItemError as ignored:
                logging.info(ignored.message)
                return
            #
            self.functions.add_subsection(subsection=func_sub)
        else:
            raise TypeError(
                f"{ast.dump(element)} (line {element.lineno})" " not supported yet"
            )
        #

    @classmethod
    def from_file(
        cls,
        path: pathlib.Path,
        encoding: str = commons.UTF8,
        superconfig=core.DUMMY_SUPERCONFIG,
    ) -> "MorastModule":
        """**Factory method:**
        read the Python module at _path_,
        analyze it, and return a new MorastModule instance from the
        syntax tree returned by **ast.parse()**.

        The module name is simply derived from the file name,
        and in src-based paths, the namespace is determined automatically.

        Remaining arguments:

        *   _encoding_: source file encoding (defaults to `utf-8`)
        *   _superconfig_: a [SuperConfig] instance
            (passed through to the initialization method)
        """
        source = path.read_text(encoding=encoding)
        module_path_parts = path.parent.parts
        namespace = ""
        src_path = "src"
        if src_path in module_path_parts:
            namespace_root_pos = 0
            while src_path in module_path_parts[namespace_root_pos:]:
                namespace_root_pos = (
                    module_path_parts.index("src", namespace_root_pos) + 1
                )
            #
            namespace = ".".join(module_path_parts[namespace_root_pos:])
            logging.debug("Module namespace: %s", namespace)
        #
        module_file = path.name
        module_name = module_file.rsplit(".", 1)[0]
        return cls(
            ast.parse(source=source, filename=path.name),
            name=module_name,
            namespace=namespace,
            superconfig=superconfig,
        )


class LinkList(nodes.MorastBaseNode):
    """A container node with all module links"""

    def __init__(self) -> None:
        """init method to be overridden in subclasses"""
        self.__module_links: Dict[str, mde.ListItem] = {}

    def add_module(self, module: MorastModule) -> None:
        r"""Add a module link; argument:

        *   _module_: a [MorastModule] instance
        """
        elements: List[mds.SafeString] = []
        elements.append(
            mde.Link(module.namespaced_module, url=f"{module.namespaced_module}.md"),
        )
        if module.docstring:
            elements.append(mde.BlockQuote(mds.declare_as_safe(module.docstring)))
        #
        self.__module_links[module.namespaced_module] = mde.ListItem(*elements)

    def as_markdown(self) -> mde.BaseElement:
        """Return a MarkDown element repesenting the node.
        If not overridden, this method simlpy returns a
        MarkDown inline element from the string conversion of the object.
        """
        sorted_links: List[mde.ListItem] = []
        for name in sorted(self.__module_links):
            sorted_links.append(self.__module_links[name])
        #
        return mde.UnorderedList(*sorted_links)


class IndexPage(BasePage):
    """Builds an index page"""

    kind = overrides.KIND_REFINDEX

    def __init__(
        self,
        superconfig=core.DUMMY_SUPERCONFIG,
        headline: str = "Modules Reference",
        docstring: str = "",
    ) -> None:
        r"""
        Initialization arguments:

        *   _superconfig_: a [SuperConfig] instance
        *   _headline_: the index page title
        *   _docstring_: a docstring for the title (raw MarkDown)
        """
        super().__init__(
            "index",
            superconfig=superconfig,
            headline=headline,
        )
        self.docstring = docstring
        self.set_docstring_from_override()
        if self.docstring:
            self.add_subnode(core.MORAST_DOCSTRING, nodes.DocString(self.docstring))
        #
        self.add_subnode("modules", LinkList())

    def add_module(self, module: MorastModule) -> None:
        r"""Add a module link; argument:

        *   _module_: a [MorastModule] instance
        """
        mod_container = self["modules"]
        if isinstance(mod_container, LinkList):
            mod_container.add_module(module)
        #


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
