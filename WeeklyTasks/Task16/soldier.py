import pyglet
from vector2d import Vector2D
from graphics import COLOUR_NAMES, window
from math import sin, cos, radians, sqrt
from random import randrange
from fsm import FSM
from weapon import Weapon

class Soldier:
    def __init__(self, world, pos, patrol_waypoints, weapon):
        self.world = world
        self.pos = pos.copy()
        self.vel = Vector2D()
        self.heading = Vector2D(0, 1)
        self.side = Vector2D(1, 0)
        self.max_speed = 500.0
        self.max_force = 2000.0
        self.mass = 1.0
        self.friction = 0.98
        self.force = Vector2D()
        self.accel = Vector2D()

        self.weapon = weapon
        self.ammo = 10
        self.max_ammo = 10
        self.reload_time = 1.5
        self.reload_timer = 0.0
        self.detection_radius = 200.0
        self.waypoint_threshold = 30.0

        self.patrol_waypoints = patrol_waypoints
        self.patrol_index = 0
        self.current_enemy = None

        #visuals
        self.color = 'AQUA'
        self.shape = pyglet.shapes.Triangle(pos.x, pos.y - 10,
                                            pos.x - 8, pos.y + 10,
                                            pos.x + 8, pos.y + 10,
                                            color=COLOUR_NAMES[self.color], batch=window.get_batch("main"))
        self.fsm = FSM('patrol')
        self._build_fsm()


    def _build_fsm(self):
        # high level states
        patrol = self.fsm.add_state('patrol')
        attack = self.fsm.add_state('attack')

        patrol.add_transition('enemy_spotted', self.fsm.states['attack'])
        attack.add_transition('enemy_dead', self.fsm.states['patrol'])

        #low level patrol
        seek_wp = self.fsm.add_state('seek_waypoint')
        arrive_wp = self.fsm.add_state('arrive_waypoint')

        patrol.add_transition('start', seek_wp)
        seek_wp.add_transition('reached', arrive_wp)
        arrive_wp.add_transition('stopped', seek_wp)

        # low level attack
        shoot = self.fsm.add_state('shoot')
        reload_state = self.fsm.add_state('reload')

        attack.add_transition('start', shoot)
        shoot.add_transition('out_of_ammo', reload_state)
        reload_state.add_transition('reloaded', shoot)

        self.fsm.current = seek_wp

    def get_nearest_enemy(self):
        nearest = None
        nearest_dist = self.detection_radius
        for enemy in self.world.enemies:
            if not enemy.alive:
                continue
            d = self.pos.distance(enemy.pos)
            if d < nearest_dist:
                nearest_dist = d
                nearest = enemy
        return nearest

    def predict_interception(self, target):
        D = target.pos - self.pos
        Ps = self.weapon.projectile_speed
        a = -Ps * Ps
        b = 0
        c = D.dot(D)
        disc = b*b - 4*a*c
        if disc < 0:
            return target.pos
        t = (-b + sqrt(disc)) / (2*a)
        if t < 0:
            t = (-b - sqrt(disc)) / (2*a)
        if t < 0:
            return target.pos
        return target.pos

    def seek(self, target_pos):
        desired = (target_pos - self.pos).normalise() * self.max_speed
        return desired - self.vel

    def arrive(self, target_pos):
        decel = 0.6
        to_target = target_pos - self.pos
        dist = to_target.length()
        if dist < 5:
            return Vector2D()
        speed = min(dist / decel, self.max_speed)
        desired = to_target * (speed / dist)
        return desired - self.vel

    def update(self, delta):
        #check for enemies
        self.current_enemy = self.get_nearest_enemy()

        # high level transitions
        if self.fsm.current_name in ('patrol', 'seek_waypoint', 'arrive_waypoint'):
            if self.current_enemy:
                self.fsm.current = self.fsm.states['attack']
                self.fsm.current = self.fsm.states['shoot']
        elif self.fsm.current_name in ('attack', 'shoot', 'reload'):
            if not self.current_enemy:
                self.fsm.current = self.fsm.states['patrol']
                self.fsm.current = self.fsm.states['seek_waypoint']

        state = self.fsm.current_name

        #execute current state
        if state == 'seek_waypoint':
            wp = self.patrol_waypoints[self.patrol_index]
            self.force = self.seek(wp)
            if self.pos.distance(wp) < self.waypoint_threshold:
                self.fsm.current = self.fsm.states['arrive_waypoint']

        elif state == 'arrive_waypoint':
            wp = self.patrol_waypoints[self.patrol_index]
            self.force = self.arrive(wp)
            if self.vel.length() < 5:
                self.patrol_index = (self.patrol_index + 1) % len(self.patrol_waypoints)
                self.fsm.current = self.fsm.states['seek_waypoint']

        elif state == 'shoot':
            if self.current_enemy and self.weapon:
                aim = self.predict_interception(self.current_enemy)
                dir_to_aim = (aim - self.pos).normalise()
                self.heading = dir_to_aim
                self.side = self.heading.perp()
                self.weapon.update(delta)
                if self.weapon.can_fire():
                    if self.ammo > 0:
                        proj = self.weapon.fire(self.pos, aim)
                        if proj:
                            self.world.projectiles.append(proj)
                            self.ammo -= 1
                    if self.ammo <= 0:
                        self.fsm.current = self.fsm.states['reload']
                        self.reload_timer = self.reload_time
            self.force = Vector2D()

        elif state == 'reload':
            self.reload_timer -= delta
            if self.reload_timer <= 0:
                self.ammo = self.max_ammo
                self.fsm.current = self.fsm.states['shoot']
            self.force = Vector2D()

        else:
            self.force = Vector2D()

        #physics integration
        if state in ('seek_waypoint', 'arrive_waypoint'):
            self.force.truncate(self.max_force)
            self.accel = self.force / self.mass
            self.vel += self.accel * delta
            self.vel *= self.friction
            self.vel.truncate(self.max_speed)
            self.pos += self.vel * delta
            if self.vel.lengthSq() > 0.0001:
                self.heading = self.vel.get_normalised()
                self.side = self.heading.perp()
        else:
            self.vel = Vector2D()
            self.force = Vector2D()

        self.world.wrap_around(self.pos)
        self.shape.x = self.pos.x
        self.shape.y = self.pos.y
        self.shape.rotation = -self.heading.angle_degrees()