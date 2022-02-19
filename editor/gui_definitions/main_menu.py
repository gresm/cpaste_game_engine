import pygame as pg
import pygame_gui as pgg

from . import GUIPromise, Obj, Container

menu_gui = GUIPromise(
    {
        "new": Obj((25, 25, 200, 50), pgg.elements.UIButton, text="create new project"),
        "open": Obj((25, 125, 200, 50), pgg.elements.UIButton, text="open from save file"),
        "recent": Obj((25, 225, 200, 50), pgg.elements.UIButton, text="open recent projects"),
        "quit": Obj((25, 325, 200, 50), pgg.elements.UIButton, text="quit")
    }
)

# pgg.elements.UIScrollingContainer


open_gui_back_rect = pg.Rect(0, 0, 200, 50)
open_gui_back_rect.bottomleft = 25, -25

open_gui = GUIPromise(
    {
        "back": Obj(
            open_gui_back_rect, pgg.elements.UIButton, text="go back", anchors={
                "left": "left", "right": "right", "top": "bottom", "bottom": "bottom"
            }
        ),
        "label1": Obj((25, 25, 200, 50), pgg.elements.UILabel, text="choose:"),
        "projects": Obj((50, 50, 200, 200), pgg.elements.UIScrollingContainer),
        "saves": Container(
            (25, 25, 200, 100),
            GUIPromise(
                {
                    "label1": Obj((25, 25, 200, 50), pgg.elements.UILabel, text="choose:"),
                    "label2": Obj((25, 50, 200, 50), pgg.elements.UILabel, text="choose:"),
                    "label3": Obj((25, 75, 200, 50), pgg.elements.UILabel, text="choose:"),
                }
            ),
            gui_type=pgg.elements.UIScrollingContainer
        )
    }
)

__all__ = [
    "menu_gui",
    "open_gui"
]
