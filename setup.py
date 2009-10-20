#!/usr/bin/env python
# encoding: utf-8
"""
setup.py

Created by Olli Wang on 2009-10-20.
Copyright (c) 2009 Ollix. All rights reserved.
"""

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(name='jump',
      version='0.9',
      description='Distributing Jython Scripts in a Jump!',
      license="GPLv3",
      author='Olli Wang',
      author_email='olliwang@ollix.com',
      url='http://opensource.ollix.org/jump',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[],
      extras_require = {},
      entry_points="""
      # -*- Entry points: -*-
      """,
      classifiers=[
          'Intended Audience :: Developers',
          "License :: OSI Approved",
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: Build Tools',
      ],
)
