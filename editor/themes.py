from __future__ import annotations

import json
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


def get_theme(name: str):
    """
    Returns game from name, if not found, returns None
    :param name: short name or full name
    :return: theme or None
    """
    if name in _themes:
        return _themes[name].theme

    for el in _themes:
        theme = _themes[el]
        if theme.full_name == name:
            return theme.theme
    return None


def get_theme_names() -> set[str]:
    """
    Returns set of full names of existing themes.
    """
    ret: set[str] = set()
    for name in _themes:
        theme = _themes[name]
        ret.add(theme.full_name)
    return ret


def get_theme_short_names() -> set[str]:
    """
    Returns set of short names of existing themes.
    :return:
    """
    ret: set[str] = set()
    for name in _themes:
        theme = _themes[name]
        ret.add(theme.file_name)
    return ret


def reload_themes():
    """
    Reloads themes form themes folder.
    """
    for path in themes_folder.iterdir():
        if path.is_file() and path.suffixes == [".theme", ".json"]:
            _themes[path.name.split(".")[0]] = _Theme(path.name.split(".")[0], json.loads(path.read_text()))


reload_themes()
