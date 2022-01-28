from __future__ import annotations

import json
import atexit
from pathlib import Path


class _Theme:
    """
    Theme class
    """
    def __init__(self, file_name: str, theme_json: list):
        self.file_name = file_name
        self.full_name: str = theme_json[0]
        self.theme = theme_json[1]
        self._theme_json = theme_json


this_file = Path(__file__)
this_folder = this_file.parent
themes_folder = this_folder / "themes"
_themes: dict[str, _Theme] = {}
theme = this_folder / "current_theme.json"
current_theme: str = ""


def set_current_theme(name: str):
    global current_theme

    current_theme = name

    if name == "":
        default_theme()
        return True

    thm = _get_theme(name)
    if thm is None:
        default_theme()
        return False

    _write_to_current_theme(json.dumps(thm))
    return True


def default_theme():
    _write_to_current_theme("{}")


def _write_to_current_theme(txt: str):
    theme.write_text(txt)


def _get_theme(name: str):
    """
    Returns game from name, if not found, returns None
    :param name: short name or full name
    :return: theme or None
    """
    if name in _themes:
        return _themes[name].theme

    for el in _themes:
        th = _themes[el]
        if th.full_name == name:
            return th.theme
    return None


def get_theme_names() -> set[str]:
    """
    Returns set of full names of existing themes.
    """
    ret: set[str] = set()
    for name in _themes:
        th = _themes[name]
        ret.add(th.full_name)
    return ret


def get_theme_short_names() -> set[str]:
    """
    Returns set of short names of existing themes.
    :return:
    """
    ret: set[str] = set()
    for name in _themes:
        th = _themes[name]
        ret.add(th.file_name)
    return ret


def reload_themes():
    """
    Reloads themes form themes folder.
    """
    for path in themes_folder.iterdir():
        if path.is_file() and path.suffixes == [".theme", ".json"]:
            _themes[path.name.split(".")[0]] = _Theme(path.name.split(".")[0], json.loads(path.read_text()))


reload_themes()
atexit.register(default_theme)
