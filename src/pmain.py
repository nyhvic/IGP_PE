import pygame as pg
from src.particle import Particle,collisionCheckParticle
import random


pg.init()
WIDTH = 1600
HEIGHT = 900
FPS = 60
screen = pg.display.set_mode((WIDTH,HEIGHT))
clock = pg.time.Clock()
particleGroup = pg.sprite.Group()

for _ in range(100):
    x = random.uniform(0, WIDTH)
    y = random.uniform(0, HEIGHT)
    vx = random.uniform(-100, 100) 
    vy = random.uniform(-100, 100)
    size = 4
    color = 'white'
    Particle(color=color, groups=particleGroup, vx=vx, vy=vy, x=x, y=y, size=size)

def main_loop():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

        dt = clock.tick(60)/1000
        screen.fill((0,0,0))

        collisionCheckParticle(particleGroup)

        particleGroup.draw(screen)
        particleGroup.update(dt)
        pg.display.update()


main_loop()