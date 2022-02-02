from __future__ import annotations
import pygame as pg


def init():
    global window
    window = pg.display.set_mode(size, flags=flags, depth=depth, display=display, vsync=vsync)


def update_setting(
        _size: tuple[int, int] | None = None,
        _flags: int | None = None,
        _depth: int | None = None,
        _display: int | None = None,
        _vsync: int | None = None
):
    global size, flags, depth, display, vsync

    if _size is not None:
        size = _size

    if _flags is not None:
        flags = _flags

    if _depth is not None:
        depth = _depth

    if _display is not None:
        display = display

    if _vsync is not None:
        vsync = _vsync


size = (600, 600)
flags = 0  # default
depth = 0  # default
display = 0  # default
vsync = 0  # default
fps = 60
window: pg.Surface
clock = pg.time.Clock()
__frame_rate = 0


def tick():
    global __frame_rate
    __frame_rate = clock.tick(fps)
    return __frame_rate


def update():
    tick()
    pg.display.flip()


def frame_rate():
    return __frame_rate
