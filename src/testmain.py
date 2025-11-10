import pygame as pg
from particle import Particle
import unittest

class Test(unittest.TestCase):
    def test_accel(self):
        p1 = Particle(ax=1,ay=1,vx=0,vy=2)
        p1.accel(1)
        self.assertEqual((p1.v.x,p1.v.y),(1.0,3.0))

    def test_move(self):
        p2 = Particle(ax=0,ay=0,vx=3,vy=5)
        p2.move(0.5)
        self.assertEqual((p2.pos.x,p2.pos.y),(1.5,2.5))

    def test_lifeCycle(self):
        p3 = Particle()
        p3.lifeCycle(5)
        check1 = p3.checkLife()
        p3.lifeCycle(6)
        check2 = p3.checkLife()
        self.assertEqual((check1,check2),(True,False))

    def test_update(self):
        p4 = Particle(ax=1,ay=3,vx=2,vy=1,x=0,y=0)
        p4.update(0.5)
        self.assertEqual(((p4.v.x,p4.v.y),(p4.pos.x,p4.pos.y)),((2.5,2.5),(1.25,1.25)))

    def test_many_updates(self):
        p5 = Particle(ax=2.5,ay=3.6,vx=1,vy=5.1,x=-2,y=2.1)
        for _ in range(10):
            p5.update(0.08)
        self.assertEqual(((p5.v.x,p5.v.y),(p5.pos.x,p5.pos.y)),((3.0000000000000004,7.980000000000002),(-0.32,7.4472000000000005)))

    def test_isCollide(self):
        p6 = Particle(x=0,y=0)
        p7 = Particle(x=1,y=0)
        pisCollide = p6.isCollide(p7)
        self.assertTrue(pisCollide)

    def test_isCollide_not(self):
        p8 = Particle(x=0,y=0)
        p9 = Particle(x=1,y=1)
        pisCollide = p8.isCollide(p9)
        self.assertFalse(pisCollide)

if __name__ == "__main__":
    unittest.main()
