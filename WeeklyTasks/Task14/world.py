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
        
        # Target representation (a red star that agents usually seek/arrive at)
        self.target = pyglet.shapes.Star(
            cx / 2, cy / 2, 
            30, 1, 4, 
            color=COLOUR_NAMES['RED'], 
            batch=window.get_batch("main")
        )

        self.weight_labels = {
            'cohesion': pyglet.text.Label('Cohesion: 1.0', x=10, y=cy - 20, color=COLOUR_NAMES['WHITE'], font_size=12),
            'separation': pyglet.text.Label('Separation: 1.5', x=10, y=cy - 40, color=COLOUR_NAMES['WHITE'], font_size=12),
            'alignment': pyglet.text.Label('Alignment: 1.0', x=10, y=cy - 60, color=COLOUR_NAMES['WHITE'], font_size=12),
            'wander': pyglet.text.Label('Wander: 0.5', x=10, y=cy - 80, color=COLOUR_NAMES['WHITE'], font_size=12),
            'helper': pyglet.text.Label('Z/X: Cohesion  C/V: Separation  B/N: Alignment  M/,: Wander  F: Spawn  P: Pause', x=10, y=cy - 100, color=COLOUR_NAMES['GREY'], font_size=10)
}

    def update(self, delta):
        """Advances the simulation by one tick."""
        if not self.paused:
            for agent in self.agents:
                agent.update(delta)
        
        if self.agents:
            a = self.agents[0]
            self.weight_labels['cohesion'].text = f'Cohesion: {a.w_cohesion:.1f}'
            self.weight_labels['separation'].text = f'Separation: {a.w_separation:.1f}'
            self.weight_labels['alignment'].text = f'Alignment: {a.w_alignment:.1f}'
            self.weight_labels['wander'].text = f'Wander: {a.w_wander:.1f}'
    
    def draw_labels(self):
        for label in self.weight_labels.values():
            label.draw()

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
        """Handles keyboard events."""
        if symbol == pyglet.window.key.P:
            self.paused = not self.paused
        elif symbol == pyglet.window.key.F:
            self.agents.append(Agent(self))
        elif symbol in AGENT_MODES:
            for agent in self.agents:
                agent.mode = AGENT_MODES[symbol]
        # Cohesion
        elif symbol == pyglet.window.key.Z:
            for agent in self.agents: agent.w_cohesion = max(0.0, agent.w_cohesion - 0.1)
        elif symbol == pyglet.window.key.X:
            for agent in self.agents: agent.w_cohesion = min(5.0, agent.w_cohesion + 0.1)
        # Separation
        elif symbol == pyglet.window.key.C:
            for agent in self.agents: agent.w_separation = max(0.0, agent.w_separation - 0.1)
        elif symbol == pyglet.window.key.V:
            for agent in self.agents: agent.w_separation = min(5.0, agent.w_separation + 0.1)
        # Alignment
        elif symbol == pyglet.window.key.B:
            for agent in self.agents: agent.w_alignment = max(0.0, agent.w_alignment - 0.1)
        elif symbol == pyglet.window.key.N:
            for agent in self.agents: agent.w_alignment = min(5.0, agent.w_alignment + 0.1)
        # Wander
        elif symbol == pyglet.window.key.M:
            for agent in self.agents: agent.w_wander = max(0.0, agent.w_wander - 0.1)
        elif symbol == pyglet.window.key.COMMA:
            for agent in self.agents: agent.w_wander = min(5.0, agent.w_wander + 0.1)