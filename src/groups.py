from src.particle import *
import pygame as pg

class FluidGroup(pg.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)

    def initDensityPressure(self):
        for p in self.sprites():
            p.initDensityPressure()

    def nearbyUpdate(self,dt,cellSize=16):
        #nearby 계산
        grid = {}
    
        for p in self.sprites():
            gridX = int(p.pos.x // cellSize)
            gridY = int(p.pos.y // cellSize)
            key = (gridX, gridY)
            if key not in grid:
                grid[key] = []
            grid[key].append(p)

        neighborOffsets = [(0,0),(1,0),(0,1),(1,1)]

        #밀도 계산
        for (gx, gy), gridParticles in grid.items():
            for p1 in gridParticles:
                for dx, dy in neighborOffsets:
                    neighborKey = (gx + dx, gy + dy)
                    if neighborKey in grid:
                        for p2 in grid[neighborKey]:
                            if id(p1) >= id(p2):
                                continue
                            
                            dist = (p1.pos-p2.pos).length()
                            #smoothing radius 동일
                            if 0 < dist <= p1.radius:
                                p1.makeDensity(p2,dist)

        #밀도 이용해서 압력 계산
        for (gx, gy), gridParticles in grid.items():
            for p1 in gridParticles:
                for dx, dy in neighborOffsets:
                    neighborKey = (gx + dx, gy + dy)
                    if neighborKey in grid:
                        for p2 in grid[neighborKey]:
                            if id(p1) >= id(p2):
                                continue
                            
                            distv = p1.pos-p2.pos
                            dist = max(distv.length(),1.e-8)
                            dirv = distv/dist
                            if 0 < dist <= p1.radius:
                                p1.makePressure(p2,dirv,dist)
                                p1.makeViscosity(p2,dist)

        #velocity Varlet 마저 업데이트
        for p in self.sprites():
            p.velocityVarletEnd(dt)


