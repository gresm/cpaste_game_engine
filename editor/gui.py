import pygame as pg
import pygame_gui as pgg

from abc import ABC, abstractmethod
from typing import Type

from . import themes, window as wd


class GUIInfo(ABC):
    @abstractmethod
    def __init__(self, gui: pgg.UIManager):
        self.gui = gui


def draw(surface: pg.Surface):
    manager.draw_ui(surface)


def update():
    manager.update(wd.frame_rate())


def handle_event(event: pg.event.Event):
    manager.process_events(event)


def generate_gui(gui: Type[GUIInfo]):
    global manager, gui_info
    manager = pgg.UIManager(wd.size, themes.theme)
    gui_info = gui(manager)


manager: pgg.UIManager
gui_info: GUIInfo
