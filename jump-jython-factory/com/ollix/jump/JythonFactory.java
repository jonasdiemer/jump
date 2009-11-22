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

package com.ollix.jump;

import org.python.core.Py;
import org.python.core.PyObject;
import org.python.core.PySystemState;

public class JythonFactory {

    private final PySystemState state;
    private final Class interfaceType;
    private final PyObject callable;

    public JythonFactory(PySystemState state, Class interfaceType,
                         String callablePath) {
        String[] path = callablePath.split(":");
        String modulePath = path[0];
        String callableName = path[1];

        PyObject importer = state.getBuiltins().__getitem__(
                                    Py.newString("__import__"));
        PyObject module = importer.__call__(Py.newString(modulePath));
        String modules[] = modulePath.split("\\.");
        for (int i = 1; i < modules.length; i++) {
            String moduleName = modules[i];
            module = module.__getattr__(moduleName);
        }
        this.callable = module.__getattr__(callableName);

        this.state = state;
        this.interfaceType = interfaceType;
    }

    public JythonFactory(Class interfaceType, String callablePath) {
        this(new PySystemState(), interfaceType, callablePath);
    }

    public JythonFactory(PySystemState state, String callablePath) {
        this(state, null, callablePath);
    }

    public JythonFactory(String callablePath) {
        this(new PySystemState(), callablePath);
    }

    public PySystemState getState() {
        return state;
    }

    private PyObject[] convertToPyArguments(Object... args) {
        PyObject pyArgs[] = new PyObject[args.length];
        for (int i = 0; i < args.length; i++) {
            pyArgs[i] = Py.java2py(args[i]);
        }
        return pyArgs;
    }

    public Object init(Object... args) {
        PyObject pyArgs[] = convertToPyArguments(args);
        return callable.__call__(pyArgs).__tojava__(interfaceType);
    }

    public Object call(Object... args) {
        PyObject pyArgs[] = convertToPyArguments(args);
        return callable.__call__(pyArgs);
    }
}
