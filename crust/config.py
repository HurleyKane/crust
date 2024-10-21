from __future__ import annotations

import os
import platform


def get_rootPath(projectName: str = "crust"):
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


def chdir_rootPath():
    os.chdir(get_rootPath())
