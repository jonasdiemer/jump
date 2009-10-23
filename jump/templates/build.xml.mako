<project name="connected_sliders" default="dist">

    <taskdef name="one-jar"
             classname="com.simontuffs.onejar.ant.OneJarTask"
             classpath="${onejar_jar_filename}"
             onerror="report"/>

    <target name="dist">
        <javac destdir="${build_class_dir}" srcdir="${base_dir}">
            % if lib_dir_exists:
            <classpath location="${lib_dir}"/>
            % endif
        </javac>

        <javac destdir="${build_class_dir}" srcdir="${build_temp_dir}">
            % if lib_dir_exists:
            <classpath location="${lib_dir}"/>
            % endif
        </javac>

        <one-jar destfile="${dist_dir}/${project_name}.jar">
            <main>
                <fileset dir="${build_class_dir}"/>
            </main>
            <lib>
                % if lib_dir_exists:
                <fileset dir="${lib_dir}"/>
                % endif
                <fileset dir="${build_lib_dir}"/>
            </lib>
            <manifest>
                <attribute name="Main-Class"
                           value="com.simontuffs.onejar.Boot"/>
                <attribute name="One-Jar-Main-Class"
                           value="${main_class}"/>
                <attribute name="Built-By" value="Jump"/>
            </manifest>
        </one-jar>
    </target>

</project>
