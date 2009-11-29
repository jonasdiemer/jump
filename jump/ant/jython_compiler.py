#!/usr/bin/env python
# encoding: utf-8
"""
jython_compiler.py

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
import shutil

from pylibtracer.libtracer import LibTracer

from com.ollix.jump.ant import JythonCompilerType


class JythonCompiler(JythonCompilerType):
    """Copies and compiles required Python modules to specified directory."""

    def __init__(self, dest_dir=None, packages=None):
        self.dest_dir = dest_dir
        self.packages = packages

    def execute(self):
        if self.packages:
            packages = [p.strip() for p in self.packages.split(',')]
        else:
            packages = []

        # Copy dependent files to specified directory
        sys.path.append(self.dest_dir)
        lib_tracer = LibTracer(full_packages=packages, quiet=True)
        count = lib_tracer.copy_to(self.dest_dir)
        if count:
            print 'Copy %d files to %s' % (count, self.dest_dir)

    def setDestDir(self, dest_dir):
        self.dest_dir = dest_dir

    def setFullPackages(self, packages):
        self.packages = packages
