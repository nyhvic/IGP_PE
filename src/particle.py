import pygame as pg
import random

class Particle(pg.sprite.Sprite):
    def __init__(self, color, groups:pg.sprite.Group,mass = 1, ax = 0, ay = 0, vx = 0, vy = 0, x = 0, y = 0,size = 4):
        super().__init__(groups)
        self.mass = mass
        self.a = pg.math.Vector2(ax,ay)
        self.v = pg.math.Vector2(vx,vy)
        self.pos = pg.math.Vector2(x,y)
        self.size = size
        self.color = color
        self.lifetime = 10
        self.createSurf()

    def createSurf(self):
        self.image = pg.Surface((self.size, self.size)).convert_alpha()
        self.image.set_colorkey('black')
        pg.draw.circle(surface=self.image, color=self.color, center=(self.size / 2, self.size / 2), radius=self.size / 2)
        self.rect = self.image.get_rect(center=self.pos)

    def accel(self,dt):
        self.v+=self.a*dt

    def move(self,dt):
        self.pos+=self.v*dt
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def lifeCycle(self, dt):
        self.lifetime-=dt

    def checkLife(self):
        if self.lifetime <= 0:
            self.kill()    

    def handleCollision(self,other):
        if isinstance(other,Particle):
            normal = (self.pos-other.pos).normalize()
            self.v.reflect_ip(normal)




    def update(self,dt):
        self.accel(dt)
        self.move(dt)
        self.lifeCycle(dt)
        self.checkLife()



def collisionCheckParticle(particleGroup):
    collisions = pg.sprite.groupcollide(particleGroup, particleGroup, False, False, pg.sprite.collide_circle)
    for p1, collided_list in collisions.items():
        for p2 in collided_list:
            if p1 == p2:
                continue
            p1.handleCollision(p2)