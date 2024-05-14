# -*- coding: utf-8 -*-

"""

morast.commandline

Command line functionality


Copyright (C) 2024 Rainer Schwarzbach

This file is part of morast.

morast is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

morast is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""

import argparse
import ast
import fnmatch
import logging
import pathlib

from typing import Dict, Iterator, Tuple

from morast import __version__
from morast import commons
from morast import core
from morast import configuration
from morast import overrides
from morast import reference


#
# Constants
#


SUBCOMMAND_AUTODETECT = "auto"
SUBCOMMAND_EXTRACT = "extract"
SUBCOMMAND_INIT = "init"
SUBCOMMAND_SHOW_CONFIG = "config"
SUBCOMMAND_SINGLE_MODULE = "module"

SUFFIX_EXTRACTED = "+extracted"

RETURNCODE_OK = 0
RETURNCODE_ERROR = 1


#
# classes
#


class Program:
    """Command line program"""

    name: str = "morast"
    description: str = "Create reference documentation from sources using AST"

    def __init__(self, *args: str) -> None:
        r"""Parses command line arguments and initializes the logger

        Initialization arguments:

        *   _\*args_: the command line arguments to parse, provided
            as individual strings
        """
        logging.basicConfig(
            format="%(levelname)-8s | %(message)s",
            level=logging.WARNING,
        )
        self.config = configuration.GlobalOptions.from_file()
        self.__arguments = self._parse_args(*args)
        logging.getLogger().setLevel(self.arguments.loglevel)

    @property
    def arguments(self) -> argparse.Namespace:
        """The parsed command line arguments"""
        return self.__arguments

    def _parse_args(self, *args: str) -> argparse.Namespace:
        r"""Internal method to parse the command line arguments
        provided through _\*args_ using argparse,
        returning the parsed arguments namespace.
        """
        main_parser = argparse.ArgumentParser(
            prog=self.name,
            description=self.description,
        )
        main_parser.set_defaults(loglevel=logging.WARNING)
        main_parser.add_argument(
            "--version",
            action="version",
            version=__version__,
            help="print version and exit",
        )
        logging_group = main_parser.add_argument_group(
            "Logging options", "control log level (default is WARNING)"
        )
        verbosity_mutex = logging_group.add_mutually_exclusive_group()
        verbosity_mutex.add_argument(
            "-d",
            "--debug",
            action="store_const",
            const=logging.DEBUG,
            dest="loglevel",
            help="output all messages (log level DEBUG)",
        )
        verbosity_mutex.add_argument(
            "-v",
            "--verbose",
            action="store_const",
            const=logging.INFO,
            dest="loglevel",
            help="be more verbose (log level INFO)",
        )
        verbosity_mutex.add_argument(
            "-q",
            "--quiet",
            action="store_const",
            const=logging.ERROR,
            dest="loglevel",
            help="be more quiet (log level ERROR)",
        )
        subparsers = main_parser.add_subparsers(
            # help="subcommands",
            dest="subcommand",
        )
        src_path = self.config.source_path
        dest_path = self.config.destination_path
        parser_single = subparsers.add_parser(
            SUBCOMMAND_AUTODETECT,
            description=f"Automatically detect modules in {src_path}"
            " and write their documentation to MarkDown files in"
            f" {dest_path}",
            help="automatically detect and document all modules",
        )
        subparsers.add_parser(
            SUBCOMMAND_EXTRACT,
            description="Extract a template override from each Python module"
            " found in the configured modules path",
            help="extract override templates from modules",
        )
        subparsers.add_parser(
            SUBCOMMAND_INIT,
            description=f"Initialize the {commons.BRAND} project"
            f" by creating a {commons.MORAST_CONFIG_DIR} path"
            " in the current directory",
            help=f"initialize the {commons.BRAND} project",
        )
        subparsers.add_parser(
            SUBCOMMAND_SHOW_CONFIG,
            description="Show configuration on standard output",
            help="show the configuration",
        )
        parser_single = subparsers.add_parser(
            SUBCOMMAND_SINGLE_MODULE,
            description="Generate documentation for a single module"
            " and write it to standard output",
            help="document a single module",
        )
        parser_single.add_argument(
            "path",
            type=pathlib.Path,
            help="the file to parse",
        )
        return main_parser.parse_args(args=args or None)

    def execute(self) -> int:
        """Execute the program
        :returns: the returncode for the script
        """
        if self.arguments.subcommand == SUBCOMMAND_AUTODETECT:
            return self.autodetect()
        #
        if self.arguments.subcommand == SUBCOMMAND_EXTRACT:
            return self.extract_override_templates()
        #
        if self.arguments.subcommand == SUBCOMMAND_INIT:
            return self.initialize()
        #
        if self.arguments.subcommand == SUBCOMMAND_SHOW_CONFIG:
            return self.show_config()
        #
        if self.arguments.subcommand == SUBCOMMAND_SINGLE_MODULE:
            return self.single_module()
        #
        return RETURNCODE_OK

    def _get_overrides(self) -> Dict[str, overrides.ModuleOverrides]:
        """Return all found module overrides"""
        mod_overrides: Dict[str, overrides.ModuleOverrides] = {}
        overrides_base_path = self.config.overrides_basepath.resolve()
        for md_override_path in overrides_base_path.glob("**/*.md"):
            if md_override_path.name.endswith(f"{SUFFIX_EXTRACTED}.md"):
                continue
            #
            logging.info("####### Reading overrides from %s", md_override_path)
            try:
                cur_override = overrides.ModuleOverrides.from_file(
                    self.config, md_override_path
                )
            except ValueError as error:
                logging.warning(
                    "ignored module overrides from %s due to following error:",
                    md_override_path,
                )
                logging.warning(str(error))
                continue
            #
            mod_overrides[cur_override.external_namespace] = cur_override
            logging.info(
                "===== Overrides external namespace: %s =====",
                cur_override.external_namespace,
            )
            for name, section in cur_override.items():
                logging.debug(
                    "____ %s ____ (ignored: %r, value stripped: %r)",
                    name,
                    section.is_ignored,
                    section.value_is_stripped,
                )
                for line in section.docstring.splitlines():
                    logging.debug(line)
                #
                additions = section.additions
                if additions:
                    logging.debug("--- Additions ---")
                    for line in additions.splitlines():
                        logging.debug(line)
                    #
                #
            #
        #
        return mod_overrides

    def _iter_found_modules(self) -> Iterator[Tuple[str, reference.BasePage]]:
        """Detect and document all modules in the package"""
        mod_overrides = self._get_overrides()
        source_base_path = self.config.source_path.resolve()
        refindex_name = "index"
        try:
            current_override = mod_overrides[refindex_name]
        except KeyError:
            current_override = overrides.ModuleOverrides(commons.EMPTY)
        #
        refindex = reference.IndexPage(
            superconfig=core.SuperConfig(
                module_overrides=current_override,
                options=self.config,
            ),
            headline="Modules reference",
        )
        for source_path in source_base_path.glob("**/*.py"):
            relpath = source_path.relative_to(source_base_path)
            mod_name = relpath.stem
            ext_namespace_ex = commons.DOT.join(relpath.parent.parts)
            ext_namespace_in = f"{ext_namespace_ex}.{mod_name}"
            module_is_excluded = False
            for excluded_modules_pattern in self.config.excluded_modules:
                if fnmatch.fnmatch(ext_namespace_in, excluded_modules_pattern):
                    module_is_excluded = True
                    break
                #
            #
            if module_is_excluded:
                continue
            #
            logging.info("####### Handling module %s …", ext_namespace_in)
            try:
                current_override = mod_overrides[ext_namespace_in]
            except KeyError:
                current_override = overrides.ModuleOverrides(commons.EMPTY)
            else:
                logging.info("… found matching overrides")
            #
            superconfig = core.SuperConfig(
                module_overrides=current_override,
                options=self.config,
            )
            morast_mod = reference.MorastModule(
                ast.parse(
                    source_path.read_text(commons.UTF8),
                    filename=str(relpath),
                ),
                name=mod_name,
                namespace=ext_namespace_ex,
                superconfig=superconfig,
            )
            refindex.add_module(morast_mod)
            yield ext_namespace_in, morast_mod
        #
        yield refindex_name, refindex

    def extract_override_templates(self) -> int:
        """Detect all modules in the package,
        extract override templates and write them to the appropriate files.

        For each override file that already exists, append `+extracted`
        to the new file name so the differences can be easily examined
        using eg. a graphical diff tool.
        """
        if not self.config.overrides_basepath.is_dir():
            logging.error(
                "The configured overrides path %s does not exist (yet).",
                self.config.overrides_basepath,
            )
            return RETURNCODE_ERROR
        #
        for ext_namespace_in, morast_mod in self._iter_found_modules():
            target_filename = f"{ext_namespace_in}.md"
            result = morast_mod.get_extracted_overrides()
            target_path = self.config.overrides_basepath / target_filename
            if target_path.exists():
                old_overrides = target_path.read_text(encoding=commons.UTF8)
                if result.rstrip() == old_overrides.rstrip():
                    continue
                #
                target_filename = f"{ext_namespace_in}{SUFFIX_EXTRACTED}.md"
                target_path = self.config.overrides_basepath / target_filename
            #
            target_path.write_text(result, encoding=commons.UTF8)
        #
        return RETURNCODE_OK

    def autodetect(self) -> int:
        """Detect and document all modules in the package"""
        if not self.config.destination_path.is_dir():
            logging.error(
                "The configured destination path %s does not exist (yet).",
                self.config.destination_path,
            )
            return RETURNCODE_ERROR
        #
        for ext_namespace_in, morast_mod in self._iter_found_modules():
            result = morast_mod.render()
            target_path = self.config.destination_path / f"{ext_namespace_in}.md"
            target_path.write_text(result, encoding=commons.UTF8)
        #
        return RETURNCODE_OK

    def initialize(self) -> int:
        """Initialize the project"""
        overrides_basepath = self.config.overrides_basepath.resolve()
        if overrides_basepath.exists():
            logging.warning(
                "Path %s already exists, nothing done",
                self.config.overrides_basepath,
            )
            return RETURNCODE_ERROR
        #
        overrides_basepath.mkdir(parents=True)
        configuration.DEFAULT_CONFIG_FILE.write_text(
            self.config.dump(include_source_comment=False),
            encoding=commons.UTF8,
        )
        return RETURNCODE_OK

    def show_config(self) -> int:
        """Show the configuration on stdout"""
        print(self.config.dump())
        return RETURNCODE_OK

    def single_module(self) -> int:
        """Document a single module on stdout"""
        print(
            reference.MorastModule.from_file(
                self.arguments.path,
                superconfig=core.SuperConfig(options=self.config),
            ).render()
        )
        return RETURNCODE_OK


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
