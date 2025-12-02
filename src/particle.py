import pygame as pg
import src.constans as C    

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
        if self.pos.x<0 or self.pos.x>C.WIDTH:
            self.kill()
        if self.pos.y<0 or self.pos.y>C.HEIGHT:
            self.kill()

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
            p/= 2
            pn=p*normal

            other.v-=pn
            self.v+=pn

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
    def __init__(self, color, groups:pg.sprite.Group,mass = 1, ax = 0, ay = C.G, vx = 0, vy = 0, x = 0, y = 0,radius = 16):
        pg.sprite.Sprite.__init__(self,groups)
        self.e=0.7
        self.mass = mass
        self.a = pg.math.Vector2(ax,ay)
        self.v = pg.math.Vector2(vx,vy)
        self.pos = pg.math.Vector2(x,y)
        self.radius = radius #smoothing length
        self.color = color
        self.lifetime = 1000
        self.density = 0
        self.pressure = pg.math.Vector2(0,0)
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
        self.density = 0
        self.pressure = pg.math.Vector2(0,0)
            


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



def checkCollisionsGrid(particles, cell_size=16):
    #일정 크기 grid로 나누고 주변 grid 내의 object와 충돌 비교함
    grid = {}
    
    for p in particles:
        grid_x = int(p.pos.x // cell_size)
        grid_y = int(p.pos.y // cell_size)
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
all particle group 만들어서 checkcollision 처리
fluid particle group에서 인접 particle 처리


fluid 초기화
all particle 충돌 처리
update (fluid 는 velocity varlet에서 마지막 v+1/2a는 안함)
fluid nearby 계산
fluid particle 마지막 v+1/2a (위치 변경에 의해 바뀐 a 적용)
'''