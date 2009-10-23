#!/usr/bin/env python
# encoding: utf-8
"""
commands.py

Created by Olli Wang on 2009-10-21.
Copyright (c) 2009 Ollix. All rights reserved.
"""

import os
import sys
import shutil

import pkg_resources

import optparse

from mako.template import Template

import jump


class CommandError(Exception):
    pass

class OptionParser(object):
    """Simulates optparse.OptionParser for adding options in command classes.

    This class should only be used by classes which inherit from Command
    class. These command classes then can add options by instantiating this
    class as a class variable named `parser`, and use it to add group options
    as using optparse.OptionParser.

    For example:
    class SomeCommand(Command):
        parser = OptionParser()
        parser.add_option("-v", "--verbose", action="store_true",
                          default=False, help="run in verbose mode")
    """
    def __init__(self):
        self.__options = []

    def add_option(self, *args, **kw):
        self.__options.append((args, kw))

    def add_options_to_parser(self, parser):
        for args, kw in self.__options:
            parser.add_option(*args, **kw)

class Command(object):
    """The base class for commands.

    This is the base class for all commands. To implement a real command, you
    need to create a class inheriting from this base class and define a
    `command` method to do the real work. Note that you need to add two
    additional parameters to the `command` method in order to receive
    arguments and options received from command line. You may also want to
    instantiate a OptionParser instance as a class variable to add some group
    options.

    For example:
    class SomeCommand(Command):
        parser = OptionParser()
        parser.add_option("-v", "--verbose", action="store_true",
                          default=False, help="run in verbose mode")

        def command(self, args, options):
            print "Hi, I'm a sub-command!"
            print "Received args:", args
            print "Received options:", options

    Attributes:
        usage: The usage message displayed in help message.
        version: The string to print when supplying --version option.
    """

    usage = '%prog [options] arg1 arg2 ...'
    version = None

    def run(self, *args):
        """Executes the command.

        Decides which command to run and execute the `command` method
        within the proper command class. It also passes two arguments,
        `args` and `options`, parsed by optparse.OptionParser to the
        `command` method. You can also pass arguments directly to this method
        instead of calling it from command line.
        """
        # Set arguements from command line if not specified in parameters
        if not args:
            args = sys.argv[1:]

        parser = optparse.OptionParser(usage=self.usage, version=self.version)
        # Add options to parser
        if hasattr(self, 'parser') and isinstance(self.parser, OptionParser):
            self.parser.add_options_to_parser(parser)

        # Create a variable to cache subcommand classes in the form of
        # {COMMAND_NAME: COMMAND_CLASS, ...}
        command_classes = {}

        # Include subcommands if defined subcmd_entry_point
        if hasattr(self, 'subcmd_entry_point'):
            # Find all subcommand classes and add group options if available
            subcmd_entry_point = self.subcmd_entry_point
            for command in pkg_resources.iter_entry_points(subcmd_entry_point):
                command_class = command.load()

                # Add group options if specified
                if hasattr(command_class.__class__, 'parser') and \
                   isinstance(command_class.parser, OptionParser):
                    option_group = optparse.OptionGroup(parser, command.name)
                    command_class.parser.add_options_to_parser(option_group)
                    parser.add_option_group(option_group)

                # Cache command class
                command_classes[command.name] = command_class

        # Parse arguments from command line
        (options, args) = parser.parse_args(list(args))
        try:
            # Determine the command instance
            command_name = args[0] if args else None
            if command_name in command_classes:
                args.pop(0)     # Remove the subcommand argument
                command_class = command_classes[command_name]
                command_instance = command_class()
            else:
                command_instance = self
            # Execute the command
            command_instance.command(args, options)
        except CommandError, e:
            print 'Error:', e.message

    def command(self, args, options):
        """The real place to execute the command.

        This method should implemented manually in subclasses in order to
        execute the command.
        """
        raise NotImplementedError()

class JumpCommand(Command):
    """The basic Jump command.

    This class implement the basic Jump command. All Jump's subcommand classes
    should inherit from this class.

    Attributes:
        subcmd_entry_point: The entry point name for Jump's subcommands.
        usage: Modifies the default usage by adding a command argument.
        version: Indicates the current Jump version.
        parser: Instantiates OptionParse class to add some parser options.
    """
    subcmd_entry_point = 'jump.commands'
    usage = '%prog command [options] arg1 arg2 ...'
    version = '%prog ' + jump.VERSION

    parser = OptionParser()
    parser.add_option('-v', '--verbose', action="store_true",
                      default=False, help="run in verbose mode")

    def command(self, args, options):
        """Returns help message."""
        JumpCommand().run('-h')

class JumpDistCommand(JumpCommand):
    """Jump dist command.

    Make a distribution.
    """
    # Folder paths
    base_dir = os.getcwd()
    lib_dir = os.path.join(base_dir, 'lib')
    dist_dir = os.path.join(base_dir, 'dist')
    build_dir = os.path.join(base_dir, 'build')
    build_lib_dir = os.path.join(build_dir, 'lib')
    build_class_dir = os.path.join(build_dir, 'class')
    build_temp_dir = os.path.join(build_dir, 'temp')
    # File paths
    build_xml_filename = os.path.join(build_temp_dir, 'build.xml')
    default_main_java = os.path.join(build_temp_dir, 'Main.java')
    config_filename = os.path.join(base_dir, 'config.jp')
    # .jar files
    jython_jar_filename = os.path.join(jump.lib_dir, 'jython.jar')
    onejar_jar_filename = os.path.join(jump.lib_dir,
                                       'one-jar-ant-task-0.96.jar')
    # Templates
    build_template = os.path.join(jump.template_dir, 'build.xml.mako')
    main_java_template = os.path.join(jump.template_dir, 'main.java.mako')
    # Template variables
    config = {'base_dir': os.getcwd(),
              'lib_dir': lib_dir,
              'dist_dir': dist_dir,
              'build_dir': build_lib_dir,
              'build_lib_dir': build_lib_dir,
              'build_class_dir': build_class_dir,
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
                         self.build_temp_dir):
            os.mkdir(dir_name)

        # Create `dist` directory if not exists
        if not os.path.isdir(self.dist_dir):
            os.mkdir(self.dist_dir)

    def populate_config_parameters(self):
        """Populates parameters from the config file."""
        config_file = open(self.config_filename, 'r')
        for line in config_file:
            # Ignore from `#` to the end of line
            line = line.split('#')[0].strip()
            if not line:
                continue
            # Add parameters to `self.config` variable
            try:
                key, value = line.split('=')
            except:
                raise CommandError("Syntax error in config file.")
            self.config[key.strip()] = value.strip()
        config_file.close()

    def setup_main_entry_point(self):
        """Setup main entry point."""
        # Raise error if either a `java_main` or a `python_main` parameter
        # is not specified in config file
        if (self.config.has_key('java_main') and \
            self.config.has_key('python_main')) or \
           (not self.config.has_key('java_main') and \
            not self.config.has_key('python_main')):
            raise CommandError("You need to specify either a `java_main` or "
                               "a `python_main` parameter in your config "\
                               "file, but not both.")
        # Use default Java main class if `python_main` is specified
        elif self.config.has_key('python_main'):
            try:
                py_module, py_func = self.config['python_main'].split(':')
            except ValueError:
                raise CommandError("The `python_main` parameter should be " \
                                   "set in the form of " \
                                   "`some.module:main_function` in your " \
                                   "config file.")
            # Create the default Main.java file in `buile.temp` directory
            main_template_vars = {'main_module': py_module,
                                  'main_func': py_func}
            main_java_tempalte = Template(filename=self.main_java_template)
            main_java = open(self.default_main_java, 'w')
            main_java.write(main_java_tempalte.render(**main_template_vars))
            main_java.close()
            self.config['java_main'] = 'com.ollix.jump.Main'

    def copy_required_jar(self):
        """Copies required `.jar` files to `build` directory."""
        # Copy `jython.jar` file to `build/lib` directory if not provided
        if not os.path.isfile(os.path.join(self.lib_dir, 'jython.jar')):
            shutil.copy2(self.jython_jar_filename, self.build_lib_dir)

        # Copy `one-jar.jar` file to `build/temp` directory
        shutil.copy2(self.onejar_jar_filename, self.build_temp_dir)

    def copy_required_libs(self):
        """Copies required Python modules to `build/class` directory."""
        # Compile Python source code to $py.class file and copy it to
        # `build/class` directory
        lib_tracer = jump.libtracer.LibTracer(self.base_dir, quiet=False)
        lib_locations = lib_tracer.get_lib_locations()
        for sys_path, relative_path in lib_locations:
            src_path = os.path.join(sys_path, relative_path)
            dest_path = os.path.join(self.build_class_dir, relative_path)
            shutil.copyfile(src_path, dest_path)

    def create_build_xml(self):
        """Creates the `build.xml` file for ant in `build/temp`."""
        build_tempalte = Template(filename=self.build_template)
        build_xml = open(self.build_xml_filename, 'w')
        build_xml.write(build_tempalte.render(**self.config))
        build_xml.close()

    def command(self, args, options):
        """Executes the command."""
        self.populate_config_parameters()
        self.setup_main_entry_point()
        self.copy_required_jar()
        self.copy_required_libs()
        self.create_build_xml()
        os.system('ant -buildfile %s' % self.build_xml_filename)

def jump_command():
    """Runs the Jump command."""
    JumpCommand().run()
