from setuptools import setup, find_packages

setup(
    name="mypackage20240516wkh",   # 包的名称, 该名称会用在PyPI(Python Package Index)上, 使用户通过这个名字来安装你的包.
    version='0.1',  # 包的版本号, 使用语义版本号(0.1, 1.0.0)来表示包的版本
    author='testpackage@testpacakge.com',   # 包的作者名
    author_email='testpackage@gmail.com',    # 包的作者的电子邮件
    description='a short description of the package',    # 对包的功能的简要描述
    long_description=open("README.md").read(),  # 对包的详细描述, 通常从一个Readme.md文件中读取. 这是在PyPI页面上显示的内容, 为用户提供包的详细信息.
    long_description_content_type="text/markdown",
    url="https://github.com/OovessaliusoO/git01",   # 包的主页URL
    packages=find_packages(),   # 包含在分发包中的所有Python包, 通常使用`find_packages()`来发现所有包.
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],  # 一个字符串列表, 用于为包提供一些额外的分类信息. PyPI使用这些分类信息来帮助用户找到你的包. 常见的分类器包括编程语言、许可证类型和操作系统兼容性
    python_requires='>=3.6',    # 指定包所兼容的Python版本.
    install_requires=[
        'numpy>=1.23.5'
    ]   # 一个字符串列表, 列出包依赖的其他Python包. 这些依赖项将在安装包时自动安装
)