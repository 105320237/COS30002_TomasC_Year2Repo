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
from graphics import window
from agent import Agent
from weapon import Weapon
from vector2d import Vector2D
import pyglet

# Global game instance (initialized in main.py)
game = None

class Game():

    def __init__(self):
        # Initialise the world based on the window size
        self.world = World(window.width, window.height)

        #default weapon
        _, speed, acc, rate, color = WEAPON_PROFILES[pyglet.window.key.R]
        weapon = Weapon(speed, acc, rate, color, window.get_batch("main"))
        
        #attacker 
        attacker = Agent(self.world, scale=25.0, mass=1.0, mode='attack', weapon=weapon)
        attacker.pos = Vector2D(window.width/2, window.height/2) #to stand still
        attacker.color = 'BLUE'
        attacker.update_vehicle_color()
        self.world.agents.append(attacker)

        #target
        target = Agent(self.world, scale=20.0, mass=1.0, mode='patrol')
        target.pos = Vector2D(150, 560)
        target.patrol_waypoints = [
            Vector2D(150, 560),
            Vector2D(650, 560)
        ]
        target.color = 'ORANGE'
        target.update_vehicle_color()
        self.world.agents.append(target)
        self.world.target_agent = target
    
        # Ensure the world is active upon startup
        self.world.paused = False

    def input_mouse(self, x, y, button, modifiers):
        """Routes mouse events to the world."""
        self.world.input_mouse(x, y, button, modifiers)

    def input_keyboard(self, symbol, modifiers):
        """Routes keyboard events to the world."""
        self.world.input_keyboard(symbol, modifiers)

    def update(self, delta):
        """Routes clock update events to the world."""
        self.world.update(delta)