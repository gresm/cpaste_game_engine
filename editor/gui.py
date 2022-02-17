from __future__ import annotations

import pygame as pg
import pygame_gui as pgg

from typing import Type
from . import themes, window as wd


class GUIObjectPromise:
    def __init__(
            self, relative_rect: pg.Rect | tuple[int, int, int, int],
            gui_type: Type[pgg.core.ui_element.UIElement],
            container: pgg.core.ui_container.IContainerLikeInterface = None,
            anchors: dict[str, str] = None,
            visible: int = 1, **kwargs
    ):
        self.relative_rect = pg.Rect(relative_rect)
        self.gui_type = gui_type

        self.container = container
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
            container=self.container if container is None else container,
            **self.kwargs,
            anchors=self.anchors,
            visible=self.visible
        )

    @classmethod
    def from_raw(
            cls,
            raw: tuple[
                tuple[int, int, int, int] | pg.Rect,
                Type[pgg.core.ui_element.UIElement],
                None | tuple[
                    pgg.core.ui_container.IContainerLikeInterface | None,
                    int, dict[str, str], int
                ],
                None | dict[str, ...]
            ]
    ):
        rect = pg.Rect(raw[0])
        gui_type = raw[1]

        if raw[2] is None:
            named = {}
        else:
            named = {
                "container": raw[2][0], "starting_height": raw[2][1],
                "anchors": raw[2][2], "visible": raw[2][3]
            }

        if raw[3] is None:
            kwargs = {}
        else:
            kwargs = raw[3]

        kw = kwargs.copy()
        kw.update(named)

        return cls(rect, gui_type, **kw)


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

    @classmethod
    def from_raw(
            cls,
            raw: dict[
                str,
                tuple[
                    tuple[int, int, int, int] | pg.Rect,
                    Type[pgg.core.ui_element.UIElement],
                    None | tuple[
                        pgg.core.ui_container.IContainerLikeInterface,
                        int, dict[str, str], int
                    ],
                    None | dict[str, ...]
                ]
            ]
    ):
        parsed = {}

        for name in raw:
            parsed[name] = GUIObjectPromise.from_raw(raw[name])

        return cls(parsed)


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
