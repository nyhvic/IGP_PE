from src.particle import *
from src.groups import *
import src.constans as C
import pygame as pg
import random


class ParticleManager:
    def __init__(self,particleGroup : pg.sprite.Group,fluidParticleGroup : FluidGroup):
        self.particleGroup = particleGroup
        self.fluidParticleGroup = fluidParticleGroup
        self.rain = False
        self.mode = C.NONE_MODE

    def addSolidParticle(self,color='white', mass=1, ax=0, ay=C.G, vx=0, vy=0, x=0, y=0, radius=4):
        SolidParticle(color,self.particleGroup,mass,ax,ay,vx,vy,x,y,radius)

    def addFluidParticle(self,color='blue', mass=1, ax=0, ay=C.G, vx=0, vy=0, x=0, y=0, radius=8):
        FluidParticle(color,(self.particleGroup,self.fluidParticleGroup),mass,ax,ay,vx,vy,x,y,radius)

    def addGasParticle(self,color='white', mass=1, ax=0, ay=-C.G//2, vx=0, vy=0, x=0, y=0, radius=8):
        GasParticle(color,self.particleGroup,mass,ax,ay,vx,vy,x,y,radius)

    def toggleRain(self):
        self.rain = not self.rain
    
    def clear(self):
        self.particleGroup.empty()
        self.fluidParticleGroup.empty()

    def update(self,dt):
        if self.rain:
            x = random.uniform(0, C.WIDTH)
            y = random.uniform(0, 300)
            vx = random.uniform(-100, 100) 
            vy = random.uniform(0, 100)
            radius = 8
            self.addFluidParticle(x=x,y=y,vx=vx,vy=vy,radius=radius)
        self.fluidParticleGroup.initDensityPressure()
        checkCollisionsGrid(self.particleGroup)
        self.particleGroup.update(dt)
        self.fluidParticleGroup.nearbyUpdate(dt)

    def draw(self,screen):
        self.particleGroup.draw(screen)
    
    def click(self,pos):
        if self.mode == C.NONE_MODE:
            return
        for _ in range(20):
            x = random.uniform(max(pos[0]-50,0),min(pos[0]+50,C.WIDTH))
            y = random.uniform(max(pos[1]-50,0),min(pos[1]+50,C.HEIGHT))
            vx = random.uniform(-50,50)
            vy =  random.uniform(-50,50)
        if self.mode == C.SOLID_MODE:
            self.addSolidParticle(x=x,y=y,vx=vx, vy=vy)
        elif self.mode == C.FLUID_MODE:
            self.addFluidParticle(x=x,y=y,vx=vx, vy=vy)
        elif self.mode == C.GAS_MODE:
            self.addGasParticle(x=x,y=y,vx=vx, vy=vy)