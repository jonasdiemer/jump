package com.ollix.jump;

import org.python.core.PyException;
import org.python.util.PythonInterpreter;

public class Main
{
    public static void main(String[] args) throws PyException
    {
        PythonInterpreter intrp = new PythonInterpreter();
        intrp.exec("import ${py_main_module} as module");
        intrp.exec("module.${py_main_func}()");
    }
}
