from __future__ import annotations

from pygame_gui.elements import UIScrollingContainer as __UIScrollingContainer
import pygame as pg

from pygame_gui.core import ObjectID
from pygame_gui.core.interfaces import IContainerLikeInterface
from pygame_gui.core.interfaces import IUIManagerInterface
from pygame_gui.core import UIElement


class ScrollingContainer(__UIScrollingContainer):
    def __init__(self, relative_rect: pg.Rect,
                 manager: IUIManagerInterface,
                 *,
                 starting_height: int = 1,
                 container: IContainerLikeInterface | None = None,
                 parent_element: UIElement | None = None,
                 object_id: dict[ObjectID, str] | None = None,
                 anchors: dict[str, str] | None = None,
                 visible: int = 1,
                 resize_automatically: int | float | tuple[int, int] | tuple[float, float] | pg.Vector2 | None = None):
        super(ScrollingContainer, self).__init__(
            relative_rect, manager, starting_height=starting_height, container=container,
            parent_element=parent_element, object_id=object_id, anchors=anchors, visible=visible
        )
        self.resize_automatically = resize_automatically

    def update(self, time_delta: float):
        super(ScrollingContainer, self).update(time_delta)

        if self.resize_automatically is not None:
            self.calculate_scrolling_dimensions(self.resize_automatically)

    def calculate_scrolling_dimensions(
            self, extra_buffer: int | float | tuple[int, int] | tuple[float, float] | pg.Vector2 = 0
    ):
        try:
            _ = len(extra_buffer)
            val = extra_buffer[0], extra_buffer[1]
        except TypeError:
            val = extra_buffer, extra_buffer

        space = self._get_space_taken_by_elements()
        self.set_scrollable_area_dimensions((val[0] + space[0], val[1] + space[1]))

    def _get_space_taken_by_elements(self):
        size_x = size_y = 0

        for item in self.scrollable_container.elements:
            size_x = max(size_x, item.get_relative_rect().right)
            size_y = max(size_y, item.get_relative_rect().bottom)

        return size_x, size_y
