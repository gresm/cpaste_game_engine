#!/usr/bin/env python
from sys import argv
from setuptools import setup
import pathlib as pt
import os
import shutil


def del_dir(folder: str):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


setups = [
    "setup_api.py",
    "setup_core.py",
    "setup_editor.py",
    "setup.py"
]

if len(argv) >= 2 and argv[1] == "all":
    ag = " ".join(argv[2:])
    for st in setups:
        print(f"running {st}")
        os.system(f"python3 {st} {ag}")
else:
    reqs = pt.Path("requirements.txt")
    long_desc = pt.Path("README.md")
    setup(
        name="cpaste",
        version="0.0.5",
        author="gresm",
        description="Game engine written in python using pygame",
        long_description=long_desc.read_text(),
        long_description_content_type="text/markdown",
        install_requires=reqs.read_text().split("\n"),
        packages=["cpaste"],
        package_dir={"cpaste": "main"},
        url="https://github.com/gresm/cpaste_game_engine",
        classifiers=[
            "Development Status :: 2 - Pre-Alpha",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: End Users/Desktop",
            "License :: OSI Approved",
            "License :: OSI Approved :: MIT License",
            "Operating System :: Android",
            "Operating System :: MacOS",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux",
            "Operating System :: Unix",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Topic :: Games/Entertainment",
            "Topic :: Software Development :: Libraries :: pygame"
        ]
    )
