# pylint: disable=too-many-lines
# -*- coding: utf-8 -*-

"""

morast.core

Core functionality


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
import collections
import logging
import re

from threading import Lock
from typing import Any, Dict, Iterator, List, Optional, Set, Tuple, Union

from smdg import elements as mde

from morast import capabilities
from morast import configuration
from morast import commons
from morast import nodes
from morast import overrides


#
# Constants
#


CLASS_METHOD = 0
STATIC_METHOD = 1
INSTANCE_METHOD = 2
MODULE_LEVEL_FUNCTION = 9

METHOD_TYPES: Tuple[str, str, str] = (
    "Class method",
    "Static method",
    "Instance method",
)

TYPES_BY_DECORATOR: Dict[str, int] = {
    "classmethod": CLASS_METHOD,
    "staticmethod": STATIC_METHOD,
}

SCOPE_CLASS = "class"
SCOPE_INSTANCE = "instance"
SCOPE_MODULE = "module"

METHOD_TARGETS: Dict[int, str] = {
    CLASS_METHOD: SCOPE_CLASS,
    STATIC_METHOD: SCOPE_CLASS,
    INSTANCE_METHOD: SCOPE_INSTANCE,
}

EXCLUDED_MODULE_VARIABLES: Tuple[str, ...] = ("__all__",)

PRX_DATACLASS = re.compile("^(?:dataclasses\\.)?dataclass(?!\\w)")

MORAST_DOCSTRING = f"{commons.BRAND}:docstring"
MORAST_VERBATIM = f"{commons.BRAND}:verbatim"
_MORAST_BASES = f"{commons.BRAND}:bases"
_MORAST_SIGNATURE = f"{commons.BRAND}:signature"


#
# Functions
#


def camel_to_snake_case(name: str) -> str:
    r"""Convert _name_ (an identifier) from CamelCase
    to lower\_snake\_case
    """
    output_collector: List[str] = []
    for index, character in enumerate(name):
        if character.isupper():
            character = character.lower()
            if index:
                output_collector.append(commons.UNDERSCORE)
            #
        output_collector.append(character)
    #
    return "".join(output_collector)


#
# Classes
#


class IgnoredItemError(Exception):
    """Exception to be raised when an item is ignored."""

    def __init__(self, message: str) -> None:
        r"""Initialization arguments:

        *   _message_: the detailed message"""
        self.message = message


class IsAPropertyError(Exception):
    """Exception to be raised when a method has a "property" decorator"""


class SuperConfig:
    r"""Object holding a part of the configuration,
    existing overrides and an OrderedDict of
    extracted OverridesSection objects.
    """

    def __init__(
        self,
        module_overrides=overrides.DUMMY_MOD_OVERRIDES,
        options=configuration.DUMMY_OPTIONS,
    ) -> None:
        r"""
        Initialization arguments:

        *   _module\_overrides_: an overrides.[ModuleOverrides] instance
        *   _options_: a configuration.[GlobalOptions] instance
        """
        self.mor = module_overrides
        self.emoji = configuration.EmojiProxy(options.emoji)
        self.advertise = options.advertise
        self._extracted_sections: collections.OrderedDict[
            Tuple[str, ...],
            Tuple[MorastDocumentableItem, overrides.OverridesSection],
        ] = collections.OrderedDict()

    def get_nested_sections(
        self,
        *name_parts: str,
    ) -> Iterator[overrides.OverridesSection]:
        r"""Return an iterator over extracted override sections,
        in correct order (nested, attributes before functions and classes),
        starting at the name built from _name\_parts_.
        """
        attributes: List[Tuple[str, ...]] = []
        functions: List[Tuple[str, ...]] = []
        classes: List[Tuple[str, ...]] = []
        for sub_name_parts, (candidate, _) in self._extracted_sections.items():
            if len(sub_name_parts) != len(name_parts) + 1:
                continue
            #
            # logging.warning("%r -> %r ???", name_parts, sub_name_parts)
            if sub_name_parts[: len(name_parts)] != name_parts:
                # logging.warning(" -> no")
                continue
            #
            # logging.warning(" -> yes")
            if isinstance(candidate, MorastFunctionDef):
                functions.append(sub_name_parts)
            elif isinstance(candidate, MorastClassDef):
                classes.append(sub_name_parts)
            else:
                attributes.append(sub_name_parts)
            #
        #
        yield self._extracted_sections[name_parts][1]
        for sub_name_parts in attributes + functions + classes:
            yield from self.get_nested_sections(*sub_name_parts)
        #

    def extract_overrides(
        self,
        item: "MorastDocumentableItem",
        namespaced_name: str,
        section: overrides.OverridesSection,
    ):
        r"""Store a tuple containing the [MorastDocumentableItem]
        instance _item_ and the [OverridesSection] instance _section_,
        identifiable by a tuple made from _namespaced\_name_ splitted by dots
        """
        self._extracted_sections[tuple(namespaced_name.split(commons.DOT))] = (
            item,
            section,
        )


DUMMY_SUPERCONFIG = SuperConfig()


# pylint: disable=too-many-instance-attributes


class MorastDocumentableItem:
    """A single documentable item (base class)"""

    kind = overrides.KIND_UNSPECIFIED

    def __init__(
        self,
        name: str,
        namespace: str = "",
        scope: str = SCOPE_MODULE,
        superconfig=DUMMY_SUPERCONFIG,
    ) -> None:
        r"""
        Initialization arguments:

        *   _name_: the name of the item (public attribute)
        *   _namespace_: the namespaced name of the containing
            [MorastSection] instance
        *   _scope_: the scope
        *   _superconfig_: the [SuperConfig] instance passed from the
            containing [MorastSection] instance
        """
        self.name = name
        self.namespace = namespace
        if namespace:
            self.namespaced_name = f"{namespace}.{name}"
        else:
            self.namespaced_name = name
        #
        self.scope = scope
        self.sc = superconfig
        self._original_docstring = True
        self.docstring: str = commons.EMPTY
        self.is_ignored = False

    def check_private(self) -> None:
        """Check if this is a private member"""
        if self.name.startswith(commons.UNDERSCORE):
            raise IgnoredItemError(
                f"{self.namespace}: ignored private member {self.name!r}"
            )
        #

    def check_ignored(self) -> bool:
        """Check for self.is_ignored"""
        if self.is_ignored:
            raise IgnoredItemError(
                f"{self.namespace}: ignored {self.name!r} as specified"
                " through override"
            )
        #
        return False

    def set_docstring_from_override(self) -> None:
        r"""Set the final docstring,
        either from the override if set there,
        or from its former value.

        This method also sets the _is\_ignored_ flag.
        """
        override_section = self.sc.mor.setdefault(
            self.namespaced_name,
            kind=self.kind,
            namespace=self.namespace,
        )
        if override_section.is_ignored:
            self.is_ignored = True
        #
        if self.docstring:
            if override_section.additions:
                self.docstring = f"{self.docstring}\n\n{override_section.docstring}"
                self._original_docstring = False
            elif override_section.docstring:
                self.docstring = override_section.docstring
                self._original_docstring = False
            #
        else:
            if (
                not override_section.docstring
                and not override_section.is_ignored
                and self.kind != overrides.KIND_REFINDEX
            ):
                override_section.add_to_docstring(
                    f"{self.sc.emoji.todo_prefix} **{self.namespaced_name}**"
                    " documentation _to be added_"
                )
            #
            self.docstring = override_section.docstring
            self._original_docstring = False
        # Always add the extracted override section
        self.sc.extract_overrides(self, self.namespaced_name, override_section)

    def markdown_elements(self) -> Iterator[mde.BaseElement]:
        """Return an iterator over MarkDown elements
        if the item is not ignored
        """
        yield mde.Paragraph(self.namespaced_name)
        yield nodes.DocString(self.docstring).as_markdown()

    def as_markdown(self) -> Iterator[mde.BaseElement]:
        """Return an iterator over MarkDown elements
        if the item is not ignored
        """
        if not self.is_ignored:
            yield from self.markdown_elements()
        #


# pylint: enable=too-many-instance-attributes


class MorastBaseAttribute(MorastDocumentableItem):
    """Base class for attributes and properties"""

    # pylint: disable=too-many-arguments

    def __init__(
        self,
        name: str,
        namespace: str = "",
        scope: str = SCOPE_MODULE,
        superconfig=DUMMY_SUPERCONFIG,
        kind: str = overrides.KIND_INSTANCE_ATTRIBUTE,
    ) -> None:
        r"""
        Initialization arguments:

        *   _name_: the name of the attribute (public attribute)
        *   _namespace_: the namespaced name of the containing
            [MorastSection] instance
        *   _scope_: the scope (one of the allowed scopes defined
            in the supported\_scopes class attribute)
        *   _superconfig_: the [SuperConfig] instance passed from the
            containing [MorastSection] instance
        *   _kind_: the item kind (one of KIND\_CONSTANT,
            KIND\_CLASS\_ATTRIBUTE, KIND\_INSTANCE\_ATTRIBUTE
            or KIND\_PROPERTY, all of which are defined
            in the **[overrides]** module)
        """
        super().__init__(
            name,
            namespace=namespace,
            scope=scope,
            superconfig=superconfig,
        )
        logging.debug("ATTRIBUTE NAME: %s", name)
        logging.debug("ATTRIBUTE SCOPE: %s", scope)
        logging.debug("ATTRIBUTE KIND: %s", kind)
        self.check_private()
        self.kind = kind

    def markdown_elements(self) -> Iterator[mde.BaseElement]:
        """Return an iterator over MarkDown elements
        if the item is not ignored
        """
        raise NotImplementedError

    def as_md_list_item(self) -> mde.ListItem:
        """Return aa a MarkDown list item"""
        return mde.ListItem(*self.markdown_elements())


class MorastAttribute(MorastBaseAttribute):
    """A (module, class, or instance) attribute"""

    supported_scopes = (SCOPE_CLASS, SCOPE_INSTANCE, SCOPE_MODULE)

    # pylint: disable=too-many-arguments

    def __init__(
        self,
        element: Union[ast.Assign, ast.AnnAssign, ast.AugAssign],
        namespace: str = "",
        scope: str = SCOPE_MODULE,
        superconfig=DUMMY_SUPERCONFIG,
        check_self: bool = False,
    ) -> None:
        r"""
        Initialization arguments:

        *   _element_: the ast element this instance is built from
        *   _namespace_: the namespaced name of the containing
            [MorastSection] instance
        *   _scope_: the scope (one of the allowed scopes defined
            in the supported\_scopes class attribute)
        *   _superconfig_: the [SuperConfig] instance passed from the
            containing [MorastSection] instance
        *   _check\_self_: a flag determining whether to ckeck for
            a `self.` prefix (suitable for instance attributes only).
            If this is `True`, the leading `self.` is stripped from the name
        """
        if scope not in self.supported_scopes:
            raise ValueError(f"scope must be one of {self.supported_scopes!r}")
        #
        prefix_by_scope: Dict[str, str] = {
            SCOPE_CLASS: f"{superconfig.emoji.class_attributes_prefix}" f" {namespace}",
            SCOPE_INSTANCE: f"{superconfig.emoji.instance_attributes_prefix} ",
            SCOPE_MODULE: f"{superconfig.emoji.constants_prefix} {namespace}",
        }
        logging.debug(ast.dump(element))
        assignment = nodes.Assignment(element, prefix=f"{prefix_by_scope[scope]}.")
        logging.debug(str(assignment))
        name = str(assignment.target)
        kind = overrides.KIND_CONSTANT
        if scope == SCOPE_INSTANCE:
            kind = overrides.KIND_INSTANCE_ATTRIBUTE
            if check_self:
                if name.startswith("self."):
                    assignment.strip_first()
                    name = str(assignment.target)
                else:
                    raise IgnoredItemError(f"{name}: no instance attribute")
                #
            #
        elif scope == SCOPE_CLASS:
            kind = overrides.KIND_CLASS_ATTRIBUTE
        #
        if commons.DOT in name:
            raise IgnoredItemError(f"{name}: ignored namespaced assignment")
        #
        super().__init__(
            name,
            namespace=namespace,
            scope=scope,
            superconfig=superconfig,
            kind=kind,
        )
        self.set_docstring_from_override()
        self.check_ignored()
        self.assignment = assignment
        if self.sc.mor[self.namespaced_name].value_is_stripped:
            self.assignment.operator = None
        #

    def markdown_elements(self) -> Iterator[mde.BaseElement]:
        """Return an iterator over MarkDown elements
        if the item is not ignored
        """
        yield mde.Paragraph(self.assignment.as_markdown())
        yield nodes.DocString(self.docstring).as_markdown()


class MorastProperty(MorastBaseAttribute):
    """An instance property"""

    # pylint: disable=too-many-arguments

    def __init__(
        self,
        element: ast.FunctionDef,
        namespace: str = "",
        superconfig=DUMMY_SUPERCONFIG,
    ) -> None:
        r"""
        Initialization arguments:

        *   _element_: the ast.FunctionDef instance of the property
        *   _namespace_: the namespaced name of the containing
            [MorastSection] instance
        *   _superconfig_: the [SuperConfig] instance passed from the
            containing [MorastSection] instance
        *   _docstring_: the docstring from the property method
        *   _type\_annotation_: the type annotation
        """
        super().__init__(
            element.name,
            namespace=namespace,
            scope=SCOPE_INSTANCE,
            superconfig=superconfig,
            kind=overrides.KIND_PROPERTY,
        )
        self.type_annotation: str = commons.EMPTY
        if isinstance(element.returns, (ast.AST, str)):
            self.type_annotation = str(nodes.get_node(element.returns))
        #
        # docstring: str = commons.EMPTY
        for sub_element in element.body:
            if isinstance(sub_element, ast.Expr):
                if isinstance(sub_element.value, ast.Constant):
                    self.docstring = nodes.remove_hanging_indent(
                        sub_element.value.value.strip(),
                        level=2,
                    )
                    break
                #
            #
        #
        self.set_docstring_from_override()
        self.check_ignored()

    def markdown_elements(self) -> Iterator[mde.BaseElement]:
        """Return an iterator over MarkDown elements
        if the item is not ignored
        """
        signature_elements: List[mde.BaseElement] = [
            mde.ItalicText("readonly property"),
            mde.InlineElement(f" {self.sc.emoji.property_prefix} "),
            mde.BoldText(f".{self.name}"),
        ]
        if self.type_annotation:
            signature_elements.append(mde.InlineElement(f": {self.type_annotation}"))
        #
        yield mde.Paragraph(mde.CompoundInlineElement(*signature_elements))
        yield nodes.DocString(self.docstring, level=0).as_markdown()


class MorastSection(MorastDocumentableItem):
    """Documentation section with a headline and other nodes.
    May also contain other sections.

    Keeps an internal collection of contained
    MorastBaseNode and [MorastSection] instances.
    """

    # pylint: disable=too-many-arguments

    def __init__(
        self,
        name: str,
        namespace: str = "",
        scope=SCOPE_MODULE,
        superconfig=DUMMY_SUPERCONFIG,
        level: int = 1,
        headline: Optional[str] = None,
    ) -> None:
        r"""
        Initialization arguments:

        *   _name_: the name of the section (public attribute)
        *   _namespace_: the namespaced name of the containing
            [MorastSection] instance
        *   _scope_: the scope
        *   _superconfig_: the [SuperConfig] instance passed from the
            containing [MorastSection] instance
        *   _level_: section level in the document hierarchy
        *   _headline_: deviant headline if provided
            (else, the headline will just be _name_)
        """
        super().__init__(
            name, namespace=namespace, scope=scope, superconfig=superconfig
        )
        if isinstance(headline, str):
            self._headline = headline
        else:
            self._headline = self.name
        #
        self._level = level
        self._contents: collections.OrderedDict[
            str, Union[nodes.MorastBaseNode, MorastDocumentableItem]
        ] = collections.OrderedDict()
        self._naming_lock = Lock()

    def __getitem__(
        self,
        name: str,
    ) -> Union[nodes.MorastBaseNode, MorastDocumentableItem]:
        """Directly return the item stored as _name_"""
        return self._contents[name]

    def __delitem__(
        self,
        name: str,
    ) -> None:
        """Delete the item stored as _name_"""
        del self._contents[name]

    def __len__(self) -> int:
        """Total number of contained nodes and subsections"""
        return len(self._contents)

    def items(
        self,
    ) -> Iterator[Tuple[str, Union[nodes.MorastBaseNode, MorastDocumentableItem]]]:
        """Return an iterator (name, item tuples)
        over all contained items
        """
        yield from self._contents.items()

    def subsections(self) -> Iterator[Tuple[str, "MorastSection"]]:
        r"""Return an iterator (name_, subsection\_instance tuples)
        over all contained [MorastSection] instances
        """
        for sub_name, subnode in self.items():
            if isinstance(subnode, MorastSection):
                yield sub_name, subnode
            #
        #

    def adjust_level(self, new_level: int) -> None:
        r"""Change the level to _new\_level_,
        recurse into all subsections and
        propagate the change.
        If a docstring is present, adjust its level as well.
        """
        self._level = new_level
        for _, child_section in self.subsections():
            child_section.adjust_level(new_level + 1)
        #
        try:
            docstring = self[MORAST_DOCSTRING]
        except KeyError:
            return
        #
        if isinstance(docstring, nodes.DocString):
            docstring.adjust_level(new_level)
        #

    def _get_unique_name(self, name: str) -> str:
        """Return a new unique name instead of _name_.
        Should be called only while holding `self._naming_lock`.
        """
        number = 0
        candidate = name
        while candidate in self._contents:
            number += 1
            candidate = f"{name}_{number}"
            if number > 1000:
                raise ValueError("Exhausted renaming attempts")
            #
        #
        return candidate

    def add_subnode(
        self,
        name: str,
        subitem: Union[nodes.MorastBaseNode, "MorastSection"],
    ) -> None:
        """Add _subitem_ (a node or section)
        and make it accessible through _name_.
        """
        self._contents.setdefault(name, subitem)
        if subitem is not self._contents[name]:
            with self._naming_lock:
                unique_name = self._get_unique_name(name)
                self._contents[unique_name] = subitem
            #
        #

    def add_subsection(
        self,
        name: str = "undefined",
        subsection: Optional["MorastSection"] = None,
    ) -> None:
        """Add a new subsection.
        If a [MorastSection] instance is provided through _subsection_,
        store it, make it available under its own name,
        and adjust its level to reflect the sections hierarchy.
        else initialize a new one and and make it available as _name_.
        """
        if subsection is None:
            subsection = MorastSection(name, level=self._level + 1)
        else:
            sub_name = subsection.name
            subsection.adjust_level(self._level + 1)
        #
        self.add_subnode(sub_name, subsection)

    def markdown_elements(self) -> Iterator[mde.BaseElement]:
        """Return an iterator over MarkDown elements for all
        contained nodes, recursing into all subsections.
        """
        if self._level > 1:
            yield nodes.MD_HR20
        #
        logging.debug("Section: %r", self.name)
        yield mde.Header(self._level, self._headline)
        for sub_name, sub_element in self._contents.items():
            logging.debug("MarkDown Elements from: %r", sub_name)
            if isinstance(sub_element, MorastDocumentableItem):
                yield from sub_element.markdown_elements()
            else:
                yield sub_element.as_markdown()
            #
        #


class ImplementedCapabilities(MorastSection):
    """Implemente capabilities section"""

    supported_scopes = (SCOPE_CLASS, SCOPE_MODULE)

    def __init__(
        self,
        implemented_capabilities: capabilities.Collector,
    ) -> None:
        r"""
        Initialization argument:

        *   _implemented\_capabilities_: a capabilities.Collector instance
        """
        super().__init__(
            "implemented_capabilities",
            namespace="",
            scope=SCOPE_CLASS,
            superconfig=DUMMY_SUPERCONFIG,
            level=4,
            headline="Implemented capabilities",
        )
        self._implemented_capabilities = implemented_capabilities

    def markdown_elements(self) -> Iterator[mde.BaseElement]:
        """Yield markdown elements"""
        yield mde.Header(self._level, self._headline)
        md_list_items: List[mde.ListItem] = []
        for implemented_md_item in self._implemented_capabilities.as_markdown():
            md_list_items.append(implemented_md_item)
        #
        yield mde.UnorderedList(*md_list_items)


class MorastAttributesList(MorastSection):
    """Attributes List,
    container for several [MorastBaseAttribute] instances
    """

    supported_scopes = (SCOPE_CLASS, SCOPE_MODULE)

    def __init__(
        self,
        name: str,
        scope: str = SCOPE_MODULE,
        superconfig=DUMMY_SUPERCONFIG,
        headline: Optional[str] = None,
    ) -> None:
        r"""
        Initialization arguments:

        *   _name_: the name of the attributes list
        *   _scope_: the scope (one of the allowed scopes defined
            in the supported\_scopes class attribute)
        *   _superconfig_: the [SuperConfig] instance passed from the
            containing [MorastModule] or [MorastClassDef] instance
        *   _headline_: the headline if different from the name
        """

        level = 2 if scope == SCOPE_MODULE else 4
        super().__init__(
            name,
            namespace="",
            scope=scope,
            superconfig=superconfig,
            level=level,
            headline=headline,
        )
        self._attributes: collections.OrderedDict[str, MorastBaseAttribute] = (
            collections.OrderedDict()
        )

    def add(self, mor_attr: MorastBaseAttribute) -> None:
        """Store _mor_attr_ under its name"""
        self._attributes[mor_attr.name] = mor_attr

    def remove(self, attr_name: str) -> None:
        """Remove the attribute named _attr_name_ if it exists"""
        self._attributes.pop(attr_name, None)

    def __getitem__(self, attr_name: str) -> MorastBaseAttribute:
        """Attribute access via name"""
        return self._attributes[attr_name]

    def __len__(self) -> int:
        """Total number of contained nodes and subsections"""
        return len(self._attributes)

    def markdown_elements(self) -> Iterator[mde.BaseElement]:
        """Yield markdown elements"""
        yield mde.Header(self._level, self._headline)
        md_list_items: List[mde.ListItem] = []
        for mor_attr in self._attributes.values():
            md_list_items.append(mor_attr.as_md_list_item())
        #
        yield mde.UnorderedList(*md_list_items)


class MorastFunctionDef(MorastSection):
    """Represents a module-level function,
    or a class, static, or instance method.
    """

    supported_scopes = (SCOPE_CLASS, SCOPE_INSTANCE, SCOPE_MODULE)

    # pylint: disable=too-many-branches

    def __init__(
        self,
        element: ast.FunctionDef,
        namespace: str = "",
        scope: str = SCOPE_MODULE,
        superconfig=DUMMY_SUPERCONFIG,
    ) -> None:
        r"""
        Initialization arguments:

        *   _element_: the ast.FunctionDef instance from which
            the function name, signature and docstring are determined
        *   _namespace_: the namespaced name of the class
            if the function is a method
        *   _scope_: the scope (one of the allowed scopes defined
            in the supported\_scopes class attribute)
        *   _superconfig_: the [SuperConfig] instance passed from the
            containing [MorastModule] or [MorastClassDef] instance
        """
        parent_name = namespace.split(commons.DOT)[-1]
        self.function_type = MODULE_LEVEL_FUNCTION
        level = 3
        if scope != SCOPE_MODULE:
            level = 4
            self.function_type = INSTANCE_METHOD
            for dec in element.decorator_list:
                if isinstance(dec, ast.Name):
                    if dec.id == "property":
                        raise IsAPropertyError
                    #
                    try:
                        self.function_type = TYPES_BY_DECORATOR[dec.id]
                    except KeyError:
                        continue
                    #
                    break
                #
            #
        #
        name = element.name
        logging.debug("%s - accepted %s", namespace, name)
        skip_first_arg = False
        if self.function_type in (CLASS_METHOD, INSTANCE_METHOD):
            skip_first_arg = True
        #
        if self.function_type == INSTANCE_METHOD:
            headline_prefix = f"{camel_to_snake_case(parent_name)}_instance."
            signature_prefix = "."
            kind = overrides.KIND_INSTANCE_METHOD
        else:
            signature_prefix = f"{parent_name}."
            if self.function_type == MODULE_LEVEL_FUNCTION:
                headline_prefix = "Function: "
                kind = overrides.KIND_FUNCTION
            else:
                headline_prefix = signature_prefix
                kind = overrides.KIND_CLASS_METHOD
            #
        #
        if self.function_type == STATIC_METHOD:
            signature_prefix = f"staticmethod {signature_prefix}"
        #
        super().__init__(
            name,
            namespace=namespace,
            scope=scope,
            superconfig=superconfig,
            level=level,
            headline=f"{headline_prefix}{name}()",
        )
        self.check_private()
        for sub_element in element.body:
            if isinstance(sub_element, ast.Expr):
                if isinstance(sub_element.value, ast.Constant):
                    # self.docstring = sub_element.value.value
                    self.docstring = nodes.remove_hanging_indent(
                        sub_element.value.value.strip(),
                        level=self._level - 2,
                    )
                    break
                #
            #
        #
        signature_prefix = f"{self.sc.emoji.signature_prefix} {signature_prefix}"
        self.add_subnode(
            _MORAST_SIGNATURE,
            nodes.Signature(
                self.name,
                element.args,
                returns=element.returns,
                prefix=signature_prefix,
                skip_first_arg=skip_first_arg,
            ),
        )
        self.kind = kind
        self.set_docstring_from_override()
        self.check_ignored()
        self.add_subnode(
            MORAST_DOCSTRING,
            nodes.DocString(self.docstring, level=0),
        )


# pylint: disable=too-many-instance-attributes
class MorastClassDef(MorastSection):
    """Represents a class."""

    kind = overrides.KIND_CLASS

    # pylint: disable=too-many-branches
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-statements

    def __init__(
        self,
        element: ast.ClassDef,
        namespace: str = "",
        superconfig=DUMMY_SUPERCONFIG,
    ) -> None:
        r"""
        Initialization arguments:

        * _element_: the ast.ClassDef instance from which
          the class name, signature, docstring, attributes
          and methods are determined
        * _namespace_: the namespace of the class
        * _superconfig_: the [SuperConfig] instance passed from the
          containing [MorastModule] instance
        """
        name = element.name
        decorators: List[nodes.MorastBaseNode] = [
            nodes.get_node(single_dec) for single_dec in element.decorator_list
        ]
        class_prefix = "Class"
        self.is_a_dataclass = False
        for item in decorators:
            dec_str = str(item)
            if PRX_DATACLASS.match(dec_str):
                self.is_a_dataclass = True
                class_prefix = "Dataclass"
                if "(frozen=True)" in dec_str:
                    class_prefix = "Frozen dataclass"
                #
                break
            #
        #
        super().__init__(
            name,
            namespace=namespace,
            superconfig=superconfig,
            level=3,
            headline=f"{class_prefix} {name}()",
        )
        self.check_private()
        inheritance_prefix = self.sc.emoji.inheritance_prefix
        self._init_method: Optional[ast.FunctionDef] = None
        self._implemented_specials = capabilities.Collector(
            f"{camel_to_snake_case(self.name)}_instance"
        )
        self.existing_attributes: Dict[str, Set[str]] = {
            SCOPE_CLASS: set(),
            SCOPE_INSTANCE: set(),
        }
        self.attribute_lists: Dict[str, MorastAttributesList] = {}
        self.methods: Dict[str, MorastSection] = {}
        for scope in (SCOPE_CLASS, SCOPE_INSTANCE):
            self.attribute_lists[scope] = MorastAttributesList(
                f"{scope} attributes",
                superconfig=superconfig,
                scope=scope,
            )
            self.methods[scope] = MorastSection(
                f"{scope} methods", superconfig=superconfig, level=self._level
            )
        #
        self._init_docstring: str = commons.EMPTY
        for sub_element in element.body:
            if isinstance(sub_element, ast.Expr):
                if isinstance(sub_element.value, ast.Constant):
                    self.docstring = nodes.remove_hanging_indent(
                        sub_element.value.value.strip(),
                        level=1,
                    )
                    continue
                #
            elif isinstance(sub_element, (ast.Assign, ast.AnnAssign)):
                if self.is_a_dataclass:
                    self._add_instance_attribute(sub_element, check_self=False)
                    continue
                self._add_class_attribute(sub_element)
            elif isinstance(sub_element, ast.FunctionDef):
                self._add_method(sub_element)
            #
        #
        # TODO: handle inheritance
        bases: List[Any] = getattr(element, "bases", [])
        if bases:
            self.add_subnode(
                _MORAST_BASES,
                nodes.MorastClassBases(*bases, prefix=f"{inheritance_prefix} "),
            )
        #
        if isinstance(self._init_method, ast.FunctionDef):
            self._add_signature(self._init_method)
        #
        if self.docstring:
            if self._init_docstring:
                self.docstring = f"{self.docstring}\n\n{self._init_docstring}"
            #
        else:
            self.docstring = self._init_docstring
        #
        self.set_docstring_from_override()
        self.check_ignored()
        self.add_subnode(
            MORAST_DOCSTRING,
            nodes.DocString(self.docstring, level=0),
        )
        if self._implemented_specials:
            self.add_subsection(
                subsection=ImplementedCapabilities(self._implemented_specials)
            )
        #
        for scope in (SCOPE_CLASS, SCOPE_INSTANCE):
            if len(self.attribute_lists[scope]):
                self.add_subsection(subsection=self.attribute_lists[scope])
            #
        #
        for scope in (SCOPE_CLASS, SCOPE_INSTANCE):
            for method_name, method_sect in self.methods[scope].subsections():
                self.add_subsection(method_name, method_sect)
            #
        #

    def _add_method(self, element: ast.FunctionDef) -> None:
        """Add method"""
        method_name = str(element.name)
        if method_name == "__init__":
            self._init_method = element
            for init_statement in self._init_method.body:
                if not self._init_docstring and isinstance(init_statement, ast.Expr):
                    if isinstance(init_statement.value, ast.Constant):
                        self._init_docstring = nodes.remove_hanging_indent(
                            init_statement.value.value.strip(),
                            level=2,
                        )
                        continue
                    #
                #
                if isinstance(init_statement, (ast.Assign, ast.AnnAssign)):
                    self._add_instance_attribute(init_statement)
                #
            #
            return
        #
        try:
            self._implemented_specials.add_method(element)
        except (
            capabilities.NoSpecialMethodError,
            capabilities.UnsupportedMethodError,
        ):
            pass
        else:
            return
        #
        try:
            method = MorastFunctionDef(
                element,
                namespace=self.namespaced_name,
                superconfig=self.sc,
                scope=SCOPE_CLASS,
            )
        except IgnoredItemError as ignored:
            logging.info(ignored.message)
            return
        except IsAPropertyError:
            # self._add_property(element)
            self.attribute_lists[SCOPE_INSTANCE].add(
                MorastProperty(
                    element,
                    namespace=self.namespaced_name,
                    superconfig=self.sc,
                )
            )
            return
        #
        self.methods[METHOD_TARGETS[method.function_type]].add_subsection(
            subsection=method
        )

    def _add_attribute(
        self,
        element: Union[ast.Assign, ast.AnnAssign],
        scope: str,
        check_self: bool = False,
    ) -> None:
        """Add an attribute

        _scope_ may be SCOPE_CLASS or SCOPE_INSTANCE
        """
        try:
            new_attribute = MorastAttribute(
                element,
                namespace=self.namespaced_name,
                superconfig=self.sc,
                scope=scope,
                check_self=check_self,
            )
        except IgnoredItemError as ignored:
            logging.info(ignored.message)
            return
        #
        if new_attribute.name in self.existing_attributes[scope]:
            return
        #
        self.attribute_lists[scope].add(new_attribute)
        self.existing_attributes[scope].add(new_attribute.name)
        logging.debug(
            "%s: accepted %s attribute %r",
            self.namespaced_name,
            scope,
            new_attribute.name,
        )
        if (
            scope == SCOPE_INSTANCE
            and new_attribute.name in self.existing_attributes[SCOPE_CLASS]
        ):
            self.attribute_lists[SCOPE_CLASS].remove(new_attribute.name)
            self.existing_attributes[SCOPE_CLASS].remove(new_attribute.name)
        #

    def _add_class_attribute(self, element: Union[ast.Assign, ast.AnnAssign]) -> None:
        """Add an instance attribute if it does not exist yet"""
        if self.is_a_dataclass:
            raise ValueError("this is a dataclass and has no class attributes")
        #
        self._add_attribute(element, SCOPE_CLASS)

    def _add_instance_attribute(
        self,
        element: Union[ast.Assign, ast.AnnAssign],
        check_self: bool = True,
    ) -> None:
        """Add an instance attribute if it does not exist yet"""
        self._add_attribute(element, SCOPE_INSTANCE, check_self=check_self)

    def _add_signature(
        self,
        init_method: ast.FunctionDef,
    ) -> None:
        """Add the signature"""
        self.add_subnode(
            _MORAST_SIGNATURE,
            nodes.Signature(
                self.name,
                init_method.args,
                returns=None,
                prefix=f"{self.sc.emoji.signature_prefix} {self.namespace}.",
                skip_first_arg=True,
            ),
        )


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
