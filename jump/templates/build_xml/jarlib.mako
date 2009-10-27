<project name="${dist_name}" default="dist">

    <path id="classpath">
        % for classpath in classpaths:
		<pathelement location="${classpath}"/>
        % endfor
    </path>

    <target name="dist">
        <javac destdir="${build_class_dir}" srcdir="${base_dir}"
               classpathref="classpath"/>

		<jar destfile="${dist_path}.jar" basedir="${build_class_dir}">
			<manifest>
                <attribute name="Built-By" value="Jump"/>
            </manifest>
		</jar>
    </target>

</project>
