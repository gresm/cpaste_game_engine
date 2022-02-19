from __future__ import annotations

import pygame as pg
import pygame_gui as pgg

from . import themes, window as wd
from typing import Type
from pygame_gui.core.interfaces import IContainerLikeInterface
from pygame_gui.core import UIContainer


class GUIObjectPromise:
    def __init__(
            self, relative_rect: pg.Rect | tuple[int, int, int, int],
            gui_type: Type[pgg.core.UIElement],
            container: pgg.core.ui_container.IContainerLikeInterface = None,
            anchors: dict[str, str] = None,
            visible: int = 1,
            *, on_load: str | None = None, **kwargs
    ):
        self.relative_rect = pg.Rect(relative_rect)
        self.gui_type = gui_type
        self.container = container

        self.anchors = anchors
        self.visible = visible

        self.on_load = on_load

        self.kwargs = kwargs

    def generate(
            self, ui_manager: pgg.core.interfaces.IUIManagerInterface,
            container: pgg.core.ui_container.IContainerLikeInterface = None
    ):
        ret = self.gui_type(
            relative_rect=self.relative_rect,
            manager=ui_manager,
            container=self.container or container,
            **self.kwargs,
            anchors=self.anchors,
            visible=self.visible
        )
        if self.on_load:
            exec(self.on_load, {"self": ret})
        return ret


class GUIPromise:
    def __init__(self, promises: dict[str, GUIObjectPromise]):
        self.promises = promises

        for name in promises:
            self.__dict__[name] = promises[name]

    def __getattr__(self, item) -> GUIObjectPromise | None:
        if item in self.promises:
            return self.promises[item]
        return None

    def __contains__(self, item):
        return item in self.promises

    def __getitem__(self, item):
        return self.__getattr__(item)

    def generate(
            self, ui_manager: pgg.core.interfaces.IUIManagerInterface,
            container: pgg.core.ui_container.IContainerLikeInterface = None
    ):
        generated = {}

        for name in self.promises:
            generated[name] = self.promises[name].generate(ui_manager, container)

        return GUIGenerated(generated)


class GUIContainerPromise(GUIObjectPromise):
    def __init__(
            self, relative_rect: pg.Rect | tuple[int, int, int, int],
            container_content: GUIPromise | GUIContainerPromise,
            gui_type: Type[pgg.core.UIElement | pgg.core.interfaces.IContainerLikeInterface] = UIContainer,
            container: pgg.core.ui_container.IContainerLikeInterface = None,
            anchors: dict[str, str] = None,
            visible: int = 1,
            *, on_load: str | None = None, **kwargs
    ):
        super(GUIContainerPromise, self).__init__(
            relative_rect, gui_type, container, anchors, visible, on_load=on_load, **kwargs
        )
        self.content = container_content

    def __getattr__(self, item) -> GUIObjectPromise | None:
        if item in self.content:
            return self.content[item]
        return None

    def __contains__(self, item):
        return item in self.content

    def __getitem__(self, item):
        return self.__getattr__(self.content)

    def generate(
            self, ui_manager: pgg.core.interfaces.IUIManagerInterface,
            container: pgg.core.ui_container.IContainerLikeInterface = None
    ):
        gen = super(GUIContainerPromise, self).generate(ui_manager, container)
        if isinstance(gen, IContainerLikeInterface):
            content = self.content.generate(ui_manager, gen)
            return GUIContainerGenerated(content, gen)
        content = self.content.generate(ui_manager, container)
        return GUIContainerGenerated(content, container)


class GUIGenerated:
    def __init__(self, generated: dict[str, pgg.core.UIElement | GUIContainerGenerated]):
        self.generated = generated

        for name in generated:
            self.__dict__[name] = generated[name]

    def __getattr__(self, item) -> pgg.core.UIElement | None:
        if item in self.generated:
            return self.generated[item]
        return None

    def __contains__(self, item):
        return item in self.generated

    def __getitem__(self, item):
        return self.__getattr__(item)


class GUIContainerGenerated:
    def __init__(self, generated: GUIGenerated, container: pgg.core.UIElement | IContainerLikeInterface):
        self._generated = generated
        self.generated = self._generated.generated
        self.container = container

        for name in generated.generated:
            self.__dict__[name] = self._generated.generated[name]

    def __getattr__(self, item) -> pgg.core.UIElement | None | object | type:
        if item in self._generated:
            return self._generated.generated[item]
        return getattr(self.container, item, None)

    def __contains__(self, item: str):
        return (item in self._generated or item in dir(self.container))\
               and not (item.startswith("__") or item.endswith("__"))

    def __getitem__(self, item):
        return self.__getattr__(item)


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
