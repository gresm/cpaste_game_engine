from setuptools import setup
import pathlib as pt

reqs = pt.Path("requirements-api.txt")
long_desc = pt.Path("README-api.md")
setup(
    name="cpaste-api",
    version="0.0.2",
    author="gresm",
    description="Subpackage of cpaste - a game engine written in python using pygame",
    long_description=long_desc.read_text(),
    long_description_content_type="text/markdown",
    install_requires=reqs.read_text().split("\n"),
    packages=["cpaste_api"],
    package_dir={"cpaste_api": "api"},
    url="https://github.com/gresm/cpaste_game_engine",
    classifiers=[
        "Development Status :: 1 - Planning",
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
