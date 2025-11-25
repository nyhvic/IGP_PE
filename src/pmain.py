import pygame as pg
from src.particle import Particle,collisionCheckParticle, SolidParticle, FluidParticle, checkCollisionsGrid
import random
import src.constans as C


pg.init()
screen = pg.display.set_mode((C.WIDTH,C.HEIGHT))
clock = pg.time.Clock()
particleGroup = pg.sprite.Group()

for _ in range(3000):
    x = random.uniform(0, C.WIDTH)
    y = random.uniform(0, C.HEIGHT)
    vx = random.uniform(-100, 100) 
    vy = random.uniform(-100, 100)
    size = 4
    color = 'white'
    SolidParticle(color=color, groups=particleGroup, vx=vx, vy=vy, x=x, y=y, size=size)

for _ in range(300):
    x = random.uniform(300,600)
    y = random.uniform(200,500)
    vx = random.uniform(-100, 100) 
    vy = random.uniform(-100, 100)
    size = 4
    FluidParticle(color='blue',groups=particleGroup, vx=vx, vy=vy, x=x, y=y, size=size)

def main_loop():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

        dt = clock.tick(C.FPS)/1000
        screen.fill((0,0,0))

        #collisionCheckParticle(particleGroup)
        checkCollisionsGrid(particleGroup)

        particleGroup.draw(screen)
        particleGroup.update(dt)
        pg.display.update()


main_loop()