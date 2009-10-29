<project name="${dist_name}" default="dist">

    <taskdef name="launch4j"
             classname="net.sf.launch4j.ant.Launch4jTask"
             classpath="${launch4j_filename}:${xstream_filename}"
             onerror="report"/>

    <path id="classpath">
        % if lib_dir_exists:
        <fileset dir="${lib_dir}" includes="**/*.jar"/>
        % endif
        <fileset dir="${build_lib_dir}" includes="**/*.jar"/>
        <fileset dir="${jython_dirname}" includes="*.jar"/>
    </path>

    <target name="init">
        <delete dir="${dist_path}"/>
        <mkdir dir="${dist_path}"/>
        <mkdir dir="${dist_path}/lib"/>
        <copy todir="${dist_path}/lib">
            % if lib_dir_exists:
            <fileset dir="${lib_dir}" includes="**/*.jar"/>
            % endif
            <fileset dir="${build_lib_dir}" includes="**/*.jar"/>
            <fileset dir="${jython_dirname}" includes="*.jar"/>
        </copy>
    </target>

    <target name="dist" depends="init">
        % if jythonlib_not_exist:
        <jar destfile="${jythonlib_jar_filename}"
             basedir="${jythonlib_dirname}"
             excludes="site-packages/" includes="**/*.py"/>
        % endif

        <javac destdir="${build_class_dir}" srcdir="${base_dir}"
               classpathref="classpath"/>

        <pathconvert pathsep="${'${line.separator}'} " property="classpaths"
                     refid="classpath">
            <map from="${lib_dir}" to="lib"/>
            <map from="${build_lib_dir}" to="lib"/>
            <map from="${jython_dirname}" to="lib"/>
        </pathconvert>

        <jar destfile="${build_temp_dir}/main.jar"
             basedir="${build_class_dir}">
            <manifest>
                <attribute name="Main-Class" value="${main_class}"/>
                <attribute name="Built-By" value="${jump_version}"/>
            </manifest>
        </jar>

        <launch4j configFile="launch4j.xml"/>
    </target>

</project>