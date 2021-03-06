from setuptools import setup
import pathlib as pt

reqs = pt.Path("requirements-core.txt")
long_desc = pt.Path("README-core.md")
setup(
    name="cpaste-core",
    version="0.0.2",
    author="gresm",
    description="Internal part of cpaste - a game engine written in python using pygame",
    long_description=long_desc.read_text(),
    long_description_content_type="text/markdown",
    install_requires=reqs.read_text().split("\n"),
    packages=["cpaste_core"],
    package_dir={"cpaste_core": "core"},
    url="https://github.com/gresm/cpaste_game_engine",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
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
