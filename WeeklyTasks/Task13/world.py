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
from agent import Agent, AGENT_MODES

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
        self.hunter = None # Placeholder for pursuit behaviour target
        
        # Target representation (a red star that agents usually seek/arrive at)
        self.target = pyglet.shapes.Star(
            cx / 2, cy / 2, 
            30, 1, 4, 
            color=COLOUR_NAMES['RED'], 
            batch=window.get_batch("main")
        )

        self.obstacles = [
            {'pos': Vector2D(cx * 0.2, cy * 0.3), 'radius': 60},
            {'pos': Vector2D(cx * 0.8, cy * 0.3), 'radius': 50},
            {'pos': Vector2D(cx * 0.5, cy * 0.7), 'radius': 70}
        ]
        self.obstacle_shapes = []
        for obs in self.obstacles:
            circle = pyglet.shapes.Circle(
                obs ['pos'].x, obs ['pos'].y, obs ['radius'],
                color=COLOUR_NAMES['GREY'],
                batch=window.get_batch("main")
            )
            self.obstacle_shapes.append(circle)

        self.hide_markers = []

    def update(self, delta):
        """Advances the simulation by one tick."""
        if not self.paused:
            for agent in self.agents:
                agent.update(delta)
        self.clear_markers()
        if self.hunter:
            prey = None 
            for agent in self.agents:
                if agent.mode == 'hide':
                    prey = agent
                    break
            if prey:
                spots = prey.calculate_hiding_spots(self.hunter.pos, self.obstacles)
                best_spot = prey.find_best_hiding_spot(self.hunter.pos, self.obstacles)
                size = 8
                for spot in spots:
                    is_best = best_spot and (spot.x == best_spot.x and spot.y == best_spot.y)
                    color = COLOUR_NAMES['GREEN'] if is_best else COLOUR_NAMES['YELLOW']
                    l1 = pyglet.shapes.Line(spot.x - size, spot.y - size, spot.x + size, spot.y + size, 2, color=color, batch=window.get_batch("info"))
                    l2 = pyglet.shapes.Line(spot.x + size, spot.y - size, spot.x - size, spot.y + size, 2, color=color, batch=window.get_batch("info"))
                    self.hide_markers.extend([l1, l2])
    def clear_markers(self):
        for marker in self.hide_markers:
            marker.delete()
        self.hide_markers.clear()

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
        """Handles keyboard events (e.g., pausing, changing agent modes)."""
        if symbol == pyglet.window.key.P:
            self.paused = not self.paused
        elif symbol == pyglet.window.key.A:
            self.agents.append(Agent(self))
        elif symbol in AGENT_MODES:
            # Update all agents to the selected behaviour mode
            for agent in self.agents[1: ]:
                agent.mode = AGENT_MODES[symbol]