import pygame as pg
import pygame_gui as pgg

from . import GUIPromise, Obj


menu_gui = GUIPromise({"test": Obj((100, 100, 100, 100), pgg.elements.UIButton, text="test")})
