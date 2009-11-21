/****************************************************************************
**
** Copyright (c) 2009 Ollix. All rights reserved.
**
** This file is part of Jump.
**
** Jump is free software: you can redistribute it and/or modify it under the
** terms of the GNU General Public License as published by the Free Software
** Foundation, either version 3 of the License, or any later version.
**
** Jump is distributed in the hope that it will be useful, but WITHOUT ANY
** WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
** FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
** details.
**
** You should have received a copy of the GNU General Public License along
** with Jump. If not, see <http://www.gnu.org/licenses/>.
**
****************************************************************************/

package com.ollix.jump.ant;

import org.apache.tools.ant.BuildException;
import org.apache.tools.ant.Task;
import com.ollix.jump.JythonFactory;
import com.ollix.jump.ant.JythonCompilerType;

public class JythonCompiler extends Task
{
    private JythonCompilerType jythonCompiler;

    public JythonCompiler() {
        JythonFactory supportSitePackages = new JythonFactory(
            "jump_jython_factory.syspath", "support_site_packages");
        supportSitePackages.call(true);

        JythonFactory factory = new JythonFactory(
            supportSitePackages.getState(), JythonCompilerType.class,
            "jump.ant.jython_compiler", "JythonCompiler");

        jythonCompiler = (JythonCompilerType) factory.init();
    }

    public void execute() throws BuildException {
        jythonCompiler.execute();
    }

    public void setDestDir(String destDir) {
        jythonCompiler.setDestDir(destDir);
    }

    public void setFullPackages(String packages) {
        jythonCompiler.setFullPackages(packages);
    }
}
