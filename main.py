import pygame as pg
from editor import window, gui


done = False
pg.init()
window.init()
gui.init()

while not done:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            done = True
        gui.handle_event(ev)
    gui.draw(window.window)
    gui.update()
    window.update()
