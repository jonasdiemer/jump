#!/usr/bin/env python
# encoding: utf-8
"""
war.py

Created by Olli Wang (olliwang@ollix.com) on 2009-11-21.
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

from com.ollix.jump.ant import WarTemplateType

from syspath import update_sys_path
update_sys_path()

from mako.template import Template

import jump


class WarTemplate(WarTemplateType):

    web_xml = 'web.xml'
    gae_xml = "appengine-web.xml"

    def __init__(self, dest_dir=None, wsgi_handler=None, no_multithread=None,
                 cache_callables=None, log_level=None, google_app_engine=None):
        self.dest_dir = dest_dir
        self.wsgi_handler = wsgi_handler
        self.no_multithread = no_multithread
        self.cache_callables = cache_callables
        self.log_level = log_level
        self.google_app_engine = google_app_engine

    def execute(self):
        self.create_web_descriptor()
        self.create_google_app_engine_descriptor()

    def create_web_descriptor(self):
        """Creates web.xml for the WAR file"""
        output_filename = os.path.join(self.dest_dir, self.web_xml)
        build_tempalte = Template(filename=os.path.join(jump.temp_dir,
                                                        self.web_xml))
        dest_file = open(output_filename, 'w')
        template_vars = dict(wsgi_handler=self.wsgi_handler,
                             no_multithread=self.no_multithread,
                             cache_callables=self.cache_callables,
                             log_level=self.log_level)
        dest_file.write(build_tempalte.render(**template_vars))
        dest_file.close()
        print "Create file: %s" % output_filename

    def create_google_app_engine_descriptor(self):
        """Creates appengine-web.xml for Google App Engine"""
        if not self.google_app_engine:
            return

        gae_id, gae_version = self.google_app_engine.split(':')
        output_filename = os.path.join(self.dest_dir, self.gae_xml)
        build_tempalte = Template(filename=os.path.join(jump.temp_dir,
                                                        self.gae_xml))
        dest_file = open(output_filename, 'w')
        dest_file.write(build_tempalte.render(gae_id=gae_id,
                                              gae_version=gae_version))
        dest_file.close()
        print "Create file: %s" % output_filename

    def setDestDir(self, dest_dir):
        self.dest_dir = dest_dir

    def setWsgiHandler(self, wsgi_handler):
        self.wsgi_handler = wsgi_handler

    def setNoMultithread(self, no_multithread):
        self.no_multithread = no_multithread

    def setCacheCallables(self, cache_callables):
        self.cache_callables = cache_callables

    def setLogLevel(self, log_level):
        self.log_level = log_level

    def setGoogleAppEngine(self, google_app_engine):
        self.google_app_engine = google_app_engine
