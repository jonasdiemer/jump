#!/usr/bin/env python
# encoding: utf-8
"""
commands.py

Created by Olli Wang on 2009-10-21.
Copyright (c) 2009 Ollix. All rights reserved.
"""

import sys
import os

from optparse import OptionParser


def jump_command():
    parser = OptionParser()
    (options, args) = parser.parse_args()
    print os.system('ant')
