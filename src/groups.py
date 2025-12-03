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
            grid_x = int(p.pos.x // cellSize)
            grid_y = int(p.pos.y // cellSize)
            key = (grid_x, grid_y)
            if key not in grid:
                grid[key] = []
            grid[key].append(p)

        neighbor_offsets = [(0,0),(1,0),(0,1),(1,1)]

        #밀도 계산
        for (gx, gy), cell_particles in grid.items():
            for p1 in cell_particles:
                for dx, dy in neighbor_offsets:
                    neighbor_key = (gx + dx, gy + dy)
                    if neighbor_key in grid:
                        for p2 in grid[neighbor_key]:
                            if id(p1) >= id(p2):
                                continue
                            
                            dist = (p1.pos-p2.pos).length()
                            #smoothing radius 동일
                            if 0 < dist <= p1.radius:
                                p1.makeDensity(p2,dist)

        #밀도 이용해서 압력 계산
        for (gx, gy), cell_particles in grid.items():
            for p1 in cell_particles:
                for dx, dy in neighbor_offsets:
                    neighbor_key = (gx + dx, gy + dy)
                    if neighbor_key in grid:
                        for p2 in grid[neighbor_key]:
                            if id(p1) >= id(p2):
                                continue
                            
                            distv = p1.pos-p2.pos
                            dist = distv.length()
                            dirv = distv/dist
                            if 0 < dist <= p1.radius:
                                p1.makePressure(p2,dirv,dist)

        #velocity Varlet 마저 업데이트
        for p in self.sprites():
            p.velocityVarletEnd(dt)
