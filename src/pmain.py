import pygame as pg
from src.particle import *
from src.groups import *
from src.particlemanager import *
import src.constans as C
import sys


pg.init()
screen = pg.display.set_mode((C.WIDTH,C.HEIGHT))
clock = pg.time.Clock()
particleGroup = pg.sprite.Group()
fluidParticleGroup = FluidGroup()
particleManager = ParticleManager(particleGroup,fluidParticleGroup)

def main_loop():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    particleManager.toggleRain()
                if event.key == pg.K_c:
                    particleManager.clear()
                if event.key == pg.K_a:
                    particleManager.mode = C.NONE_MODE
                if event.key == pg.K_s:
                    particleManager.mode = C.SOLID_MODE
                if event.key == pg.K_d:
                    particleManager.mode = C.FLUID_MODE
                if event.key == pg.K_f:
                    particleManager.mode = C.GAS_MODE
        if pg.mouse.get_pressed()[0]:
            particleManager.click(pg.mouse.get_pos())

        dt = clock.tick(C.FPS)/1000
        screen.fill((0,0,0))

        particleManager.update(dt)
        particleManager.draw(screen)
        pg.display.update()


main_loop()