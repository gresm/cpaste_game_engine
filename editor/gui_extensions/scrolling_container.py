from __future__ import annotations

from pygame_gui.elements import UIScrollingContainer as __UIScrollingContainer
import pygame as pg


class ScrollingContainer(__UIScrollingContainer):
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
