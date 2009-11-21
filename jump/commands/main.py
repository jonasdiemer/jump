#!/usr/bin/env python
# encoding: utf-8
"""
jump.py

Created by Olli Wang (olliwang@ollix.com) on 2009-10-26.
Copyright (c) 2009 Ollix. All rights reserved.

This file is part of Jump.

Jump is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or any later version.

Jump is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with Jump.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
import shutil
import tempfile

import oparse
from mako.template import Template

import jump


class JumpCommand(oparse.Command):
    """The basic Jump command.

    This class implement the basic Jump command. All Jump's subcommand classes
    should inherit from this class.

    Attributes:
        subcmd_entry_point: The entry point name for Jump's subcommands.
        usage: Modifies the default usage by adding a command argument.
        version: Indicates the current Jump version.
        parser: Instantiates OptionParse class to add some parser options.
    """
    usage = '%prog command [options] arg1 arg2 ...'
    description = """Jump is a build tool for distributing Jython applications.
You can find more about Jump at http://gitorious.org/jump."""
    version = '%prog ' + jump.VERSION
    subcommand_entry_point = 'jump.commands'

    # Basic configuration
    base_dir = os.getcwd()
    build_dir = 'build'
    config_filename = os.path.join(base_dir, 'config.jp')
    manifest_filename = os.path.join(base_dir, 'manifest.jp')
    build_xml_filename = os.path.join(tempfile.gettempdir(), 'build.xml')
    build_xml_template = os.path.join(jump.temp_dir, 'build.xml')
    default_dist_name = os.path.basename(base_dir)

    # Command options
    parser = oparse.OptionParser()
    parser.add_option('-v', '--verbose', action="store_true",
                      default=False, help="run in verbose mode")
    parser.add_option('-n', '--dist_name', action="store",
                      default=default_dist_name,
                      help="name of the distribution file")
    parser.add_option('-p', '--include_packages', action="store",
                      default="", help="include full Python packages")
    parser.add_option('-d', '--dist_dir', action="store",
                      default=os.path.join(base_dir, 'dist'),
                      help="directory to put the distribution")
    parser.add_option('-m', '--main_entry_point', action="store",
                      default=None, help="main entry point, either Java or " \
                                         "Python")
    parser.add_option('--java_only', action="store_true",
                      default=False, help="Ignore any Jython code and " \
                                          "JAR file")
    parser.add_option('--jump_jython_factory', action="store_true",
                      default=False, help="Use Jump's Jython factory.")

    def initialize(self, options):
        """Setup distribuiton enviroments"""
        self.options = options
        options.base_dir = self.base_dir
        options.build_dir = self.build_dir
        options.jump_dir = jump.jump_dir
        options.jump_version = "Jump %s" % jump.VERSION

        # Convert boolean values
        self.convert_boolean_values(['java_only', 'jump_jython_factory'])

        # Extracts patterns in manifest file
        self.extract_manifest_patterns(options)

        # Set Jython's root directory
        os.environ['JYTHON_HOME'] = options.jython_home = sys.prefix

    def convert_boolean_values(self, option_names):
        """Convert boolean values to true or false respectively."""
        for option_name in option_names:
            if self.options[option_name]:
                self.options[option_name] = "true"
            else:
                self.options[option_name] = "false"

    def extract_manifest_patterns(self, options):
        """Extracts patterns in manifest file."""
        if not os.path.isfile(self.manifest_filename):
            options.manifest_patterns = []
            return

        manifest_patterns = []
        for line in open(self.manifest_filename, 'r'):
            # Ignore from `#` to the end of line
            line = line.split('#', 1)[0].strip()
            if not line:
                continue
            # Retrieve patterns
            try:
                command, pattern = line.split(' ', 1)
            except ValueError:
                error_message = "Syntax error in manifest file: %r" % line
                raise jump.commands.CommandError(error_message)
            # Raise error if command is invalid
            if command not in ['include', 'exclude']:
                error_message = "Command not supported in manifest file: " \
                                "%r" % command
                raise jump.commands.CommandError(error_message)
            manifest_patterns.append((command, pattern))
        # Save patterns to options
        options.manifest_patterns = manifest_patterns

    def create_template_file(self, template, output):
        """Creates template files for ant in `build/temp`."""
        output_dir = os.path.dirname(output)
        tempalte = Template(filename=template)
        output_file = open(output, 'w')
        output_file.write(tempalte.render(**self.options))
        output_file.close()

    def command(self, args, options):
        """Returns help message."""
        jump = JumpCommand()
        jump('-h')

    def clean(self):
        os.remove(self.build_xml_filename)
        shutil.rmtree(os.path.join(self.base_dir, 'build'))

def jump_command():
    """Runs the Jump command."""
    jump = JumpCommand()
    jump()
