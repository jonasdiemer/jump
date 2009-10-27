#!/usr/bin/env python
# encoding: utf-8
"""
jarlib.py

Created by Olli Wang (olliwang@ollix.com) on 2009-10-27.
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

from mako.template import Template

import jump


class JumpJarLibCommand(jump.commands.main.JumpCommand):
    """Jump jarlib command.

    Make a JAR library file.
    """
    usage = "make a JAR library file"
    parser = jump.commands.OptionParser()

    def create_build_xml(self, options):
        """Creates the `build.xml` file for ant in `build/temp`."""
        # Template variables
        classpaths = sys.registry['java.class.path'].split(':')
        template_vars = {"classpaths": classpaths,
                         "lib_dir_exists": os.path.isdir(self.lib_dir),
                         "base_dir": self.base_dir,
                         "lib_dir": self.lib_dir,
                         "build_lib_dir": self.build_lib_dir,
                         "build_class_dir": self.build_class_dir}
        options.update(template_vars)
        build_tempalte = Template(filename=jump.jarlib_build_xml_template)
        build_xml = open(self.build_xml_filename, 'w')
        build_xml.write(build_tempalte.render(**options))
        build_xml.close()

    def command(self, args, options):
        """Executes the command."""
        self.copy_python_libs(options, self.build_class_dir)
        self.setup_dist_environments(options)
        self.create_build_xml(options)
        os.system('ant -buildfile %s' % self.build_xml_filename)
