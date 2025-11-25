import pygame as pg
import src.constans as C    

class Particle(pg.sprite.Sprite):
    def __init__(self, color, groups:pg.sprite.Group,mass = 1, ax = 0, ay = C.G, vx = 0, vy = 0, x = 0, y = 0,size = 4):
        super().__init__(groups)
        self.mass = mass
        self.a = pg.math.Vector2(ax,ay)
        self.v = pg.math.Vector2(vx,vy)
        self.pos = pg.math.Vector2(x,y)
        self.size = size
        self.color = color
        self.lifetime = 1000
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

    def checkOut(self):
        if self.pos.x<0 or self.pos.x>C.WIDTH:
            self.kill()
        if self.pos.y<0 or self.pos.y>C.HEIGHT:
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
        self.checkOut()


class SolidParticle(Particle):
    def __init__(self, color, groups, mass=1, ax=0, ay=C.G, vx=0, vy=0, x=0, y=0, size=4):
        super().__init__(color, groups, mass, ax, ay, vx, vy, x, y, size)

    def handleCollision(self, other):
        if isinstance(other,SolidParticle):
            normal = (self.pos-other.pos).normalize()
            diff = self.v-other.v
            p = diff.dot(normal)*normal
            self.v-=p
            other.v+=p

        elif isinstance(other,FluidParticle):
            effect = other.v*0.1
            self.v+=effect



class FluidParticle(Particle):
    def __init__(self, color, groups:pg.sprite.Group,mass = 1, ax = 0, ay = C.G, vx = 0, vy = 0, x = 0, y = 0,size = 4):
        super().__init__(color,groups,mass,ax,ay,vx,vy,x,y,size)
        self.combine=False
        self.group = groups

    def handleCollision(self,other):
        if isinstance(other,SolidParticle):
            effect = other.v*0.1
            self.v+=effect
            self.lifetime = 1
        elif isinstance(other,FluidParticle):
            if self.combine or other.combine:
                return
            middle = (self.pos+other.pos)/2
            FluidParticle(color='blue',groups=self.group,vx=(self.v.x+other.v.y)/2,vy=(self.v.y+other.v.y)/2,x=middle.x,y=middle.y,size=(self.size+other.size)*0.7)
            self.combine=True
            other.combine=True
            self.lifetime=0.1
            other.lifetime=0.1


class GasParticle(Particle):
    def __init__(self, color, groups, mass=1, ax=0, ay=C.G, vx=0, vy=0, x=0, y=0, size=4):
        super().__init__(color, groups, mass, ax, ay, vx, vy, x, y, size)




def collisionCheckParticle(particleGroup):
    collisions = pg.sprite.groupcollide(particleGroup, particleGroup, False, False, pg.sprite.collide_circle)
    for p1, collided_list in collisions.items():
        for p2 in collided_list:
            if id(p1) >= id(p2):
                continue
            p1.handleCollision(p2)



def checkCollisionsGrid(particles, cell_size=16):
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
                        radius = (p1.size + p2.size) / 2
                        
                        if dist < radius ** 2:
                            p1.handleCollision(p2)