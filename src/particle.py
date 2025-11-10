import pygame as pg
import random

class Particle():
    def __init__(self,mass = 1, ax = 0, ay = 0, vx = 0, vy = 0, x = 0, y = 0,size = 1):
        super().__init__()
        self.mass = mass
        self.a = pg.math.Vector2(ax,ay)
        self.v = pg.math.Vector2(vx,vy)
        self.pos = pg.math.Vector2(x,y)
        self.size = size #radius 
        self.lifetime = 10

    def accel(self,dt):
        self.v+=self.a*dt

    def move(self,dt):
        self.pos+=self.v*dt

    def lifeCycle(self, dt):
        self.lifetime-=dt

    def checkLife(self):
        if self.lifetime <= 0:
            return False
        return True 

    def update(self,dt): #second order ode로 update
        self.accel(dt)
        self.move(dt)
        self.lifeCycle(dt)
        self.checkLife()

    def isCollide(self,p):
        return self.pos.distance_to((p.pos.x,p.pos.y)) <= self.size