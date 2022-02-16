import pygame as pg
import pygame_gui as pgg

from . import GUIPromise, Obj


menu_gui = GUIPromise(
    {
        "new": Obj((25, 25, 200, 50), pgg.elements.UIButton, text="create new project"),
        "open": Obj((25, 125, 200, 50), pgg.elements.UIButton, text="open from save file"),
        "recent": Obj((25, 225, 200, 50), pgg.elements.UIButton, text="open recent projects"),
        "quit": Obj((25, 325, 200, 50), pgg.elements.UIButton, text="quit")
    }
)


open_gui = GUIPromise(
    {
        "test": Obj((25, 25, 200, 50), pgg.elements.UILabel, text="test")
    }
)


__all__ = [
    "menu_gui",
    "open_gui"
]
