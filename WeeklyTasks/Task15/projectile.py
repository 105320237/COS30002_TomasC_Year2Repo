import pyglet
from vector2d import Vector2D 

class Projectile:
    def __init__(self, pos, vel, color='yellow', lifetime=2.0, batch=None):
        self.pos = pos.copy()
        self.vel = vel.copy()
        self.speed = vel.length()
        self.color = color
        self.lifetime = lifetime
        self.age = 0.0
        self.alive = True

        self.shape = pyglet.shapes.Circle( pos.x, pos.y, 3, color=color, batch=batch)

    def update(self, delta):
        self.age += delta
        if self.age >= self.lifetime:
            self.alive = False
            self.shape.delete()
            return
        self.pos += self.vel * delta
        self.shape.x = self.pos.x
        self.shape.y = self.pos.y