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
from agent import Agent
from weapon import Weapon


WEAPON_PROFILES = {
    pyglet.window.key.R: ('Rifle', 800, 0.02, 4, COLOUR_NAMES['YELLOW']),
    pyglet.window.key.O: ('Rocket', 300, 0.02, 1, COLOUR_NAMES['ORANGE']),
    pyglet.window.key.H: ('Handgun', 700, 0.15, 3, COLOUR_NAMES['GREY']),
    pyglet.window.key.G: ('Grenade', 200, 0.3, 0.7, COLOUR_NAMES['GREEN']),
}
class World(object):
    """The simulation container holding agents and environmental state."""

    def __init__(self, cx, cy):
        # Dimensions of the world
        self.cx = cx
        self.cy = cy
        
        # State flags
        self.paused = True
        self.show_info = True
        
        # Simulation entities
        self.agents = []
        self.projectiles = []
        self.target_agent = None
        
        # Target representation (a red star that agents usually seek/arrive at)
        self.target = pyglet.shapes.Star(
            cx / 2, cy / 2, 30, 1, 4, 
            color=COLOUR_NAMES['RED'], 
            batch=window.get_batch("main")
        )

    def update(self, delta):
        """Advances the simulation by one tick."""
        if not self.paused:
            for agent in self.agents:
                agent.update(delta)
            for proj in self.projectiles[:]:
                proj.update(delta)
                if not proj.alive:
                    self.projectiles.remove(proj)
                elif self.target_agent:
                    if proj.pos.distance(self.target_agent.pos) < 20:
                        self.target_agent.on_hit()
                        proj.alive = False
                        proj.shape.delete()
                        self.projectiles.remove(proj)

    def wrap_around(self, pos):
        """Treats the world as a toroidal (wrap-around) space.
        
        Updates the x and y coordinates of the provided position object.
        """
        if pos.x > self.cx:
            pos.x -= self.cx
        elif pos.x < 0:
            pos.x += self.cx
            
        if pos.y > self.cy:
            pos.y -= self.cy
        elif pos.y < 0:
            pos.y += self.cy

    def transform_points(self, points, pos, forward, side, scale):
        """Transforms a list of local space points into world space.
        
        Useful for rendering complex shapes that rotate and scale with an agent.
        """
        # Create copies of points to avoid mutating the original definitions
        world_pts = [pt.copy() for pt in points]
        
        # Construct transformation matrix
        mat = Matrix33()
        mat.scale_update(scale.x, scale.y)
        mat.rotate_by_vectors_update(forward, side)
        mat.translate_update(pos.x, pos.y)
        
        # Apply transformation
        mat.transform_vector2d_list(world_pts)
        return world_pts
    
    def transform_point(self, point, pos, forward, side):
        world_pt = point.copy()
        mat = Matrix33()
        mat.rotate_by_vectors_update(forward, side)
        mat.translate_update(pos.x, pos.y)
        mat.transform_vector2d(world_pt)
        return world_pt

    def input_mouse(self, x, y, button, modifiers):
        """Handles mouse events (e.g., moving the target)."""
        if button == 1:  # Left click
            self.target.x = x
            self.target.y = y
    
    def input_keyboard(self, symbol, modifiers):
        if symbol == pyglet.window.key.P:
            self.paused = not self.paused
        elif symbol in WEAPON_PROFILES:
            name, speed, acc, rate, color = WEAPON_PROFILES[symbol]
            for agent in self.agents:
                if agent.mode == 'attack':
                    agent.weapon = Weapon(speed, acc, rate, color, window.get_batch("main"))
                    print(f"Weapon: {name}")