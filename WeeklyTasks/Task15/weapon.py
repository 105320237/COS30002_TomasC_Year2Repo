from vector2d import Vector2D
from projectile import Projectile
from math import cos, sin
import random

class Weapon:
    def __init__(self, projectile_speed, accuracy, fire_rate, color, batch):
        self.projectile_speed = projectile_speed
        self.accuracy = accuracy
        self.fire_rate = fire_rate
        self.color = color
        self.batch = batch
        self.cooldown = 0.0

    def can_fire(self):
        return self.cooldown <= 0.0
    
    def update(self, delta):
        if self.cooldown > 0.0:
            self.cooldown -= delta
    
    def fire(self, pos, target_point):
        if not self.can_fire():
            return None
        self.cooldown = 1.0 / self.fire_rate
        direction = (target_point - pos).normalise()
        if self.accuracy > 0:
            angle = random.uniform(-self.accuracy, self.accuracy)
            cos_a = cos(angle)
            sin_a = sin(angle)
            direction = Vector2D(direction.x * cos_a - direction.y * sin_a, direction.x * sin_a + direction.y * cos_a)
        
        vel = direction * self.projectile_speed
        return Projectile(pos, vel, self.color, batch=self.batch)
