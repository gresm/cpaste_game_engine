from __future__ import annotations

import pygame as pg
import pygame_gui as pgg

from . import themes, window as wd
from typing import Type, cast
from pygame_gui.core.interfaces import IContainerLikeInterface


class GUIObjectPromise:
    def __init__(
            self, relative_rect: pg.Rect | tuple[int, int, int, int],
            gui_type: Type[pgg.core.ui_element.UIElement],
            anchors: dict[str, str] = None,
            visible: int = 1, **kwargs
    ):
        self.relative_rect = pg.Rect(relative_rect)
        self.gui_type = gui_type

        self.anchors = anchors
        self.visible = visible

        self.kwargs = kwargs

    def generate(
            self, ui_manager: pgg.core.interfaces.IUIManagerInterface,
            container: pgg.core.ui_container.IContainerLikeInterface = None
    ):
        return self.gui_type(
            relative_rect=self.relative_rect,
            manager=ui_manager,
            container=container,
            **self.kwargs,
            anchors=self.anchors,
            visible=self.visible
        )


class GUIPromise:
    def __init__(self, promises: dict[str, GUIObjectPromise]):
        self.promises = promises

    def generate(
            self, ui_manager: pgg.core.interfaces.IUIManagerInterface,
            container: pgg.core.ui_container.IContainerLikeInterface = None
    ):
        generated = {}

        for name in self.promises:
            generated[name] = self.promises[name].generate(ui_manager, container)

        return GUIGenerated(generated)


class GUIContainerPromise(GUIPromise, GUIObjectPromise):
    def __init__(
            self, promises: dict[str, GUIObjectPromise],
            relative_rect: pg.Rect | tuple[int, int, int, int],
            gui_type: Type[IContainerLikeInterface, pgg.core.UIElement] = pgg.core.UIContainer,
            anchors: dict[str, str] = None,
            visible: int = 1,
            **kwargs
    ):
        super(GUIPromise).__init__(relative_rect, gui_type, anchors=anchors, visible=visible, **kwargs)
        super(GUIObjectPromise, self).__init__(promises)

    def generate(
            self, ui_manager: pgg.core.interfaces.IUIManagerInterface,
            container: pgg.core.ui_container.IContainerLikeInterface = None
    ):
        container = cast(IContainerLikeInterface, GUIObjectPromise.generate(self, ui_manager, container))
        generated = {}

        for name in self.promises:
            generated[name] = self.promises[name].generate(ui_manager, container)

        return GUIGenerated(generated)


class GUIGenerated:
    def __init__(self, generated: dict[str, pgg.core.ui_element.UIElement]):
        self.generated = generated

        for name in generated:
            self.__dict__[name] = generated[name]

    def __getattr__(self, item) -> pgg.core.ui_element.UIElement | None:
        if item in self.generated:
            return self.generated[item]
        return None

    def __contains__(self, item):
        return item in self.generated


def draw(surface: pg.Surface):
    manager.draw_ui(surface)


def update():
    manager.update(wd.frame_rate())


def handle_event(event: pg.event.Event):
    manager.process_events(event)


def reset():
    global manager
    manager = pgg.UIManager(wd.size, str(themes.theme))


def add(gui: GUIPromise):
    global gui_info
    gui_info = gui.generate(manager)


def generate(gui: GUIPromise):
    reset()
    add(gui)
    return gui_info


manager: pgg.UIManager
gui_info: GUIGenerated
