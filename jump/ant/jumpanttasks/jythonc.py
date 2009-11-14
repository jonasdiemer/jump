#!/usr/bin/env python
# encoding: utf-8
"""
jythonc.py

Created by Olli Wang (olliwang@ollix.com) on 2009-11-14.
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

from jumpanttasks.libtracer import LibTracer


def get_sys_path():
    """Get system paths from the JYTHON_HOME environment variable."""
    jython_lib_dir = os.path.join(os.environ['JYTHON_HOME'], 'Lib')
    site_package_dir = os.path.join(jython_lib_dir, 'site-packages')
    easy_install_pth = os.path.join(site_package_dir, 'easy-install.pth')
    syspath = []
    if os.path.isfile(easy_install_pth):
        for line in open(easy_install_pth, 'r'):
            line = line.strip()
            if line and ' ' not in line:
                if line.startswith('./'):
                    path = os.path.join(site_package_dir, line[2:])
                elif line.startswith('/'):
                    path = line
                else:
                    continue
                syspath.append(path)
    syspath.append(site_package_dir)
    syspath.append(jython_lib_dir)
    return syspath

def jythonc(destdir, packages):
    """Copies required Python modules to specified directory."""
    if packages:
        packages = packages.split(',')

    # Find all required Python modules or packages and copy them
    # to the specified destnation directory
    sys.path.append(destdir)
    lib_tracer = LibTracer('.', quiet=True, full_packages=packages,
                           syspath=get_sys_path())
    lib_locations = lib_tracer.get_lib_locations()
    print 'Compiling %d source files to %s' % (len(lib_locations), destdir)
    for sys_path, relative_path in lib_locations:
        src_path = os.path.join(sys_path, relative_path)
        dest_path = os.path.join(destdir, relative_path)
        destdirname = os.path.dirname(dest_path)
        if not os.path.isdir(destdirname):
            os.makedirs(destdirname)
        shutil.copy2(src_path, dest_path)
