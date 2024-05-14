# -*- coding: utf-8 -*-

"""

tests.test_reference

Unit test the reference module


Copyright (C) 2024 Rainer Schwarzbach

This file is part of morast.

morast is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

morast is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""

from unittest import TestCase

from morast import reference


PACKAGE_TITLE = "Fancy heading"
PACKAGE_DESCRIPTION = "Package description"


PAGE_WITH_DOCSTRINGS = """# Fancy heading

> Package description

*   [module1](module1.md)

    > module1 docstring

*   [module2.submodule](module2.submodule.md)

    > module2 submodule docstring
    > over 2 lines"""

SIMPLE_PAGE = """# Modules Reference

*   [module1](module1.md)
*   [module2.submodule](module2.submodule.md)"""


class MockModule(reference.MorastModule):
    """Mock object for a MorastModule"""

    # pylint: disable=super-init-not-called
    def __init__(self, name: str, namespace: str = "", docstring: str = "") -> None:
        """Store name and docstring as provided, and set _namespaced_prefix"""
        self.name = name
        self._namespace_prefix = f"{namespace}." if namespace else ""
        self.docstring = docstring


MODULES = [
    MockModule("module1"),
    MockModule("submodule", namespace="module2"),
]

MODULES_WITH_DOCSTRINGS = [
    MockModule("module1", docstring="module1 docstring"),
    MockModule(
        "submodule",
        namespace="module2",
        docstring="module2 submodule docstring\nover 2 lines",
    ),
]


class IndexPage(TestCase):
    """IndexPage class"""

    maxDiff = None

    def test_simple(self) -> None:
        """simplest form"""
        refindex = reference.IndexPage()
        for module in MODULES:
            refindex.add_module(module)
        #
        self.assertEqual(refindex.render(), SIMPLE_PAGE)

    def test_docstring(self) -> None:
        """page with docstrings"""
        refindex = reference.IndexPage(
            headline=PACKAGE_TITLE, docstring=PACKAGE_DESCRIPTION
        )
        for module in MODULES_WITH_DOCSTRINGS:
            refindex.add_module(module)
        #
        self.assertEqual(refindex.render(), PAGE_WITH_DOCSTRINGS)


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
