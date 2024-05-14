# -*- coding: utf-8 -*-

"""

tests.test_core

Unit test the core module


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

from unittest import TestCase

from smdg import elements as mde
from smdg import strings as mds

from morast import core
from morast import overrides

from . import commons as tcom


EXPECTED_MBN_REPR = "<MorastBaseNode instance>"

PAPERCLIP_EMOJI = "\N{PAPERCLIP}"
CONSTRUCTION_SIGN_EMOJI = "\N{CONSTRUCTION SIGN}"

EMPTY = ""
LF = "\n"
EXAMPLE_MOD_NAME = "mod_name"
EXAMPLE_MOD_NAMESPACE = f"example_namespace.{EXAMPLE_MOD_NAME}"
C1 = "const_1"
C2 = "const_2"
C3 = "const_3"
C4 = "_private_const_3"

C1_DOC = f"documentation of {C1}"
C3_DOC = f"documentation of {C3}"

EXAMPLE_MOD_OVERRIDE = f"""# {EXAMPLE_MOD_NAME}

## {C1}

{C1_DOC}

## {C2} – ignore

## {C3} (strip-value)

{C3_DOC}
"""

EXAMPLE_SUPERCONFIG = core.SuperConfig(
    module_overrides=overrides.ModuleOverrides.from_string(
        EXAMPLE_MOD_NAME,
        EXAMPLE_MOD_OVERRIDE,
        EXAMPLE_MOD_NAMESPACE,
    )
)

EXAMPLE_ASSIGNMENT_1 = f"{C1}: str = 'abcd'"
EXAMPLE_ASSIGNMENT_3 = f"{C3}: List[str] = [{EXAMPLE_MOD_NAME}.{C2}]"


SDC_NAME = "DataStorage"
SIMPLE_DATACLASS = f'''
@dataclasses.dataclass
class {SDC_NAME}:
    """class docstring"""

    number: int
    flag: bool = False
    identifier: str = "dummy"
'''

FDC_NAME = "EmojiConfiguration"
FROZEN_DATACLASS = f'''
@dataclasses.dataclass(frozen=True)
class {FDC_NAME}:
    """Configuration of emoji for …"""

    enabled: bool = True
'''

PROP_NAME = "readonly_prop"
PROPERTY = f'''
@property
def {PROP_NAME}(self) -> str:
    """Readonly string property"""
    return self.__hidden_attr
'''


def safe_missing_docstring(class_name: str, attr_name: str) -> mds.SafeString:
    """Return an expected  placeholder docstring for an attribute"""
    return mds.declare_as_safe(
        f"{CONSTRUCTION_SIGN_EMOJI}"
        f" **{class_name}.{attr_name}** documentation _to be added_"
    )


class Functions(TestCase):
    """Module-level functions"""


class MorastDocumentableItem(TestCase):
    """MorastDocumentableItem class"""

    maxDiff = None

    def test_docstring(self) -> None:
        """initialization and docstring of a simple item"""
        item = core.MorastDocumentableItem(
            C1,
            namespace=EXAMPLE_MOD_NAME,
            superconfig=EXAMPLE_SUPERCONFIG,
        )
        item.set_docstring_from_override()
        self.assertEqual(item.docstring, C1_DOC)

    def test_ignored(self) -> None:
        """.is_ignored property and .check_ignored()"""
        for name, ignored in ((C1, False), (C2, True)):
            item = core.MorastDocumentableItem(
                name,
                namespace=EXAMPLE_MOD_NAME,
                superconfig=EXAMPLE_SUPERCONFIG,
            )
            item.set_docstring_from_override()
            with self.subTest(name, ignored=ignored):
                self.assertEqual(item.is_ignored, ignored)
            #
            with self.subTest(f"{name} raises exception"):
                if ignored:
                    self.assertRaisesRegex(
                        core.IgnoredItemError,
                        f"\\A{EXAMPLE_MOD_NAME}: ignored {name!r} as specified"
                        " through override",
                        item.check_ignored,
                    )
                else:
                    self.assertFalse(item.check_ignored())
                #
            #
        #

    def test_check_private(self) -> None:
        """.check_private() method"""
        item = core.MorastDocumentableItem(
            C4,
            namespace=EXAMPLE_MOD_NAME,
            superconfig=EXAMPLE_SUPERCONFIG,
        )
        self.assertRaisesRegex(
            core.IgnoredItemError,
            f"\\A{EXAMPLE_MOD_NAME}: ignored private member {C4!r}",
            item.check_private,
        )

    def test_markdown_elements(self) -> None:
        """.markdown_elements() method"""
        item = core.MorastDocumentableItem(
            C1,
            namespace=EXAMPLE_MOD_NAME,
            superconfig=EXAMPLE_SUPERCONFIG,
        )
        item.set_docstring_from_override()
        self.assertEqual(
            list(item.markdown_elements()),
            [
                mde.Paragraph(f"{EXAMPLE_MOD_NAME}.{C1}"),
                mde.BlockQuote(mds.SafeString(C1_DOC)),
            ],
        )


class MorastAttribute(TestCase):
    """MorastAttribute class"""

    maxDiff = None

    def test_simple_docstring(self) -> None:
        """initialization and docstring of a simple item"""
        element = tcom.first_parsed_body_element(EXAMPLE_ASSIGNMENT_1)
        if not isinstance(element, (ast.AnnAssign, ast.AugAssign, ast.Assign)):
            self.skipTest("wrong type")
            return
        #
        item = core.MorastAttribute(
            element,
            namespace=EXAMPLE_MOD_NAME,
            superconfig=EXAMPLE_SUPERCONFIG,
        )
        self.assertEqual(item.docstring, C1_DOC)

    def test_stripped_value_as_markdown(self) -> None:
        """docstring of a simple item"""
        element = tcom.first_parsed_body_element(EXAMPLE_ASSIGNMENT_3)
        if not isinstance(element, (ast.AnnAssign, ast.AugAssign, ast.Assign)):
            self.skipTest("wrong type")
            return
        #
        item = core.MorastAttribute(
            element,
            namespace=EXAMPLE_MOD_NAME,
            superconfig=EXAMPLE_SUPERCONFIG,
        )
        self.assertEqual(
            list(item.markdown_elements()),
            [
                mde.Paragraph(
                    mde.CompoundInlineElement(
                        mde.InlineElement(
                            f"{EXAMPLE_SUPERCONFIG.emoji.constants_prefix}"
                            f" {EXAMPLE_MOD_NAME}."
                        ),
                        mde.BoldText(mde.InlineElement(C3)),
                        mde.InlineElement(": "),
                        mde.CompoundInlineElement(
                            mde.InlineElement("List"),
                            mde.InlineElement("["),
                            mde.InlineElement("str"),
                            mde.InlineElement("]"),
                        ),
                    ),
                ),
                mde.BlockQuote(mds.SafeString(C3_DOC)),
            ],
        )


class MorastProperty(TestCase):
    """MorastProperty class"""

    maxDiff = None

    def test_attributes(self) -> None:
        """attributes of the element"""
        element = tcom.first_parsed_body_element(PROPERTY)
        if not isinstance(element, ast.FunctionDef):
            self.skipTest("wrong type")
            return
        #
        item = core.MorastProperty(
            element,
            namespace="DummyClass",
            superconfig=EXAMPLE_SUPERCONFIG,
        )
        for attr_name, expexted_value in (
            ("name", PROP_NAME),
            ("docstring", "Readonly string property"),
            ("type_annotation", "str"),
        ):
            with self.subTest(attr_name=attr_name, expexted_value=expexted_value):
                self.assertEqual(getattr(item, attr_name), expexted_value)
            #
        #


class MorastClassDef(TestCase):
    """MorastClassDef class"""

    maxDiff = None

    def test_simple_dataclass(self) -> None:
        """test initialization of a simple data class"""
        ast_class_def = tcom.first_parsed_body_element(SIMPLE_DATACLASS)
        if isinstance(ast_class_def, ast.ClassDef):
            class_def = core.MorastClassDef(ast_class_def)
        else:
            raise ValueError("Excpected a class definition")
        #
        with self.subTest("name"):
            self.assertEqual(class_def.name, SDC_NAME)
        #
        with self.subTest("is a dataclass"):
            self.assertTrue(class_def.is_a_dataclass)
        #
        for item in ("number", "flag", "identifier"):
            with self.subTest("instance_attribute", item=item):
                current_attr = class_def.attribute_lists[core.SCOPE_INSTANCE][item]
                if isinstance(current_attr, core.MorastAttribute):
                    self.assertEqual(current_attr.name, item)
                    self.assertEqual(current_attr.scope, core.SCOPE_INSTANCE)
                else:
                    raise ValueError("expected an Attribute")
                #
            #
        #
        with self.subTest("MarkDown elements"):
            self.assertEqual(
                list(class_def.markdown_elements()),
                [
                    mde.HorizontalRule(20),
                    mde.Header(3, "Dataclass DataStorage()"),
                    mde.BlockQuote(mds.sanitize("class docstring")),
                    # mde.HorizontalRule(20),
                    mde.Header(4, "instance attributes"),
                    mde.UnorderedList(
                        mde.ListItem(
                            mde.Paragraph(
                                mde.CompoundInlineElement(
                                    mde.InlineElement(f"{PAPERCLIP_EMOJI} ."),
                                    mde.BoldText(mde.InlineElement("number")),
                                    mde.InlineElement(": "),
                                    mde.InlineElement("int"),
                                ),
                            ),
                            mde.BlockQuote(safe_missing_docstring(SDC_NAME, "number")),
                        ),
                        mde.ListItem(
                            mde.Paragraph(
                                mde.CompoundInlineElement(
                                    mde.InlineElement(f"{PAPERCLIP_EMOJI} ."),
                                    mde.BoldText(mde.InlineElement("flag")),
                                    mde.InlineElement(": "),
                                    mde.InlineElement("bool"),
                                    mde.InlineElement(" = "),
                                    mde.CodeSpan("False"),
                                ),
                            ),
                            mde.BlockQuote(safe_missing_docstring(SDC_NAME, "flag")),
                        ),
                        mde.ListItem(
                            mde.Paragraph(
                                mde.CompoundInlineElement(
                                    mde.InlineElement(f"{PAPERCLIP_EMOJI} ."),
                                    mde.BoldText(mde.InlineElement("identifier")),
                                    mde.InlineElement(": "),
                                    mde.InlineElement("str"),
                                    mde.InlineElement(" = "),
                                    mde.CodeSpan("'dummy'"),
                                ),
                            ),
                            mde.BlockQuote(
                                safe_missing_docstring(SDC_NAME, "identifier")
                            ),
                        ),
                    ),
                ],
            )

    def test_frozen_dataclass(self) -> None:
        """test initialization of a frozen data class"""
        ast_class_def = tcom.first_parsed_body_element(FROZEN_DATACLASS)
        if isinstance(ast_class_def, ast.ClassDef):
            class_def = core.MorastClassDef(ast_class_def)
        else:
            raise ValueError("Excpected a class definition")
        #
        with self.subTest("name"):
            self.assertEqual(class_def.name, FDC_NAME)
        #
        with self.subTest("is a dataclass"):
            self.assertTrue(class_def.is_a_dataclass)
        #
        item = "enabled"
        with self.subTest("instance_attribute", item=item):
            current_attr = class_def.attribute_lists[core.SCOPE_INSTANCE][item]
            if isinstance(current_attr, core.MorastAttribute):
                self.assertEqual(current_attr.name, item)
                self.assertEqual(current_attr.scope, core.SCOPE_INSTANCE)
            else:
                raise ValueError("expected an Attribute")
            #
        #
        with self.subTest("MarkDown elements"):
            self.assertEqual(
                list(class_def.markdown_elements()),
                [
                    mde.HorizontalRule(20),
                    mde.Header(3, "Frozen dataclass EmojiConfiguration()"),
                    mde.BlockQuote(mds.sanitize("Configuration of emoji for …")),
                    mde.Header(4, "instance attributes"),
                    mde.UnorderedList(
                        mde.ListItem(
                            mde.Paragraph(
                                mde.CompoundInlineElement(
                                    mde.InlineElement(f"{PAPERCLIP_EMOJI} ."),
                                    mde.BoldText(mde.InlineElement("enabled")),
                                    mde.InlineElement(": "),
                                    mde.InlineElement("bool"),
                                    mde.InlineElement(" = "),
                                    mde.CodeSpan("True"),
                                ),
                            ),
                            mde.BlockQuote(safe_missing_docstring(FDC_NAME, "enabled")),
                        ),
                    ),
                ],
            )


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
