import pygame as pg
import src.constans as C    
from math import pi

class Particle(pg.sprite.Sprite):
    def __init__(self, color, groups:pg.sprite.Group,mass = 1, ax = 0, ay = C.G, vx = 0, vy = 0, x = 0, y = 0,radius = 2):
        super().__init__(groups)
        self.e=0.7
        self.mass = mass
        self.a = pg.math.Vector2(ax,ay)
        self.v = pg.math.Vector2(vx,vy)
        self.pos = pg.math.Vector2(x,y)
        self.radius = radius
        self.color = color
        self.lifetime = 1000
        self.createSurf()

    def createSurf(self):
        self.image = pg.Surface((self.radius*2, self.radius*2)).convert_alpha()
        self.image.set_colorkey('black')
        pg.draw.circle(surface=self.image, color=self.color, center=(self.radius, self.radius), radius=self.radius)
        self.rect = self.image.get_rect(center=self.pos)

    # 오일러 메소드 (1st order)
    # def accel(self,dt):
    #     self.v+=self.a*dt

    # def move(self,dt):
    #     self.pos+=self.v*dt
    #     self.rect.center = (int(self.pos.x), int(self.pos.y))

    def velocityVarlet(self,dt):
        #Velocity Varlet 이용 (2nd order)
        self.v+=0.5*self.a*dt
        self.pos+=self.v*dt
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        #self.a가 self.pos에 의해 바뀌면... do something

        self.v+=0.5*self.a*dt

    def lifeCycle(self, dt):
        self.lifetime-=dt

    def checkLife(self):
        if self.lifetime <= 0:
            self.kill()    

    def checkOut(self):
        if self.pos.x < self.radius:
            self.pos.x = self.radius
            self.v.x *=-0.3
        elif self.pos.x > C.WIDTH - self.radius:
            self.pos.x = C.WIDTH - self.radius
            self.v.x *=-0.3
        if self.pos.y < self.radius:
            self.pos.y = self.radius
            self.v.y *=-0.3
        elif self.pos.y > C.HEIGHT - self.radius:
            self.pos.y = C.HEIGHT - self.radius
            self.v.y *=-0.3


    def handleCollision(self,other):
        #배웠던 충돌 공식 사용
            diff = self.pos - other.pos
            dist = diff.length()
            if dist == 0: 
                return
            normal = diff / dist

            rvn = (self.v-other.v).dot(normal)
            if rvn>0:
                return
            p = -(self.e+1)*rvn
            p /= 2
            pn=p*normal

            other.v-=pn
            self.v+=pn

            pene = 0.2*(self.radius+other.radius - dist)
            other.pos-= pene*normal
            self.pos+= pene*normal

    def update(self,dt):
        self.velocityVarlet(dt)
        self.lifeCycle(dt)
        self.checkLife()
        self.checkOut()


class SolidParticle(Particle):
    def __init__(self, color, groups, mass=1, ax=0, ay=C.G, vx=0, vy=0, x=0, y=0, radius=2):
        super().__init__(color, groups, mass, ax, ay, vx, vy, x, y, radius)

    def handleCollision(self, other):
        if isinstance(other,SolidParticle):
            super().handleCollision(other)

        elif isinstance(other,FluidParticle):
            effect = other.v*0.1
            self.v+=effect



class FluidParticle(Particle):
    # Fluid 구성 입자들은 mass 1, smoothing radius(radius) 동일 가정
    def __init__(self, color, groups:pg.sprite.Group,mass = 1, ax = 0, ay = C.G, vx = 0, vy = 0, x = 0, y = 0,radius = 8):
        pg.sprite.Sprite.__init__(self,groups)
        self.e=0.5
        self.mass = mass
        self.a = pg.math.Vector2(ax,ay)
        self.v = pg.math.Vector2(vx,vy)
        self.pos = pg.math.Vector2(x,y)
        self.radius = radius #smoothing length
        self.color = color
        self.lifetime = 1000
        self.density = 1.e-8
        self.pressure = pg.math.Vector2(0,0)
        self.viscosity = pg.math.Vector2(0,0)
        self.mradius = radius/4 # middlepoint
        self.createSurf()


    def createSurf(self):
        self.image = pg.Surface((self.radius*2, self.radius*2)).convert_alpha()
        self.image.set_colorkey('black')
        pg.draw.circle(surface=self.image, color=(0,0,255,100), center=(self.radius, self.radius), radius=self.radius)
        pg.draw.circle(surface=self.image,color = self.color,center=(self.radius,self.radius),radius=self.mradius)
        self.rect = self.image.get_rect(center=self.pos)

    def handleCollision(self,other):
        if isinstance(other,SolidParticle):
            effect = other.v*0.1
            self.v+=effect
            self.lifetime = 1
        else:
            super().handleCollision(other)

    def initDensityPressure(self):
        self.density = 1.e-8
        self.pressure = pg.math.Vector2(0,0)

    def velocityVarletHalf(self,dt):
        #Velocity Varlet 이용 (2nd order)
        self.v+=0.5*self.a*dt
        self.pos+=self.v*dt
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def velocityVarletEnd(self,dt):
        #self.a가 self.pos에 의해 바뀜
        self.a = pg.Vector2(0,C.G) + self.pressure + self.viscosity# 압력으로 인한 a = pressure/mass  mass=1
        self.v+=0.5*self.a*dt

    def update(self,dt):
        self.velocityVarletHalf(dt)
        self.lifeCycle(dt)
        self.checkLife()
        self.checkOut()

    def makeDensity(self,p2,dist):
        #Poly6 커널함수 이용해 density 추가
        #315(smoothing_radius**2-dist**2)**3 / 64pismoothing_radius**9
        #약 4.9
        # c = 4.9/(pi*self.radius**9)
        # w = c*(self.radius**2-dist**2)**3
        
        #self.radius**9로 나눠 매우 작은 값이 되어버림
        #spiky kernel로 대체

        c = 10/(pi*self.radius**5)
        w = c*(self.radius-dist)**3
        self.density += w
        p2.density += w

    def densityToSPressure(self):
        #밀도를 압력으로 변환
        # K(density-optimaldensity)  K : 충분히 큰 상수 optimal_density : 상수
        return 1500* (self.density-0.05)

    def makePressure(self,p2,dirv,dist):
        Pi = max(self.densityToSPressure(),0) #self density to pressure
        Pj = max(p2.densityToSPressure(),0) #p2 density to pressure

        #Spiky 커널함수 gradient 이용 (Poly6은 x=0에서 미분불가?)
        # -30(smoothing_radius-dist)**2 dirv / pi*smoothing_radius**5
        c = -30/(pi*self.radius**5)
        gradw = (c*(self.radius-dist)**2 )* dirv

        # Fi(i(self)로의 압력) = -(Pi/self.density**2 + Pj/p2.density**2)grad(W(커널함수))
        f = -(Pi/self.density**2 + Pj/p2.density**2) * gradw 
        self.pressure+=f
        p2.pressure-=f

    def makeViscosity(self,p2,dist):
        #점성 추가
        # 2D viscosity 함수 라플라시안 사용
        u = 0.01
        c = 20 / (pi*self.radius**5)
        lapw = c*(self.radius-dist)
        self.viscosity += u*(p2.v-self.v) * lapw
        p2.viscosity += u*(self.v-p2.v) * lapw
        


class GasParticle(Particle):
    def __init__(self, color, groups, mass=1, ax=0, ay=-C.G//2, vx=0, vy=0, x=0, y=0, radius=2):
        super().__init__(color, groups, mass, ax, ay, vx, vy, x, y, radius)
        self.image.set_alpha(128)

    def handleCollision(self, other):
        if(not isinstance(other,GasParticle)):
            self.lifetime=0.1




def collisionCheckParticle(particleGroup):
    #pygame 라이브러리 내 충돌 판정
    #group 내의 모든 object와 1ㄷ1 판정하는듯(느리다)
    collisions = pg.sprite.groupcollide(particleGroup, particleGroup, False, False, pg.sprite.collide_circle)
    for p1, collided_list in collisions.items():
        for p2 in collided_list:
            if id(p1) >= id(p2):
                continue
            p1.handleCollision(p2)



def checkCollisionsGrid(particles, cellSize=16):
    #일정 크기 grid로 나누고 주변 grid 내의 object와 충돌 비교함
    grid = {}
    
    for p in particles:
        grid_x = int(p.pos.x // cellSize)
        grid_y = int(p.pos.y // cellSize)
        key = (grid_x, grid_y)
        
        if key not in grid:
            grid[key] = []
        grid[key].append(p)

    neighbor_offsets = [(0,0),(1,0),(0,1),(1,1)]

    for (gx, gy), cell_particles in grid.items():
        for p1 in cell_particles:
            for dx, dy in neighbor_offsets:
                neighbor_key = (gx + dx, gy + dy)
                if neighbor_key in grid:
                    for p2 in grid[neighbor_key]:
                        if id(p1) >= id(p2):
                            continue
                        dist = p1.pos.distance_squared_to(p2.pos)
                        radius = (p1.radius + p2.radius) / 2
                        
                        if dist < radius ** 2:
                            p1.handleCollision(p2)



'''
all particle group

particle manager

점성 적용

테스트/시연용 (단축키, 배치, clear)

fire, explosion
'''