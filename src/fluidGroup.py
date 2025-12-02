from src.particle import *
import pygame as pg

class FluidGroup(pg.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)

    def initDensityPressure(self):
        for p in self.sprites:
            p.initDensityPressure()
