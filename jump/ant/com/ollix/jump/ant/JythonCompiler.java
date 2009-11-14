package com.ollix.jump.ant;

import org.apache.tools.ant.BuildException;
import org.apache.tools.ant.Task;
import org.python.util.PythonInterpreter;
import org.python.core.PyObject;
import org.python.core.PyString;

public class JythonCompiler extends Task {
    private PyObject jythonc;
    private PyString destdir;
    private PyString packages;

    public JythonCompiler() {
        PythonInterpreter interpreter = new PythonInterpreter();
        interpreter.exec("from jumpanttasks.jythonc import jythonc");
        jythonc = interpreter.get("jythonc");

        destdir = new PyString("");
        packages = new PyString("");
    }

    public void execute() throws BuildException {
        jythonc.__call__(this.destdir, this.packages);
    }

    public void setDestdir(String destdir) {
        this.destdir = new PyString(destdir);
    }

    public void setPackages(String packages) {
        this.packages = new PyString(packages);
    }
}