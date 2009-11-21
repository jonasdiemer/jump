#!/usr/bin/env python
# encoding: utf-8
"""
syspath.py

Created by Olli Wang (olliwang@ollix.com) on 2009-11-20.
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
import tempfile
import zipfile


def support_site_packages(unpack_eggs=False):
    if unpack_eggs:
        tempdir = os.path.join(tempfile.gettempdir(), 'jump.build.eggs')
        # Clean tempdir
        if os.path.isdir(tempdir):
            shutil.rmtree(tempdir)
        os.makedirs(tempdir)

    jython_lib_dir = os.path.join(os.environ['JYTHON_HOME'], 'Lib')
    site_package_dir = os.path.join(jython_lib_dir, 'site-packages')
    easy_install_pth = os.path.join(site_package_dir, 'easy-install.pth')
    sys.path.insert(0, site_package_dir)
    if os.path.isfile(easy_install_pth):
        for line in open(easy_install_pth, 'r'):
            line = line.strip()
            if not line or ' ' in line:
                continue
            if line.startswith('./'):
                egg_path = os.path.join(site_package_dir, line[2:])
            elif line.startswith('/'):
                egg_path = line
            else:
                continue
            # Unpack zipped egg file
            if unpack_eggs and zipfile.is_zipfile(egg_path):
                egg_path = unpack_egg(egg_path, tempdir)
            sys.path.insert(0, egg_path)

def unpack_egg(egg_path, tempdir):
    egg = zipfile.ZipFile(egg_path)
    egg_name = os.path.basename(egg_path)
    egg_dir = os.path.join(tempdir, egg_name)

    for name in egg.namelist():
        target = os.path.join(egg_dir, name)
        target_dirname = os.path.dirname(target)
        if not os.path.isdir(target_dirname):
            os.makedirs(target_dirname)
        f = open(target, 'wb')
        try:
            f.write(egg.read(name))
        finally:
            f.close()
    return egg_dir
