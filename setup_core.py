from setuptools import setup
import pathlib as pt


reqs = pt.Path("requirements-core.txt")
long_desc = pt.Path("README-core.md")
setup(
    name="cpaste-core",
    version="0.0.1",
    author="gresm",
    description="Internal part of cpaste - a game engine written in python using pygame",
    long_description=long_desc.read_text(),
    long_description_content_type="text/markdown",
    install_requires=reqs.read_text().split("\n"),
    packages=["cpaste_core"],
    package_dir={"cpaste_core": "core"},
    url="https://github.com/gresm/cpaste_game_engine"
)
