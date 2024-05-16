from setuptools import setup, find_packages

setup(
    classifiers=[
        # 发展时期
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 开发的目标用户
        "Intended Audience :: Customer Service",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        # 属于什么类型
        "Topic :: Multimedia",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Sound/Audio :: CD Audio",
        "Topic :: Multimedia :: Sound/Audio :: Editors",
        # 许可证信息
        "License :: OSI Approved :: Apache Software License",
        # 目标 Python 版本
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    name="py_music_editer",
    version="0.1.0.alpha24051001",
    description="提供主流音乐文件数据与属性管理，读取与修改，以及工具集的Python库。",
    author="CooooldWind_",
    url="https://gitee.com/CooooldWind/PyMusicEditer",
    packages=find_packages(),
    install_requires=[
    ],
)
