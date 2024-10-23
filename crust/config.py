from __future__ import annotations

import os
import platform
import importlib.util as iu

def get_rootPath(projectName: str = "crust"):
    status = iu.find_spec(projectName)
    if status is not None:
        return status.submodule_search_locations[0]
    else:
        try:
            os_name = platform.system()
            if os_name == "Windows":
                pathList = os.getcwd().split("\\")
                index = pathList.index(projectName)
                rootPath = ""
                for i in range(index + 1):
                    rootPath += pathList[i] + "\\"
            elif os_name == "Linux":
                pathList = os.getcwd().split("/")
                index = pathList.index(projectName)
                rootPath = ""
                for i in range(index + 1):
                    rootPath += pathList[i] + "/"
            else:
                rootPath = "."
                pass
            return rootPath
        except:
            raise FileNotFoundError("Please check your project name")