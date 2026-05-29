import pyglet
from vector2d import Vector2D
from graphics import COLOUR_NAMES, window

class Enemy:
    def __init__(self, pos, health=30):
        self.pos = pos.copy()
        self.health = health
        self.max_health = health
        self.alive = True
        self.radius = 20
        self.shape = pyglet.shapes.Circle(pos.x, pos.y, self.radius, color=COLOUR_NAMES['RED'], batch=window.get_batch("main"))

    
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.shape.delete()

    def draw_health_bar(self):
        pass