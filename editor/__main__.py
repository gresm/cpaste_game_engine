import pygame as pg
from . import themes, window, gui, gui_definitions as gd


done = False
pg.init()
window.init()
themes.set_current_theme("dark_mode")
is_black = True
gui.generate(gd.menu_gui)

while not done:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            done = True
        elif ev.type == pg.KEYDOWN:
            if ev.key == pg.K_SPACE:
                if is_black:
                    themes.set_current_theme("light_mode")
                else:
                    themes.set_current_theme("dark_mode")
                is_black = not is_black
        gui.handle_event(ev)
    window.window.fill((0, 0, 0) if is_black else (255, 255, 255))

    gui.draw(window.window)
    gui.update()
    window.update()
