import pygame as pg
from src.particle import *
import random
from src.groups import *
import src.constans as C


pg.init()
screen = pg.display.set_mode((C.WIDTH,C.HEIGHT))
clock = pg.time.Clock()
particleGroup = pg.sprite.Group()
fluidParticleGroup = FluidGroup()

# for _ in range(1000):
#     x = random.uniform(0, C.WIDTH)
#     y = random.uniform(0, C.HEIGHT)
#     vx = random.uniform(-100, 100) 
#     vy = random.uniform(-100, 100)
#     size = 4
#     color = 'white'
#     SolidParticle(color=color, groups=particleGroup, vx=vx, vy=vy, x=x, y=y, size=size)

for _ in range(1000):
    x = random.uniform(300,600)
    y = random.uniform(200,500)
    vx = random.uniform(-10, 10) 
    vy = random.uniform(-10, 10)
    radius = 16
    FluidParticle(color='blue',groups=(particleGroup,fluidParticleGroup), vx=vx, vy=vy, x=x, y=y,radius=radius)

def main_loop():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

        dt = clock.tick(C.FPS)/1000
        screen.fill((0,0,0))

        #collisionCheckParticle(particleGroup)
        fluidParticleGroup.initDensityPressure()
        checkCollisionsGrid(particleGroup)
        particleGroup.update(dt)

        particleGroup.draw(screen)
        pg.display.update()


main_loop()