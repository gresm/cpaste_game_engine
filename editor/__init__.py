"""
This part of library is not ment to be imported, maybe try cpaste_core or cpaste_api?
Use it whenever you are sure that you want it.
"""
import pygame as pg
from . import window
from . import gui
from . import gui_definitions
from .run import main as _main


def init():
    pg.init()
    window.init()


def run():
    init()
    _main()
