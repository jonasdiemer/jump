package com.ollix.jump;

import org.python.core.PyException;
import org.python.util.PythonInterpreter;

public class Main
{
    public static void main(String[] args) throws PyException
    {
        PythonInterpreter interpreter = new PythonInterpreter();
        interpreter.exec("import ${py_main_module} as module");
        interpreter.exec("module.${py_main_func}()");
    }
}
