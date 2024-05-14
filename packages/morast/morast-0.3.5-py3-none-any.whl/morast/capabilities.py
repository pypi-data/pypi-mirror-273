# -*- coding: utf-8 -*-

"""

morast.capabilities

Capabiliiies through special methods


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
import dataclasses
import re

from typing import Any, Dict, Iterator, List, Optional, Tuple

from smdg import elements as mde
from smdg import strings as mds

from morast import commons
from morast import nodes


RICH_COMPARISONS: Dict[str, str] = {
    "lt": "<",
    "gt": ">",
    "le": "<=",
    "ge": ">=",
    "eq": "==",
    "ne": "!=",
}
BASIC_METHODS: Tuple[str, ...] = (
    "str",
    "repr",
    "hash",
    "bool",
    *RICH_COMPARISONS,
)

PRX_SPECIAL_METHOD = re.compile(r"\A__([a-z]+(?:_[a-z]+)*)__\Z")


#
# Classes
#


class DuplicateNameError(Exception):
    """Raised if there exists already a special method with this name"""


class NoSpecialMethodError(Exception):
    """Raised if the method is not a special method"""


class NotHandledInThisGroupError(Exception):
    """Raised if a special method is not handled by thos group"""


class UnsupportedMethodError(Exception):
    """Raised if the method is not (yet) supported"""


@dataclasses.dataclass(frozen=True)
class SpecialMethod:
    """Stores data of a special method"""

    name: str
    docstring: str
    arguments: ast.arguments
    returns: Optional[ast.AST] = None

    @property
    def args(self) -> List[ast.arg]:
        """Return posonlyargs and args concatenated"""
        return self.arguments.posonlyargs + self.arguments.args

    @property
    def args_signature(self) -> List[str]:
        """Return a list of strings representing the arguments part
        of the method signature
        """
        args_sig: List[str] = []
        posonlyargs = self.arguments.posonlyargs
        args_ = self.arguments.args
        vararg = getattr(self.arguments, "vararg", None)
        kwonlyargs = self.arguments.kwonlyargs
        kw_defaults = self.arguments.kw_defaults
        kwarg = getattr(self.arguments, "kwarg", None)
        posonly_present = len(posonlyargs) > 1
        num_args = len(args_)
        # num_pos_defaults = len(defaults)
        if posonly_present:
            num_position = len(posonlyargs) + num_args
            for index_, current_arg in enumerate(posonlyargs):
                if not index_:
                    continue
                #
                args_sig.append(
                    self.get_annotated_arg_item(
                        current_arg,
                        self.get_nth_last_default(num_position - index_),
                    )
                )
            #
            args_sig.append("/")
        #
        for index_, current_arg in enumerate(args_):
            if not posonlyargs and not index_:
                continue
            #
            args_sig.append(
                self.get_annotated_arg_item(
                    current_arg,
                    self.get_nth_last_default(num_args - index_),
                )
            )
        #
        if vararg:
            args_sig.append(f"*{self.get_annotated_arg_item(vararg)}")
        elif args_ and kwonlyargs:
            args_sig.append("*")
        #
        for index_, current_arg in enumerate(kwonlyargs):
            args_sig.append(
                self.get_annotated_arg_item(
                    current_arg,
                    kw_defaults[index_],
                )
            )
        #
        if kwarg:
            args_sig.append(f"**{self.get_annotated_arg_item(kwarg)}")
        #
        return args_sig

    @staticmethod
    def get_annotated_arg_item(
        arg_obj: ast.arg, default: Optional[ast.AST] = None, /
    ) -> str:
        """Return the string representation of an argument,
        with annotation and/or default value if defined.
        """
        arg_str = arg_obj.arg
        arg_ann = getattr(arg_obj, "annotation", None)
        if arg_ann is not None:
            arg_str = f"{arg_str}: {nodes.get_node(arg_ann)}"
        #
        if default is None:
            return arg_str
        #
        default_str = str(nodes.get_node(default))
        if arg_ann is None:
            return f"{arg_str}={default_str}"
        #
        return f"{arg_str} = {default_str}"

    def get_nth_last_default(self, index_: int) -> Optional[ast.AST]:
        r"""Returns the default value at _index\__,
        counting from the end of the _defaults_ attribute of _arguments_.

        Returns None if no default value is defined
        (ie. _index\__ exceeds the size of the list).
        """
        try:
            return self.arguments.defaults[-index_]
        except IndexError:
            return None
        #


class BaseSignature:
    """Signature of a capability, base class"""

    format_string = "<capability {0.name!r} of {0.instance_name}{0.return_annotation}>"

    def __init__(
        self, name: str, instance_name: str, returns: str = commons.EMPTY
    ) -> None:
        r"""Initialization arguments:

        *   _name_: the name of the capability
        *   _instance\_name_: the instance name as it should appear
            in the generated documentation
        *   _returns_: the return annotation a string
        """
        self.name = name
        self.instance_name = instance_name
        self.returns = returns

    @property
    def return_annotation(self) -> str:
        """The string representation of the return annotation if defined,
        else an empty string.
        """
        if self.returns:
            return f" → {self.returns}"
        #
        return commons.EMPTY

    def __eq__(self, other) -> bool:
        r"""BaseSignature and subclasses instances compare equal
        if they are of the same type and if the
        _name_, _returns_, and _instance\_name_ attributes
        of both instances match
        """
        if all(
            (
                self.__class__.__name__ == other.__class__.__name__,
                self.name == other.name,
                self.returns == other.returns,
                self.instance_name == other.instance_name,
            )
        ):
            return True
        #
        return False

    def __str__(self) -> str:
        r"""BaseSignature and subclasses instances’ string representations
        are built using the _format\_string_ attribute.
        """
        return self.format_string.format(self)

    @classmethod
    def from_method(cls, method: SpecialMethod, instance_name: str) -> "BaseSignature":
        r"""Factory method:
        initialize from the SpecialMethod instance _method_
        with _instance\_name_ explicitly added
        """
        name = method.name
        returns = commons.EMPTY
        if method.returns:
            returns = str(nodes.get_node(method.returns))
        #
        return cls(name, instance_name, returns=returns)


class FunctionSignature(BaseSignature):
    """Signature of a capability implementing a generic function
    (str, repr, bool, hash, len, etc.)
    """

    format_string = "{0.name}({0.instance_name}){0.return_annotation}"


class RichComparisonSignature(BaseSignature):
    """Rich comparison signature"""

    format_string = "{0.instance_name} {0.comparison} {0.other_name}"

    def __init__(
        self,
        name: str,
        instance_name: str,
        returns: str = commons.EMPTY,
        other_name: str = "default_other",
    ) -> None:
        r"""Initialization arguments:

        *   _name_: the name of the capability
        *   _instance\_name_: the instance name as it should appear
            in the generated documentation
        *   _returns_: the return annotation a string (not used in this class)
        *   _other\_name_: the name of the compared instance
            as it should appear in the generated documentation
        """
        super().__init__(name, instance_name, returns=commons.EMPTY)
        self.comparison = RICH_COMPARISONS[name]
        self.other_name = other_name

    @classmethod
    def from_method(
        cls, method: SpecialMethod, instance_name: str
    ) -> "RichComparisonSignature":
        r"""Factory method:
        initialize from the SpecialMethod instance _method_
        with _instance\_name_ explicitly added
        """
        name = method.name
        try:
            other_name = method.args[1].arg
        except IndexError:
            other_name = "default_other"
        #
        return cls(name, instance_name, returns=commons.EMPTY, other_name=other_name)


class CustomFormattedSignature(BaseSignature):
    """Custom formatted signature"""

    def __init__(
        self,
        name: str,
        instance_name: str,
        returns: str = commons.EMPTY,
        format_string: str = "",
        **kwargs,
    ) -> None:
        r"""Initialization arguments:

        *   _name_: the name of the capability
        *   _instance\_name_: the instance name as it should appear
            in the generated documentation
        *   _returns_: the return annotation a string (not used in this class)
        *   _format\_string_: a format string
        *   kwargs: additional parameters as keyword arguments
        """
        super().__init__(name, instance_name, returns=returns)
        self.format_string = format_string
        self.__data: Dict[str, Any] = kwargs

    def __getattr__(self, name: str) -> Any:
        """The data item stored as _name_"""
        try:
            return self.__data[name]
        except KeyError as error:
            raise AttributeError(name) from error
        #

    @classmethod
    def from_method(
        cls,
        method: SpecialMethod,
        instance_name: str,
        format_string: str = "",
        **kwargs,
    ) -> "CustomFormattedSignature":
        r"""Factory method:
        initialize from the SpecialMethod instance _method_
        with _instance\_name_ explicitly added
        """
        name = method.name
        returns = commons.EMPTY
        if method.returns:
            returns = str(nodes.get_node(method.returns))
        #
        return cls(
            name,
            instance_name,
            returns=returns,
            format_string=format_string,
            **kwargs,
        )


@dataclasses.dataclass(frozen=True)
class Capability:
    """Stores the capability of a special method"""

    signature: BaseSignature
    docstring: str


class SpecialMethodsGroupBase:
    """Special methods group base class"""

    handled_methods: Tuple[str, ...] = ()

    def __init__(self, instance_var: str) -> None:
        r"""Initialization argument:

        *   _instance\_var_: Variable name to use as the representation
            of an instance of the documented class
        """
        self.__instance_var: str = instance_var
        self.__methods: Dict[str, SpecialMethod] = {}

    def __getitem__(self, name: str) -> SpecialMethod:
        """Access a stored method by its _name_"""
        return self.__methods[name]

    def __contains__(self, name: str) -> bool:
        """True if a special method with name _name_ is stored"""
        return name in self.__methods

    def __len__(self) -> int:
        """The number of stored SpecialMethod instances"""
        return len(self.__methods)

    @property
    def instance_var(self) -> str:
        """The instance variable"""
        return self.__instance_var

    def add_method(self, parsed_function: ast.FunctionDef) -> None:
        r"""Store a SpecialMethod instance created from _parsed\_function_"""
        func_match = PRX_SPECIAL_METHOD.match(parsed_function.name)
        if func_match is None:
            raise NoSpecialMethodError
        #
        func_name = func_match.group(1)
        if func_name in self:
            raise DuplicateNameError
        #
        if func_name not in self.handled_methods:
            raise NotHandledInThisGroupError
        #
        docstring = commons.EMPTY
        for sub_element in parsed_function.body:
            if isinstance(sub_element, ast.Expr):
                # self.docstring =
                if isinstance(sub_element.value, ast.Constant):
                    docstring = sub_element.value.value
                    break
                #
            #
        #
        self.__methods[func_name] = SpecialMethod(
            func_name,
            docstring,
            parsed_function.args,
            returns=getattr(parsed_function, "returns", None),
        )

    def get_capability(self, name: str) -> Capability:
        """Return a capability instance"""
        docstring = self[name].docstring
        signature = self.get_signature(name)
        return Capability(signature, docstring)

    def get_signature(self, name: str) -> BaseSignature:
        """Return a BaseSignature (subclass) instance"""
        return BaseSignature.from_method(self[name], self.instance_var)

    def implementations(self) -> Iterator[Capability]:
        """Return an iterator over the implemented capabilities"""
        for name in self.__methods:
            yield self.get_capability(name)
        #


class BasicCustomizationGroup(SpecialMethodsGroupBase):
    """Special Methods group: Basic customization,
    compare [Basic customization methods]
    """

    handled_methods = BASIC_METHODS

    def get_signature(self, name: str) -> BaseSignature:
        """Return a BaseSignature (subclass) instance"""
        try:
            return RichComparisonSignature.from_method(self[name], self.instance_var)
        except KeyError:
            return FunctionSignature.from_method(self[name], self.instance_var)
        #


class ContainerTypesEmulationGroup(SpecialMethodsGroupBase):
    """Special Methods group: Emulating container types,
    compare [Emulating container types]
    """

    _func_sig_methods: Tuple[str, ...] = ("len", "iter", "reversed")
    _fs_by_method: Dict[str, str] = {
        "getitem": "{0.instance_name}[{0.key}]{0.return_annotation}",
        "setitem": "{0.instance_name}[{0.key}] = {0.value}",
        "delitem": "del {0.instance_name}[{0.key}]",
        "contains": "{0.key} in {0.instance_name}{0.return_annotation}",
    }
    handled_methods = (*_func_sig_methods, *_fs_by_method)

    def get_signature(self, name: str) -> BaseSignature:
        """Return a BaseSignature (subclass) instance"""
        if name in self._func_sig_methods:
            return FunctionSignature.from_method(self[name], self.instance_var)
        #
        format_string = self._fs_by_method[name]
        method_args = self[name].args
        sig_kwargs: Dict[str, str] = {"key": method_args[1].arg}
        if name == "setitem":
            sig_kwargs["value"] = method_args[2].arg
        #
        return CustomFormattedSignature.from_method(
            self[name],
            self.instance_var,
            format_string=format_string,
            **sig_kwargs,
        )


class CallableObjectsEmulationGroup(SpecialMethodsGroupBase):
    """Special Methods group: Emulating callable objects,
    compare [Emulating callable objects]
    """

    handled_methods = ("call",)

    def get_signature(self, name: str) -> BaseSignature:
        """Return a BaseSignature (subclass) instance"""
        # method_args = self[name].args
        sig_args: List[str] = self[name].args_signature
        return CustomFormattedSignature.from_method(
            self[name],
            self.instance_var,
            format_string=("{0.instance_name}({0.call_args}){0.return_annotation}"),
            call_args=", ".join(sig_args),
        )


class Collector:
    """Collects capabilities per class"""

    basic_customization = "basic customization"
    container_types_emulation = "container types emulation"
    callable_objects = "callable objects"
    supported_groups: Tuple[str, ...] = (
        basic_customization,
        container_types_emulation,
        callable_objects,
    )

    def __init__(self, instance_var: str) -> None:
        r"""Initialization arguments:

        *   _instance\_var_: The variable name to use as the representation
            of an instance of the documented class
        """
        self.__groups: Dict[str, SpecialMethodsGroupBase] = {
            self.basic_customization: BasicCustomizationGroup(instance_var),
            self.container_types_emulation: ContainerTypesEmulationGroup(instance_var),
            self.callable_objects: CallableObjectsEmulationGroup(instance_var),
        }

    def __getitem__(self, name: str) -> SpecialMethodsGroupBase:
        """Access a stored group by its _name_"""
        return self.__groups[name]

    def __bool__(self) -> bool:
        """Collector instances evaluate to `True`
        if any capability is implemented.
        """
        return any(
            (
                bool(special_methods_group)
                for special_methods_group in self.__groups.values()
            )
        )

    def add_method(self, parsed_method: ast.FunctionDef) -> None:
        r"""Add the capability implemented by the
        [ast.FunctionDef] instance _parsed\_method_
        """
        for group in self.supported_groups:
            try:
                self[group].add_method(parsed_method)
            except (KeyError, NotHandledInThisGroupError):
                continue
            #
            # DuplicateNameError and NoSpecialMethodError are re-raised
            # implicitly by not cathing there errors
            break
        else:
            raise UnsupportedMethodError
        #

    def as_markdown(self) -> Iterator[mde.ListItem]:
        r"""Returns an iterator over MarkDown list items"""
        for special_methods_group in self.__groups.values():
            for capability in special_methods_group.implementations():
                yield mde.ListItem(
                    mde.Paragraph(str(capability.signature)),
                    mde.BlockQuote(mds.declare_as_safe(capability.docstring)),
                )
            #
        #


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
