# 该库对C++进行
# 安装 python setup.py bdist_wheel
import setuptools
import subprocess

VERSION = '0.0.0'
package_name = f"crust"

subprocess.run(["pip", "install", "-r", "requirements.txt"])

setuptools.setup(
    name=package_name,
    version=VERSION,  # 两个地方都可以
    description="",
    author="chenmingkai",
    author_email="<chmingkai@outlook.com>",
    url="https://github.com/hurleykane/crust",
    packages=setuptools.find_packages("."), # 自动找
    include_pacVkage_data=True,
    package_data={
        # 引入任何包下的pyd文件，加入字典则对应包下的文件
        "crust": ["source/*"]
    },
    # install_requires=install_requires,
    setup_requires=[
    ], # 用于指定在构建或安装项目之前所需要的依赖项。这些依赖通常是为了支持 setup.py 的运行，或者是构建包的工具依赖
    extras_require={
    },# 用于 opencv 的依赖
)
