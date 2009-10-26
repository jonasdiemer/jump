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
import shutil

import jump


class JumpCommand(jump.commands.Command):
    """The basic Jump command.

    This class implement the basic Jump command. All Jump's subcommand classes
    should inherit from this class.

    Attributes:
        subcmd_entry_point: The entry point name for Jump's subcommands.
        usage: Modifies the default usage by adding a command argument.
        version: Indicates the current Jump version.
        parser: Instantiates OptionParse class to add some parser options.
    """
    subcmd_entry_point = 'jump.commands'
    usage = '%prog command [options] arg1 arg2 ...'
    version = '%prog ' + jump.VERSION
    config_filename = 'config.jp'
    required_options = ['main_entry_point']

    parser = jump.commands.OptionParser()
    parser.add_option('-v', '--verbose', action="store_true",
                      default=False, help="run in verbose mode")
    parser.add_option('-n', '--dist_name', action="store",
                      default=None, help="name of the distribution file")
    parser.add_option('-p', '--include_packages', action="store",
                      default=None, help="include full Python packages")

    def copy_python_libs(self, options, dest_dir):
        """Copies required Python modules to `build/class` directory."""
        if options.include_packages:
            full_packages = options.include_packages.split(',')
        else:
            full_packages = None

        # Find all required Python modules or packages and copy them
        # to the specified destnation directory
        lib_tracer = jump.libtracer.LibTracer(self.base_dir, quiet=False,
                                              full_packages=full_packages)
        lib_locations = lib_tracer.get_lib_locations()
        for sys_path, relative_path in lib_locations:
            src_path = os.path.join(sys_path, relative_path)
            dest_path = os.path.join(dest_dir, relative_path)
            dest_dirname = os.path.dirname(dest_path)
            if not os.path.isdir(dest_dirname):
                os.makedirs(dest_dirname)
            shutil.copy2(src_path, dest_path)

    def command(self, args, options):
        """Returns help message."""
        JumpCommand().run('-h')

def jump_command():
    """Runs the Jump command."""
    JumpCommand().run()
