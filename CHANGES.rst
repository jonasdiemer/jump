CHANGES
=======
v0.9.7.3
========
* Puts cachdir directory in system temporary directory by default.
* Command option names were prefixed by subcommand's name if it is a subcommand's option.
* All command option names' underlines were replaces by dashes.
* Added FMPP and Ant contrib's license files.
* Added README file.
* Added CHANGES file.
* Remove ``*.jp`` pattern from MANIFEST.in

v0.9.7.2
========
* Supports ignoring specified Python packages.
* Fixed broken ``include_packages`` command option.
* Using ``pylibtracer``'s API to copy dependent Python packages.
* Updated to require ``pylibtracer`` v0.9.1.

v0.9.7.1
========
* Packages the jump-jython-factory.jar file into distribution if using default Jython driver.
* Updated to require ``oparse`` v0.9.1.

v0.9.7
======
* Excludes ``test`` directories from Jython's standard library when packaging into a JAR file.
* Fixed error when executing ``jarlib`` command.
* Compiles Jython modules after Java source files compiled.
* Included resource files in Jump's distribution.
* Migrated command's fundamentals to ``oparse`` project.
* Updated to require ``oparse`` v0.9.0.
* Code refactoring.
* Creates ``build.xml`` file for ANT to build independently.
* Rewrote Jump's ANT tasks using Jython's factory technique.
* Limits Jump that can be only installed with Jython.
* Created a function to update ``sys.path`` with packages in site-packages directory when executing jump's commands.
* Build-related files have been put in the system's temporary directory.
* Migrated ``libtracer`` module to an independent ``pylibtracer`` project.
* Using FMPP to create template files when building.
* The version string were retrieved by ``pkg_resources`` module.
* Makes sure all binaries preserve execute permissions.

v0.9.6.2
========
* Supports using 32 bit JavaApplicationStub when creating Mac App Bundles.
* Fixed the error to include all project's files in the final distribution.
* The ``LibTracer`` instance supports importing Java Classes in Jython modules.
* Excludes ``build`` and ``dist`` directories explicitly in the final distribution.

v0.9.6.1
========
* Supports using comments in manifest file.
* Fixed error if manifest file not existed.

v0.9.6
======
* Update Jump's website URL.
* Supports including and excluding resource files.
* Supports distributing ``Java only`` applications.
* Fixed error when executing ``jump`` command.
* Catches all ``CommandError``'s raised when executing commands.

v0.9.5.2
========
* Fixed error caused by missing variables.

v0.9.5.1
========
* Added the ``main_entry_point`` command option to be required in ``exe`` command.
* Included the GPLv3 license.

v0.9.5
======
* Fixed ``jar`` command's description.
* Supports making Mac App Bundles.
* Supports making WAR files.
* Supports making Windows EXE files.
* Put templates along their command's directory.
* Restricts importing Java classes at module level.
* Fixed error when setting main entry point.
* Supports Java Native Interface for the ``jar`` command.

v0.9.4
======
* Code refactoring.
* Supports including specified Python packages in the final distribution.
* Added ``main_entry_point`` command option to required options for the ``jar`` command.
* Removed required command options from ``jump``'s top level command.

v0.9.3
======
* Excludes modules in Jython's standard library from distributing.
* Separated Jython's standard library from the standard ``jython.jar`` file.

v0.9.2
======
* Fixed the error that not all project's modules are included in the final distribution.
* Created parent directories for each dependent module in the final distribution.
* Converts all Python modules to ``$py.class`` files explicitly.

v0.9.1
======
* Included ez_setup.py file in the Jump's distribution.
* Included templates in the Jump's distribution.
* Fixed some bugs.

v0.9.0
======
* Initial release
* Supports making standalone JAR files using One-JAR.
