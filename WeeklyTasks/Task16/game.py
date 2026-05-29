"""Game Controller for Autonomous Agents.

This module acts as the high-level controller, orchestrating the interaction 
between the world, input handling, and the application update loop.

Created by
    Clinton Woodward (2019)
    James Bonner (2024)
    contact: jbonner@swin.edu.au

Comments and code refactored by Enrique Ketterer <ekettererortiz@swin.edu.au>
- S1 2026

For class use only. Do not publicly share or post this code without permission.
"""

from world import World, WEAPON_PROFILES
from soldier import Soldier
from weapon import Weapon
from vector2d import Vector2D
from graphics import window
import pyglet

game = None

class Game:
    def __init__(self):
        self.world = World(window.width, window.height)

        _, speed, acc, rate, color = WEAPON_PROFILES[pyglet.window.key.R]
        weapon = Weapon(speed, acc, rate, color, window.get_batch("main"))

        patrol_path = [
            Vector2D(150, 150),
            Vector2D(650, 150),
            Vector2D(650, 550),
            Vector2D(150, 550),
        ]

        soldier = Soldier(self.world, Vector2D(150, 150), patrol_path, weapon)
        self.world.soldier = soldier
        self.world.paused = False

    def input_mouse(self, x, y, button, modifiers):
        pass

    def input_keyboard(self, symbol, modifiers):
        self.world.input_keyboard(symbol, modifiers)

    def update(self, delta):
        self.world.update(delta)