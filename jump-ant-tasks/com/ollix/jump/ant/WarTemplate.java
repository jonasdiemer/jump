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

import org.apache.tools.ant.BuildException;
import org.apache.tools.ant.Task;
import com.ollix.jump.JythonFactory;
import com.ollix.jump.ant.WarTemplateType;

public class WarTemplate extends Task
{
    private WarTemplateType warTemplate;

    public WarTemplate() {
        JythonFactory factory = new JythonFactory(
            WarTemplateType.class, "jump_ant_tasks.war_template", 
            "WarTemplate");

        warTemplate = (WarTemplateType) factory.init();
    }

    public void execute() throws BuildException {
        warTemplate.execute();
    }

    public void setDestDir(String destDir) {
        warTemplate.setDestDir(destDir);
    }
    
    public void setWsgiHandler(String wsgiHandler) {
        warTemplate.setWsgiHandler(wsgiHandler);
    }

    public void setNoMultithread(String noMultithread) {
        warTemplate.setNoMultithread(noMultithread);
    }

    public void setCacheCallables(String cacheCallables) {
        warTemplate.setCacheCallables(cacheCallables);
    }

    public void setLogLevel(String logLevel) {
        warTemplate.setLogLevel(logLevel);
    }
    
    public void setGoogleAppEngine(String googleAppEngine) {
        warTemplate.setGoogleAppEngine(googleAppEngine);
    }
}
