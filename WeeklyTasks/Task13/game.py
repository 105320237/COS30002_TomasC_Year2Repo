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

from world import World
from graphics import window
from agent import Agent

# Global game instance (initialized in main.py)
game = None

class Game():
    """Main game application class."""

    def __init__(self):
        # Initialise the world based on the window size
        #hunter and prey setup
        self.world = World(window.width, window.height)
        hunter = Agent(self.world, scale = 35.0, mass = 2.0, mode = 'wander')
        hunter.color = 'RED'
        hunter.max_speed = 15.0 * hunter.scale.x
        hunter.max_force = 80.0 * hunter.scale.x
        hunter.update_vehicle_color()
        self.world.agents.append(hunter)


        prey = Agent(self.world, scale = 20.0, mass = 0.8, mode = 'hide')
        prey.color = 'GREEN'
        prey.max_speed = 30.0 * prey.scale.x
        prey.max_force = 150.0 * prey.scale.x
        prey.update_vehicle_color()
        self.world.agents.append(prey)

        self.world.hunter = hunter
        
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