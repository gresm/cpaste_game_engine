from setuptools import setup
import pathlib as pt


reqs = pt.Path("requirements-api.txt")
long_desc = pt.Path("README-api.md")
setup(
    name="cpaste-api",
    version="0.0.1",
    author="gresm",
    description="Subpackage of cpaste - a game engine written in python using pygame",
    long_description=long_desc.read_text(),
    long_description_content_type="text/markdown",
    install_requires=reqs.read_text().split("\n"),
    packages=["cpaste_api"],
    package_dir={"cpaste_api": "api"},
    url="https://github.com/gresm/cpaste_game_engine"
)
