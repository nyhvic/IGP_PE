import pygame as pg
from src.particle import Particle


pg.init()
WIDTH = 1600
HEIGHT = 900
FPS = 60
screen = pg.display.set_mode((WIDTH,HEIGHT))
clock = pg.time.Clock()
particleGroup = pg.sprite.Group()
p1 = Particle(color='red', groups=particleGroup,size = 50, ax=10,ay=10,x=WIDTH/2,y=HEIGHT/2)

def main_loop():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

        dt = clock.tick(60)/1000
        screen.fill((0,0,0))
        particleGroup.draw(screen)
        particleGroup.update(dt)
        pg.display.update()