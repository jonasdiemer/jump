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

import org.python.util.PythonInterpreter;

public class JumpFactory
{
    private static PythonInterpreter interpreter;

    public static PythonInterpreter getInterpreter() {
        if (interpreter == null) {
            interpreter = new PythonInterpreter();
            interpreter.exec("from jumpanttasks.syspath import set_sys_path");
            interpreter.exec("set_sys_path()");
        }
        return interpreter;
    }
}