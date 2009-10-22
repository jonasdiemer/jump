#!/usr/bin/env python
# encoding: utf-8
"""
commands.py

Created by Olli Wang on 2009-10-21.
Copyright (c) 2009 Ollix. All rights reserved.
"""

import sys
import os

import pkg_resources

import optparse

import jump


class Error(Exception):
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

def jump_command():
    """Runs the Jump command."""
    JumpCommand().run()
