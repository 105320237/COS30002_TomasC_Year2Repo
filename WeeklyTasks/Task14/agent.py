"""Autonomous Agent Steering Logic.

This module defines the Agent class, which implements various steering 
behaviours such as Seek, Flee, Arrive, and placeholders for Pursuit, 
Wander, and Path Following. It handles the physics integration (force -> 
acceleration -> velocity -> position) and updates the graphical representation.

Created by
    Clinton Woodward (2019)
    James Bonner (2024)
    contact: jbonner@swin.edu.au

Comments and code refactored by Enrique Ketterer <ekettererortiz@swin.edu.au>
- S1 2026

For class use only. Do not publicly share or post this code without permission.
"""

import pyglet
from vector2d import Vector2D, Point2D
from graphics import COLOUR_NAMES, window, ArrowLine
from math import sin, cos, radians
from random import random, randrange, uniform
from path import Path

# Mapping of keyboard keys to steering modes
AGENT_MODES = {
    pyglet.window.key._1: 'seek',
    pyglet.window.key._2: 'arrive_slow',
    pyglet.window.key._3: 'arrive_normal',
    pyglet.window.key._4: 'arrive_fast',
    pyglet.window.key._5: 'flee',
    pyglet.window.key._6: 'pursuit',
    pyglet.window.key._7: 'follow_path',
    pyglet.window.key._8: 'wander',
}

class Agent(object):
    """A vehicle agent with steering behaviours."""

    # Deceleration rates for the Arrive behaviour
    DECELERATION_SPEEDS = {
        'slow': 0.9,
        'normal': 0.6,
        'fast': 0.3,
    }

    def __init__(self, world=None, scale=30.0, mass=1.0, mode='seek'):
        # Reference to the simulation world
        self.world = world
        self.mode = mode
        
        # Physics state: position, velocity, and orientation
        angle = radians(random() * 360)
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.vel = Vector2D()
        self.heading = Vector2D(sin(angle), cos(angle))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)
        self.mass = mass
        
        # Forces and limits
        self.force = Vector2D()
        self.accel = Vector2D()
        self.max_speed = 20.0 * scale
        self.friction = 0.98
        # self.max_force = 100.0 # Example limit

        # ---- Graphical Representation ----
        self.color = 'ORANGE'
        # Local space vertices for a simple triangle vehicle
        self.vehicle_shape = [
            Point2D(-10,  6),
            Point2D( 10,  0),
            Point2D(-10, -6)
        ]
        
        # Main vehicle primitive
        self.vehicle = pyglet.shapes.Triangle(
            self.pos.x + self.vehicle_shape[1].x, self.pos.y + self.vehicle_shape[1].y,
            self.pos.x + self.vehicle_shape[0].x, self.pos.y + self.vehicle_shape[0].y,
            self.pos.x + self.vehicle_shape[2].x, self.pos.y + self.vehicle_shape[2].y,
            color=COLOUR_NAMES[self.color],
            batch=window.get_batch("main")
        )

        # ---- Debug/Info Visuals ----
        # Wander logic visuals (placeholders)
        self.info_wander_circle = pyglet.shapes.Circle(0, 0, 10, color=COLOUR_NAMES['WHITE'], batch=window.get_batch("info"))
        self.info_wander_target = pyglet.shapes.Circle(0, 0, 5, color=COLOUR_NAMES['GREEN'], batch=window.get_batch("info"))
        
        # Vectors: Blue = Steering Force, Aqua = Velocity, Grey = Desired Change
        self.info_force_vector = ArrowLine(Vector2D(0,0), Vector2D(0,0), colour=COLOUR_NAMES['BLUE'], batch=window.get_batch("info"))
        self.info_vel_vector = ArrowLine(Vector2D(0,0), Vector2D(0,0), colour=COLOUR_NAMES['AQUA'], batch=window.get_batch("info"))
        self.info_net_vectors = [
            ArrowLine(Vector2D(0,0), Vector2D(0,0), colour=COLOUR_NAMES['GREY'], batch=window.get_batch("info")),
            ArrowLine(Vector2D(0,0), Vector2D(0,0), colour=COLOUR_NAMES['GREY'], batch=window.get_batch("info")),
        ]

        ### STUDENT TODO: Initialise path and wander details here
        self.path = Path()
        self.randomise_path()
        self.waypoint_threshold = 20.0

        self.wander_target = Vector2D(1, 0)
        self.wander_dist = 2.0 * scale
        self.wander_radius = 1.5 * scale
        self.wander_jitter = 15.0

        self.max_force = 100.0 * scale

    def calculate(self, delta):
        """Calculates the accumulated steering force based on the current mode."""
        mode = self.mode
        target_pos = Vector2D(self.world.target.x, self.world.target.y)
        
        if mode == 'seek':
            force = self.seek(target_pos)
        elif mode == 'arrive_slow':
            force = self.arrive(target_pos, 'slow')
        elif mode == 'arrive_normal':
            force = self.arrive(target_pos, 'normal')
        elif mode == 'arrive_fast':
            force = self.arrive(target_pos, 'fast')
        elif mode == 'flee':
            force = self.flee(target_pos)
        elif mode == 'pursuit':
            force = self.pursuit(self.world.hunter)
        elif mode == 'wander':
            force = self.wander(delta)
        elif mode == 'follow_path':
            force = self.follow_path()
        else:
            force = Vector2D()
            
        self.force = force
        return force

    def update(self, delta):
        """Updates the agent's physics and graphical representation."""
        # 1. Calculate steering force
        force = self.calculate(delta)
        
        # 2. Integrate physics: F = ma -> a = F/m
        self.accel = force / self.mass
        
        # 3. Update velocity and clamp to max speed
        self.vel += self.accel * delta
        self.vel *= self.friction
        self.vel.truncate(self.max_speed)
        
        # 4. Update position
        self.pos += self.vel * delta
        
        # 5. Update orientation if moving
        if self.vel.lengthSq() > 0.00000001:
            self.heading = self.vel.get_normalised()
            self.side = self.heading.perp()
            
        # 6. Handle world boundaries (wrap-around)
        self.world.wrap_around(self.pos)
        
        # 7. Update graphical vehicle position and rotation
        # Note: Pyglet shapes rotation is in degrees, clockwise.
        self.vehicle.x = self.pos.x
        self.vehicle.y = self.pos.y
        self.vehicle.rotation = -self.heading.angle_degrees()

        # 8. Update debug vector visuals
        s = 0.5 # Scale factor for vector drawing
        self.info_force_vector.position = self.pos
        self.info_force_vector.end_pos = self.pos + self.force * s
        
        self.info_vel_vector.position = self.pos
        self.info_vel_vector.end_pos = self.pos + self.vel * s
        
        # Net change vectors (showing how force modifies velocity)
        self.info_net_vectors[0].position = self.pos + self.vel * s
        self.info_net_vectors[0].end_pos = self.pos + (self.force + self.vel) * s
        self.info_net_vectors[1].position = self.pos
        self.info_net_vectors[1].end_pos = self.pos + (self.force + self.vel) * s

    def speed(self):
        return self.vel.length()
    
    def randomise_path(self):
        cx, cy = self.world.cx, self.world.cy
        margin = min(cx, cy) * (1/6)
        self.path.create_random_path(5, margin, margin, cx - margin, cy - margin, looped=True)

    # ---- Steering Behaviour Implementations ----

    def seek(self, target_pos):
        """Calculates a force to move the agent towards a target."""
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return (desired_vel - self.vel)

    def flee(self, hunter_pos):
        panic_distance = 100.0
        if self.pos.distance(hunter_pos) > panic_distance:
            return Vector2D()
        desired_vel = (self.pos - hunter_pos).normalise() * self.max_speed
        return (desired_vel - self.vel)

    def arrive(self, target_pos, speed):
        """Steers the agent to arrive at a target with zero velocity."""
        decel_rate = self.DECELERATION_SPEEDS.get(speed, 0.6)
        to_target = target_pos - self.pos
        dist = to_target.length()
        
        if dist > 0.1:
            # Required speed to decelerate over the remaining distance
            req_speed = dist / decel_rate
            req_speed = min(req_speed, self.max_speed)
            desired_vel = to_target * (req_speed / dist)
            return (desired_vel - self.vel)
        return Vector2D(0, 0)

    def pursuit(self, evader):
        """Predicts an evader's future position and seeks towards it."""
        if evader is None:
            return Vector2D()
    
        to_evader = evader.pos - self.pos
        distance = to_evader.length()
        prediction_time = distance / self.max_speed
        future_pos = evader.pos + evader.vel * prediction_time
        return self.seek(future_pos)

    def wander(self, delta):
            """Randomly jitters a projected circle to produce organic movement."""
            jitter = self.wander_jitter * delta
            self.wander_target += Vector2D(uniform(-1, 1) * jitter, uniform(-1, 1) * jitter)
            self.wander_target.normalise()
            self.wander_target *= self.wander_radius
            target_local = self.wander_target + Vector2D(self.wander_dist, 0)
            world_target = self.world.transform_point(target_local, self.pos, self.heading, self.side)

            self.info_wander_target.x = world_target.x
            self.info_wander_target.y = world_target.y

            circle_center = self.pos + self.heading * self.wander_dist
            self.info_wander_circle.x = circle_center.x
            self.info_wander_circle.y = circle_center.y
            self.info_wander_circle.radius = self.wander_radius
            return self.seek(world_target)

    def follow_path(self):
        """Moves the agent along a predefined set of waypoints."""
        if self.path.is_finished():
            return self.arrive(self.path.current_pt(), 'slow')
        else:
            if self.pos.distance(self.path.current_pt()) < self.waypoint_threshold:
                self.path.inc_current_pt()
            return self.seek(self.path.current_pt())
