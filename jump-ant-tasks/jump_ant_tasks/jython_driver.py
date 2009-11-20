#!/usr/bin/env python
# encoding: utf-8
"""
jython_driver.py

Created by Olli Wang (olliwang@ollix.com) on 2009-11-18.
Copyright (c) 2009 Ollix. All rights reserved.

Jump is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or any later version.

Jump is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with Jump. If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys

from com.ollix.jump.ant import JythonDriverType

from syspath import update_sys_path
update_sys_path()

from mako.template import Template

import jump


class JythonDriver(JythonDriverType):

    def __init__(self, dest_dir=None, main_entry_point=None):
        self.dest_dir = dest_dir
        self.main_entry_point = main_entry_point

    def execute(self):
        try:
            py_module, py_func = self.main_entry_point.split(':')
        except ValueError:
            # Set Java main class
            return

        # Use default Main.java file to trigger Python main entry point
        template_vars = {'py_main_module': py_module, 'py_main_func': py_func}
        filename = 'Main.java'
        output_filename = os.path.join(self.dest_dir, filename)
        build_tempalte = Template(filename=os.path.join(jump.temp_dir,
                                                        filename))
        dest_file = open(output_filename, 'w')
        dest_file.write(build_tempalte.render(**dict(py_main_module=py_module,
                                                     py_main_func=py_func)))
        dest_file.close()
        print "Create file: %s" % output_filename

    def setDestDir(self, dest_dir):
        self.dest_dir = dest_dir

    def setMainEntryPoint(self, main_entry_point):
        self.main_entry_point = main_entry_point
