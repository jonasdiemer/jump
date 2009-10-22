package com.ollix.jump;

import org.python.core.*;
import org.python.util.PythonInterpreter;

public class Main
{
    public static void main(String[] args) throws PyException
    {
        PythonInterpreter intrp = new PythonInterpreter();
        intrp.exec("import ${main_module}");
        intrp.exec("${main_module}.${main_func}()");
    }
}
