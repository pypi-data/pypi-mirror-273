# -*- coding: utf-8 -*-

"""

tests.test_capabilities

Unit test the capabilities module


Copyright (C) 2024 Rainer Schwarzbach

This file is part of morast.

morast is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

morast is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""

from typing import List, Tuple, Type
from unittest import TestCase

from morast import capabilities

from . import commons as tcom


EMPTY = ""

NAME_DUMMY = "dummy"
DOCSTRING_DUMMY = "Dummy special_group"

NAME_NONSPECIAL = "nonspecial"


#
# Helper functions
#


def get_method(
    name: str,
    docstring: str,
    args: str = "self",
    returns: str = "",
    body: str = "",
):
    """Return a method with name and docstring"""
    if returns:
        returns = f" -> {returns}"
    #
    if not body:
        body = 'return "dummy"'
    #
    if "\n" in body:
        _body_lines: List[str] = []
        for _line in body.splitlines(keepends=True):
            _body_lines.append(f"    {_line}")
        #
        body = "".join(_body_lines)
    #
    return f'def {name}({args}){returns}:\n    """{docstring}"""\n{body}\n'


def get_special_method(
    name: str,
    docstring: str,
    args: str = "self",
    returns: str = EMPTY,
    body: str = EMPTY,
):
    """Return a special method with name and docstring"""
    return get_method(f"__{name}__", docstring, args=args, returns=returns, body=body)


METHOD_DUMMY = get_special_method(NAME_DUMMY, DOCSTRING_DUMMY)
METHOD_NONSPECIAL = get_method(NAME_NONSPECIAL, DOCSTRING_DUMMY)


#
# Classes
#


class GroupDummy(capabilities.SpecialMethodsGroupBase):
    """Special Methods group dummy"""

    handled_methods: Tuple[str, ...] = ("dummy",)


class SpecialMethodsGroup(TestCase):
    """Special methods group base class and GroupDummy class"""

    maxDiff = None

    def test_base_nonspecial(self):
        """non-special method"""
        basic = capabilities.SpecialMethodsGroupBase("base_instance")
        self.assertRaises(
            capabilities.NoSpecialMethodError,
            basic.add_method,
            tcom.first_parsed_body_element(METHOD_NONSPECIAL),
        )

    def test_base_dummy(self):
        """__dummy__ method in base class"""
        basic = capabilities.SpecialMethodsGroupBase("base_instance")
        self.assertRaises(
            capabilities.NotHandledInThisGroupError,
            basic.add_method,
            tcom.first_parsed_body_element(METHOD_DUMMY),
        )

    def test_dummy(self):
        """__dummy__ method in a subclass habnling this method"""
        basic = GroupDummy("dummy_instance")
        dummy_method_ast = tcom.first_parsed_body_element(METHOD_DUMMY)
        basic.add_method(dummy_method_ast)
        with self.subTest("expected capability"):
            self.assertIn(NAME_DUMMY, basic)
        #
        capability = basic.get_capability(NAME_DUMMY)
        with self.subTest("capability docstring"):
            self.assertEqual(capability.docstring, DOCSTRING_DUMMY)
        #
        with self.subTest("capability signature"):
            self.assertEqual(
                str(capability.signature),
                f"<capability {NAME_DUMMY!r} of dummy_instance>",
            )
        #
        with self.subTest("duplicate method name"):
            self.assertRaises(
                capabilities.DuplicateNameError,
                basic.add_method,
                dummy_method_ast,
            )
        #

    def test_instance_var(self):
        """instance_var property"""
        basic = capabilities.SpecialMethodsGroupBase("base_instance")
        self.assertEqual(basic.instance_var, "base_instance")


class SpecialMethodsGroupTestCase(TestCase):
    """Base class for testing a special methods group"""

    maxDiff = None
    instance_name = "smg_instance"
    subject_class: Type = capabilities.SpecialMethodsGroupBase

    # pylint: disable=too-many-arguments
    def capability_generic_test(
        self,
        name: str,
        docstring: str,
        args: str = "self",
        body: str = EMPTY,
        returns: str = EMPTY,
        expected_signature: str = EMPTY,
    ) -> None:
        """Generic rich compariosons test"""
        group = self.subject_class(self.instance_name)
        method_ast = tcom.first_parsed_body_element(
            get_special_method(name, docstring, args=args, body=body, returns=returns)
        )
        group.add_method(method_ast)
        with self.subTest("expected capability"):
            self.assertIn(name, group)
        #
        with self.subTest("docstring"):
            self.assertIn(group[name].docstring, docstring)
        #
        signature = group.get_signature(name)
        with self.subTest("signature"):
            self.assertEqual(
                str(signature),
                expected_signature,
            )
        #


class BasicCustomizationGroup(SpecialMethodsGroupTestCase):
    """Basic customization"""

    maxDiff = None
    instance_name = "bc_instance"
    subject_class: Type = capabilities.BasicCustomizationGroup
    other_name = "other"

    # pylint: disable=too-many-arguments
    def capability_as_comparison_test(
        self,
        name: str,
        docstring: str,
        other_name: str = "other",
        body: str = EMPTY,
        expected_signature: str = EMPTY,
    ) -> None:
        """Generic rich compariosons test"""
        return self.capability_generic_test(
            name,
            docstring,
            args=f"self, {other_name}",
            body=body,
            expected_signature=expected_signature,
        )

    def test_repr(self):
        """**repr** capability"""
        self.capability_generic_test(
            "repr",
            "Constructor representation",
            returns="str",
            expected_signature=f"repr({self.instance_name}) → str",
        )

    def test_str(self):
        """**str** capability"""
        self.capability_generic_test(
            "str",
            "Instance string value",
            returns="str",
            expected_signature=f"str({self.instance_name}) → str",
        )

    def test_hash(self):
        """**hash** capability"""
        self.capability_generic_test(
            "hash",
            "Hash value",
            body="return 13",
            returns="int",
            expected_signature=f"hash({self.instance_name}) → int",
        )

    def test_bool(self):
        """**bool** capability"""
        self.capability_generic_test(
            "bool",
            "Boolean evaluation",
            body="return True",
            returns="bool",
            expected_signature=f"bool({self.instance_name}) → bool",
        )

    def test_len(self):
        """(unhandled) **len** capability"""
        self.assertRaises(
            capabilities.NotHandledInThisGroupError,
            self.capability_generic_test,
            "len",
            "Length",
            body="return 7",
            returns="int",
        )

    def test_eq(self):
        """Rich comparison: eq"""
        self.capability_as_comparison_test(
            "eq",
            "rich comparison: equals",
            expected_signature=f"{self.instance_name} == {self.other_name}",
        )

    def test_ne(self):
        """Rich comparison: ne"""
        self.capability_as_comparison_test(
            "ne",
            "rich comparison: unequal",
            expected_signature=f"{self.instance_name} != {self.other_name}",
        )

    def test_lt(self):
        """Rich comparison: lt"""
        self.capability_as_comparison_test(
            "lt",
            "rich comparison: less than",
            expected_signature=f"{self.instance_name} < {self.other_name}",
        )

    def test_gt(self):
        """Rich comparison: gt"""
        self.capability_as_comparison_test(
            "gt",
            "rich comparison: greater than",
            expected_signature=f"{self.instance_name} > {self.other_name}",
        )

    def test_le(self):
        """Rich comparison: le"""
        self.capability_as_comparison_test(
            "le",
            "rich comparison: less or equal",
            expected_signature=f"{self.instance_name} <= {self.other_name}",
        )

    def test_ge(self):
        """Rich comparison: ge"""
        self.capability_as_comparison_test(
            "ge",
            "rich comparison: greater or equal",
            expected_signature=f"{self.instance_name} >= {self.other_name}",
        )


class ContainerTypesEmulationGroup(SpecialMethodsGroupTestCase):
    """Container types emulation"""

    maxDiff = None
    instance_name = "cte_instance"
    subject_class: Type = capabilities.ContainerTypesEmulationGroup

    def test_len(self):
        """**len** capability"""
        self.capability_generic_test(
            "len",
            "Number of contained items",
            body="return len(self.__data)",
            returns="int",
            expected_signature=f"len({self.instance_name}) → int",
        )

    def test_iter(self):
        """**iter** capability"""
        self.capability_generic_test(
            "iter",
            "Iterator over contained items",
            body="\n".join(
                (
                    "for item in self.__data:",
                    "    yield item",
                )
            ),
            returns="Iterator[int]",
            expected_signature=f"iter({self.instance_name}) → Iterator[int]",
        )

    def test_reversed(self):
        """**reversed** capability"""
        self.capability_generic_test(
            "reversed",
            "Reverse iterator over contained items",
            body="\n".join(
                (
                    "# example values",
                    "for item in self.__data[::-1]:",
                    "    yield item",
                )
            ),
            returns="Iterator[int]",
            expected_signature=(f"reversed({self.instance_name}) → Iterator[int]"),
        )

    def test_getitem(self):
        """**getitem** capability"""
        self.capability_generic_test(
            "getitem",
            "item access by name",
            args="self, key",
            body="return self.__data[key]",
            returns="int",
            expected_signature=f"{self.instance_name}[key] → int",
        )

    def test_setitem(self):
        """**setitem** capability"""
        self.capability_generic_test(
            "setitem",
            "item setter method",
            args="self, key, value",
            body="self.__data[key] = value",
            expected_signature=f"{self.instance_name}[key] = value",
        )

    def test_delitem(self):
        """**delitem** capability"""
        self.capability_generic_test(
            "delitem",
            "item deletion method",
            args="self, key",
            body="del self.__data[key]",
            expected_signature=f"del {self.instance_name}[key]",
        )

    def test_contains(self):
        """**contains** capability"""
        self.capability_generic_test(
            "contains",
            "membership testing",
            args="self, key",
            body="\n".join(
                (
                    "# example value",
                    "if key in self.__data:",
                    "    return True",
                )
            ),
            returns="bool",
            expected_signature=f"key in {self.instance_name} → bool",
        )


class CallableObjectsEmulationGroup(SpecialMethodsGroupTestCase):
    """Callable objects emulation"""

    maxDiff = None
    instance_name = "cte_instance"
    subject_class: Type = capabilities.CallableObjectsEmulationGroup

    def test_call(self):
        """**call** capability"""
        for args, expected_args_display in (
            ("a, b, c, d", "a, b, c, d"),
            ("a=1, b: int = 2, *c, d=4", "a=1, b: int = 2, *c, d=4"),
            ("/, a, b, c=3, **d", "a, b, c=3, **d"),
            ("a=8, b: int = 6, /, d=5", "a=8, b: int = 6, /, d=5"),
            ("a, b, /, c", "a, b, /, c"),
            ("a, b, /", "a, b, /"),
            ("a, b=9, *, c=7", "a, b=9, *, c=7"),
        ):
            with self.subTest(
                args=args,
                expected_args_display=expected_args_display,
            ):
                self.capability_generic_test(
                    "call",
                    "call docstring: calcluate something",
                    args=f"self, {args}",
                    body="...",
                    returns="int",
                    expected_signature=(
                        f"{self.instance_name}({expected_args_display}) → int"
                    ),
                )
            #
        #


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
