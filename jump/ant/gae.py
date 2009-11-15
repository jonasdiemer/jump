#!/usr/bin/env python
# encoding: utf-8
"""
gae.py

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


def gae(destdir, string):
    if not string:
        return

    try:
        gae_id, gae_version = string.split(':')
    except ValueError:
        error_message = "`google_app_engine` parameter is not set " \
                        "properly."
        raise jump.commands.CommandError(error_message)

    filename = 'appengine-web.xml'
    output_filename = os.path.join(destdir, filename)
    build_tempalte = Template(filename=os.path.join(jump.temp_dir, filename))
    dest_file = open(output_filename, 'w')
    dest_file.write(build_tempalte.render(**dict(gae_id=gae_id,
                                                 gae_version=gae_version)))
    dest_file.close()
    print "Create file: %s" % output_filename
