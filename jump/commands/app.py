#!/usr/bin/env python
# encoding: utf-8
"""
app.py

Created by Olli Wang (olliwang@ollix.com) on 2009-10-27.
Copyright (c) 2009 Ollix. All rights reserved.

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

from mako.template import Template

import jump
from jump.commands.main import JumpCommand


class JumpAppCommand(JumpCommand):
    """Jump jar command.

    Make a Mac app bundle.
    """
    usage = "make a Mac app bundle"
    parser = jump.commands.OptionParser()
    required_options = ['main_entry_point']

    def create_build_xml(self, options):
        """Creates the `build.xml` file for ant in `build/temp`."""
        # Template variables
        template_vars = {"jarbundler_filename": jump.jarbundler_filename,
                         "lib_dir_exists": os.path.isdir(self.lib_dir),
                         "base_dir": self.base_dir,
                         "lib_dir": self.lib_dir,
                         "build_lib_dir": self.build_lib_dir,
                         "build_class_dir": self.build_class_dir,
                         "build_temp_dir": self.build_temp_dir,
                         "build_resc_dir": self.build_resc_dir}
        options.update(template_vars)
        JumpCommand.create_build_xml(self, jump.app_build_xml_template,
                                     options)

    def command(self, args, options):
        """Executes the command."""
        self.setup_main_entry_point(options)
        self.copy_jython_jars(options)
        self.copy_python_libs(options, self.build_class_dir)
        self.setup_dist_environments(options)
        self.create_build_xml(options)
        os.system('ant -buildfile %s' % self.build_xml_filename)
