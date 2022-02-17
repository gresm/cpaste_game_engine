import pygame as pg
import pygame_gui as pgg
from . import themes, window, gui, gui_definitions as gd


def main():
    done = False
    pg.init()
    window.init()
    themes.set_current_theme("dark_mode")
    is_black = True
    current_gui = gui.generate(gd.menu_gui)

    def flip_theme():
        nonlocal is_black
        if is_black:
            themes.set_current_theme("light_mode")
        else:
            themes.set_current_theme("dark_mode")
        is_black = not is_black

    while not done:
        for ev in pg.event.get():
            gui.handle_event(ev)
            if ev.type == pg.QUIT:
                done = True
            elif ev.type == pg.KEYDOWN:
                if ev.key == pg.K_SPACE:
                    pass
            elif ev.type == pgg.UI_BUTTON_PRESSED:
                if ev.ui_element is current_gui.quit:
                    done = True
                elif ev.ui_element is current_gui.open:
                    current_gui = gui.generate(gd.open_gui)
                elif ev.ui_element is current_gui.back:
                    current_gui = gui.generate(gd.menu_gui)

        window.window.fill((0, 0, 0) if is_black else (255, 255, 255))

        gui.draw(window.window)
        gui.update()
        window.update()
