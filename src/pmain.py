import pygame as pg


pg.init()
WIDTH = 1600
HEIGHT = 900
FPS = 60
screen = pg.display.set_mode((WIDTH,HEIGHT))

def main_loop():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

        screen.fill((0,0,0))