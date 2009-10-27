#!/usr/bin/env python
# encoding: utf-8
"""
jar.py

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

import jump
from jump.commands.main import JumpCommand


class JumpJarCommand(JumpCommand):
    """Jump jar command.

    Make a standalone JAR file.
    """
    usage = "make a standalone JAR file"
    parser = jump.commands.OptionParser()
    required_options = ['main_entry_point']

    def copy_default_resources(self):
        """Copies default resources to `build/resource` directory."""
        # Generate default license file
        JumpCommand.create_template_file(self, jump.license_template,
                                         self.license_filename)

    def create_template_file(self, options):
        """Creates the `build.xml` file for ant in `build/temp`."""
        # Template variables
        template_vars = {"onejar_jar_filename": jump.onejar_jar_filename,
                         "lib_dir_exists": os.path.isdir(self.lib_dir),
                         "base_dir": self.base_dir,
                         "lib_dir": self.lib_dir,
                         "build_lib_dir": self.build_lib_dir,
                         "build_class_dir": self.build_class_dir,
                         "build_temp_dir": self.build_temp_dir,
                         "build_resc_dir": self.build_resc_dir}
        options.update(template_vars)
        JumpCommand.create_template_file(self, jump.jar_build_xml_template,
                                         self.build_xml_filename, options)

    def command(self, args, options):
        """Executes the command."""
        self.setup_main_entry_point(options)
        self.copy_jython_jars(options)
        self.copy_python_libs(options, self.build_class_dir)
        self.copy_default_resources()
        self.setup_dist_environments(options)
        self.create_template_file(options)
        os.system('ant -buildfile %s' % self.build_xml_filename)
