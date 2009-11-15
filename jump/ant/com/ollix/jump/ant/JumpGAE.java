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
import org.python.util.PythonInterpreter;
import org.python.core.PyObject;
import org.python.core.PyString;
import com.ollix.jump.ant.JumpFactory;

public class JumpGAE extends Task
{
    private PyObject gae;
    private PyString destDir;
    private PyString string;

    public JumpGAE() {
        PythonInterpreter interpreter = JumpFactory.getInterpreter();
        interpreter.exec("from jump.ant.gae import gae");
        gae = interpreter.get("gae");

        destDir = new PyString("");
        string = new PyString("");
    }

    public void execute() throws BuildException {
        gae.__call__(this.destDir, this.string);
    }

    public void setDestDir(String destDir) {
        this.destDir = new PyString(destDir);
    }

    public void setString(String string) {
        this.string = new PyString(string);
    }
}