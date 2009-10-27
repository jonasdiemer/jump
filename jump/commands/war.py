#!/usr/bin/env python
# encoding: utf-8
"""
war.py

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

import jump
from jump.commands.main import JumpCommand


class JumpWarCommand(JumpCommand):
    """Jump jar command.

    Make a Mac app bundle.
    """
    usage = "make a Mac app bundle"
    parser = jump.commands.OptionParser()
    parser.add_option('-w', '--wsgi_handler', action="store",
                      default='application.handler',
                      help="callable wsgi handler")
    parser.add_option('-l', '--log_level', action="store",
                      default='debug',  help="the level of diagnostic " \
                                             "output should be logged")
    parser.add_option('-c', '--cache_callables', action="store_true",
                      default=False,  help="whether or not it should cache " \
                                           "any callables it creates")
    parser.add_option('-g', '--google_app_engine', action="store",
                      default=None,  help="should set in the form of " \
                                           "`ID:VERSION`")
    required_options = ['wsgi_handler']

    # Basic configuration
    appengine_xml_filename = os.path.join(JumpCommand.build_temp_dir,
                                          'appengine-web.xml')

    def create_template_file(self, options):
        """Creates the `build.xml` file for ant in `build/temp`."""
        # Template variables
        template_vars = {"war_web_xml_filename": self.war_web_xml_filename,
                         "appengine_xml_filename": self.appengine_xml_filename,
                         "lib_dir_exists": os.path.isdir(self.lib_dir),
                         "base_dir": self.base_dir,
                         "lib_dir": self.lib_dir,
                         "build_lib_dir": self.build_lib_dir,
                         "build_class_dir": self.build_class_dir,
                         "build_temp_dir": self.build_temp_dir}
        options.update(template_vars)
        JumpCommand.create_template_file(self, jump.war_build_xml_template,
                                         self.build_xml_filename, options)
        JumpCommand.create_template_file(self, jump.war_web_xml_template,
                                         self.war_web_xml_filename, options)

        if options.google_app_engine:
            try:
                gae_id, gae_version = options.google_app_engine.split(':')
            except ValueError:
                error_message = "`google_app_engine` parameter is not set " \
                                "properly."
                raise jump.commands.CommandError(error_message)
            else:
                options.gae_id, options.gae_version = gae_id, gae_version
                JumpCommand.create_template_file(self,
                                                 jump.appengine_xml_template,
                                                 self.appengine_xml_filename,
                                                 options)

    def command(self, args, options):
        """Executes the command."""
        self.copy_jython_jars(options)
        self.copy_python_libs(options, self.build_class_dir)
        self.setup_dist_environments(options)
        self.create_template_file(options)
        os.system('ant -buildfile %s' % self.build_xml_filename)
