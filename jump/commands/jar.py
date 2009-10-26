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
import shutil

from mako.template import Template

import jump

class JumpJarCommand(jump.commands.main.JumpCommand):
    """Jump dist command.

    Make a distribution.
    """
    usage = "make a distribution file"
    parser = jump.commands.OptionParser()
    parser.add_option('-m', '--main_entry_point', action="store",
                      default=None, help="main entry point, either Java or " \
                                         "Python")

    # Folder paths
    base_dir = os.getcwd()
    lib_dir = os.path.join(base_dir, 'lib')
    dist_dir = os.path.join(base_dir, 'dist')
    build_dir = os.path.join(base_dir, 'build')
    build_lib_dir = os.path.join(build_dir, 'lib')
    build_class_dir = os.path.join(build_dir, 'classes')
    build_resc_dir = os.path.join(build_dir, 'resources')
    build_temp_dir = os.path.join(build_dir, 'temp')
    # File paths
    build_xml_filename = os.path.join(build_temp_dir, 'build.xml')
    default_main_java = os.path.join(build_temp_dir, 'Main.java')
    config_filename = os.path.join(base_dir, 'config.jp')
    # .jar files
    jython_jar_filename = os.path.join(jump.lib_dir, 'jython.jar')
    jythonlib_jar_filename = os.path.join(jump.lib_dir, 'jython-lib.jar')
    onejar_jar_filename = os.path.join(jump.lib_dir,
                                       'one-jar-ant-task-0.96.jar')
    # Templates
    build_template = os.path.join(jump.template_dir, 'build.xml.mako')
    main_java_template = os.path.join(jump.template_dir, 'main.java.mako')
    license_template = os.path.join(jump.template_dir, 'license.mako')
    # Template variables
    config = {'base_dir': os.getcwd(),
              'lib_dir': lib_dir,
              'dist_dir': dist_dir,
              'build_dir': build_lib_dir,
              'build_lib_dir': build_lib_dir,
              'build_class_dir': build_class_dir,
              'build_resc_dir': build_resc_dir,
              'build_temp_dir': build_temp_dir,
              'onejar_jar_filename': onejar_jar_filename,
              'lib_dir_exists': os.path.isdir(lib_dir)}

    def __init__(self):
        """Initialize build environment.

        Creates some directories for build and distribution in the current
        working directory, the added directories include:
            CURRENT_DIRECTORY
            |-- build           # build-related files
            |   |-- lib         # .jar files
            |   |-- classes     # Java bytecode class files
            |   |-- temp        # temporary files
            |-- dist            # distribution files
        """
        # Create `build` directory and nested directories
        if os.path.isdir(self.build_dir):
            shutil.rmtree(self.build_dir)
        os.mkdir(self.build_dir)
        for dir_name in (self.build_lib_dir, self.build_class_dir,
                         self.build_resc_dir, self.build_temp_dir):
            os.mkdir(dir_name)

        # Create `dist` directory if not exists
        if not os.path.isdir(self.dist_dir):
            os.mkdir(self.dist_dir)

    def setup_main_entry_point(self, options):
        """Setup main entry point."""
        # Interpret `main_entry_point` parameter
        try:
            py_module, py_func = options.main_entry_point.split(':')
        except ValueError:
            # Set Java main class
            options.main_class = options.main_entry_point
        else:
            # Use default Main.java file to trigger Python main entry point
            main_template_vars = {'py_main_module': py_module,
                                  'py_main_func': py_func}
            main_java_tempalte = Template(filename=self.main_java_template)
            main_java = open(self.default_main_java, 'w')
            main_java.write(main_java_tempalte.render(**main_template_vars))
            main_java.close()
            options.main_class = 'com.ollix.jump.Main'

    def copy_required_jar(self, options):
        """Copies required `.jar` files to `build/lib` directory."""
        # Override default Jython JAR files if provided
        if os.path.isfile(os.path.join(self.lib_dir, 'jython.jar')):
            # The operation will be done in ant
            options.use_default_jython = False
        # Or, use Jython JAR files included in Jump
        else:
            options.use_default_jython = True
            shutil.copy2(self.jython_jar_filename, self.build_lib_dir)
            shutil.copy2(self.jythonlib_jar_filename, self.build_lib_dir)

        # Copy `one-jar.jar` file to `build/temp` directory
        shutil.copy2(self.onejar_jar_filename, self.build_temp_dir)

    def copy_default_resources(self):
        """Copies default resources to `build/resource` directory."""
        # Generate default license file
        license_tempalte = Template(filename=self.license_template)
        license = open(os.path.join(self.build_resc_dir, 'LICENSE'), 'w')
        license.write(license_tempalte.render())
        license.close()

    def create_build_xml(self, options):
        """Creates the `build.xml` file for ant in `build/temp`."""
        if not options.dist_name:
            options.dist_name = os.path.basename(self.base_dir)

        options.update(self.config)
        build_tempalte = Template(filename=self.build_template)
        build_xml = open(self.build_xml_filename, 'w')
        build_xml.write(build_tempalte.render(**options))
        build_xml.close()

    def command(self, args, options):
        """Executes the command."""
        self.setup_main_entry_point(options)
        self.copy_required_jar(options)
        self.copy_python_libs(options, self.build_class_dir)
        self.copy_default_resources()
        self.create_build_xml(options)
        os.system('ant -buildfile %s' % self.build_xml_filename)

    def clean(self):
        """Removes all generated files used for build."""
        # Remove `build` directory
        shutil.rmtree(self.build_dir)
