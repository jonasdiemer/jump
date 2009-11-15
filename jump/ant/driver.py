#!/usr/bin/env python
# encoding: utf-8
"""
driver.py

Created by Olli Wang (olliwang@ollix.com) on 2009-11-15.
Copyright (c) 2009 Ollix. All rights reserved.

This file is part of Jump.

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

from mako.template import Template

import jump


def driver(main_entry_point, destdir):
    try:
        py_module, py_func = main_entry_point.split(':')
    except ValueError:
        # Set Java main class
        return

    # Use default Main.java file to trigger Python main entry point
    template_vars = {'py_main_module': py_module, 'py_main_func': py_func}
    filename = 'Main.java'
    output_filename = os.path.join(destdir, filename)
    build_tempalte = Template(filename=os.path.join(jump.temp_dir, filename))
    dest_file = open(output_filename, 'w')
    dest_file.write(build_tempalte.render(**dict(py_main_module=py_module,
                                                 py_main_func=py_func)))
    dest_file.close()
    print "Create file: %s" % output_filename
