<project name="${dist_name}" default="dist">

    <path id="classpath">
        % if lib_dir_exists:
        <fileset dir="${lib_dir}" includes="**/*.jar"/>
        % endif
        % if not java_only:
        <fileset dir="${jython_dirname}" includes="*.jar"/>
        % endif
    </path>

    <target name="dist">
        % if not java_only and jythonlib_not_exist:
        <jar destfile="${jythonlib_jar_filename}"
             basedir="${jythonlib_dirname}"
             excludes="site-packages/,**/test/" includes="**/*.py"/>
        % endif

        <javac destdir="${build_class_dir}" srcdir="${base_dir}"
               classpathref="classpath"/>

		<jar destfile="${dist_path}.jar" basedir="${build_class_dir}">
			<manifest>
                <attribute name="Built-By" value="${jump_version}"/>
            </manifest>
            <fileset dir="${base_dir}">
                <include name =""/>
                % for command, pattern in manifest_patterns:
                <${command} name="${pattern}"/>
                % endfor
                <exclude name="build/**"/>
                <exclude name="dist/**"/>
            </fileset>
		</jar>
    </target>

</project>
