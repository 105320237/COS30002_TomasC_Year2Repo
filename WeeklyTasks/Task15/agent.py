"""
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
from math import sin, cos, radians, sqrt
from random import random, randrange, uniform

class Agent(object):
    DECELERATION_SPEEDS = {'slow': 0.9, 'normal': 0.6, 'fast': 0.3}

    def __init__(self, world=None, scale=30.0, mass=1.0, mode='seek', weapon=None):
        self.world = world
        self.mode = mode
        self.weapon = weapon

        angle = radians(random() * 360)
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.vel = Vector2D()
        self.heading = Vector2D(sin(angle), cos(angle))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)
        self.mass = mass

        self.force = Vector2D()
        self.accel = Vector2D()
        self.max_speed = 20.0 * scale
        self.max_force = 100.0 * scale
        self.friction = 0.98

        #Patrol
        self.patrol_waypoints = []
        self.patrol_index = 0
        self.waypoint_threshold = 30.0

        #Wander
        self.wander_target = Vector2D(1, 0)
        self.wander_dist = 2.0 * scale
        self.wander_radius = 1.5 * scale
        self.wander_jitter = 15.0

        self.color = 'ORANGE'
        self.vehicle_shape = [
            Point2D(-10, 6), Point2D(10, 0), Point2D(-10, -6)
        ]
        self._create_vehicle()

        self.hit_timer = 0.0
        self.original_color = self.color

        # Debug visuals
        self.info_force_vector = ArrowLine(Vector2D(0,0), Vector2D(0,0),
                                           colour=COLOUR_NAMES['BLUE'], batch=window.get_batch("info"))
        self.info_vel_vector = ArrowLine(Vector2D(0,0), Vector2D(0,0),
                                         colour=COLOUR_NAMES['AQUA'], batch=window.get_batch("info"))
        self.info_net_vectors = [
            ArrowLine(Vector2D(0,0), Vector2D(0,0), colour=COLOUR_NAMES['GREY'], batch=window.get_batch("info")),
            ArrowLine(Vector2D(0,0), Vector2D(0,0), colour=COLOUR_NAMES['GREY'], batch=window.get_batch("info")),
        ]

    def _create_vehicle(self):
        self.vehicle = pyglet.shapes.Triangle(
            self.pos.x + self.vehicle_shape[1].x, self.pos.y + self.vehicle_shape[1].y,
            self.pos.x + self.vehicle_shape[0].x, self.pos.y + self.vehicle_shape[0].y,
            self.pos.x + self.vehicle_shape[2].x, self.pos.y + self.vehicle_shape[2].y,
            color=COLOUR_NAMES[self.color], batch=window.get_batch("main")
        )
    
    def update_vehicle_color(self):
        self._create_vehicle()
    
    def predict_interception(self, target):
        D = target.pos - self.pos
        Tv = target.vel
        Ps = self.weapon.projectile_speed if self.weapon else 500.0

        a = Tv.dot(Tv) - Ps * Ps
        b = 2 * D.dot(Tv)
        c = D.dot(D)

        t = None
        if abs(a) < 1e-6:  #avoid division by zero
            if abs(b) > 1e-6:
                t = -c / b
        else:
            disc = b * b - 4 * a * c
            if disc >= 0:
                sqrt_disc = sqrt(disc)
                t1 = (-b + sqrt_disc) / (2 * a)
                t2 = (-b - sqrt_disc) / (2 * a)
                if t1 > 0 and t2 > 0:
                    t = min(t1, t2)
                elif t1 > 0:
                    t = t1
                elif t2 > 0:
                    t = t2
        
        if t is None or t < 0:
            return target.pos #in case of no valid solutions it will just aim at the current position
        return target.pos + target.vel * t


    def calculate(self, delta):
        mode = self.mode
        if mode == 'attack':
            force = Vector2D()
            if self.world.target_agent and self.weapon:
                self.weapon.update(delta)
                aim = self.predict_interception(self.world.target_agent)
                dir_to_aim = (aim - self.pos).normalise()
                self.heading = dir_to_aim
                self.side = self.heading.perp()
                if self.weapon.can_fire():
                    proj = self.weapon.fire(self.pos, aim)
                    if proj:
                        self.world.projectiles.append(proj)
        elif mode == 'patrol':
            force = self.patrol(delta)
        else:
            force = Vector2D()
        self.force = force
        return force

    def update(self, delta):
        """Updates the agent's physics and graphical representation."""
        if self.hit_timer > 0.0:
            self.hit_timer -= delta
            if self.hit_timer <= 0.0:
                self.color = self.original_color
                self._create_vehicle()
        if self.mode == 'attack':
            self.calculate(delta)
            self.vehicle.x = self.pos.x
            self.vehicle.y = self.pos.y
            self.vehicle.rotation = -self.heading.angle_degrees()
            return


        # 1. Calculate steering force
        force = self.calculate(delta)
        force.truncate(self.max_force)
        
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

    def on_hit(self):
        self.hit_timer = 0.3
        self.color = 'RED'
        self._create_vehicle()

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

    def wander(self, delta):
        jitter = self.wander_jitter * delta

        self.wander_target += Vector2D(uniform(-1, 1) * jitter, uniform(-1, 1) * jitter)
        self.wander_target.normalise()
        self.wander_target *= self.wander_radius
        target_local = self.wander_target + Vector2D(self.wander_dist, 0)

        world_target = self.world.transform_point(target_local, self.pos, self.heading, self.side)

        return self.seek(world_target)
    
    def patrol(self, delta):
        if not self.patrol_waypoints:
            return Vector2D()
        target_wp = self.patrol_waypoints[self.patrol_index]
        if self.pos.distance(target_wp) < self.waypoint_threshold:
            self.patrol_index = (self.patrol_index + 1) % len(self.patrol_waypoints)
            target_wp = self.patrol_waypoints[self.patrol_index]
        return self.arrive(target_wp, 'slow')