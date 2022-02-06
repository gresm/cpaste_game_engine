from setuptools import setup
import pathlib as pt


reqs = pt.Path("requirements-editor.txt")
long_desc = pt.Path("README-engine.md")
setup(
    name="cpaste-editor",
    version="0.0.1",
    author="gresm",
    description="Graphical interface of cpaste - a game engine written in python using pygame",
    long_description=long_desc.read_text(),
    long_description_content_type="text/markdown",
    install_requires=reqs.read_text().split("\n"),
    packages=["cpaste_editor"],
    package_dir={"cpaste_editor": "editor"},
    url="https://github.com/gresm/cpaste_game_engine"
)
