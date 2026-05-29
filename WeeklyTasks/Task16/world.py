"""World Environment for Steering Simulation.

This module defines the World class, which manages the simulation space, 
the target object, and the collection of agents. It handles spatial 
constraints (like toroidal wrap-around) and routes input events to 
relevant simulation entities.

Created by
    Clinton Woodward (2019)
    James Bonner (2024)
    contact: jbonner@swin.edu.au

Comments and code refactored by Enrique Ketterer <ekettererortiz@swin.edu.au>
- S1 2026

For class use only. Do not publicly share or post this code without permission.
"""

from vector2d import Vector2D
from matrix33 import Matrix33
import pyglet
from graphics import COLOUR_NAMES, window
from weapon import Weapon

WEAPON_PROFILES = {
    pyglet.window.key.R: ('Rifle', 800, 0.02, 4, COLOUR_NAMES['YELLOW']),
    pyglet.window.key.O: ('Rocket', 300, 0.02, 1, COLOUR_NAMES['ORANGE']),
    pyglet.window.key.H: ('Handgun', 700, 0.15, 3, COLOUR_NAMES['GREY']),
    pyglet.window.key.G: ('Grenade', 200, 0.3, 0.7, COLOUR_NAMES['GREEN']),
}

class World(object):
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.paused = False
        self.projectiles = []
        self.enemies = []
        self.soldier = None

    def update(self, delta):
        if self.paused:
            return
        if self.soldier:
            self.soldier.update(delta)

        for proj in self.projectiles[:]:
            proj.update(delta)
            if not proj.alive:
                self.projectiles.remove(proj)
                continue
            for enemy in self.enemies:
                if enemy.alive and proj.pos.distance(enemy.pos) < enemy.radius + 3:
                    enemy.take_damage(10)
                    proj.alive = False
                    proj.shape.delete()
                    self.projectiles.remove(proj)
                    break

        self.enemies = [e for e in self.enemies if e.alive]

    def wrap_around(self, pos):
        if pos.x > self.cx: pos.x -= self.cx
        elif pos.x < 0: pos.x += self.cx
        if pos.y > self.cy: pos.y -= self.cy
        elif pos.y < 0: pos.y += self.cy

    def input_keyboard(self, symbol, modifiers):
        if symbol == pyglet.window.key.P:
            self.paused = not self.paused
        elif symbol == pyglet.window.key.E:
            from enemy import Enemy
            from random import randrange
            pos = Vector2D(randrange(100, self.cx-100), randrange(100, self.cy-100))
            self.enemies.append(Enemy(pos))
        elif symbol in WEAPON_PROFILES and self.soldier:
            name, speed, acc, rate, color = WEAPON_PROFILES[symbol]
            self.soldier.weapon = Weapon(speed, acc, rate, color, window.get_batch("main"))
            print(f"Weapon: {name}")