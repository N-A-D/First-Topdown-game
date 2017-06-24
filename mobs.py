'''
@author: Ned Austin Datiles
'''

import pygame as pg
from random import choice, uniform, randint
from core_functions import collide_with_obstacles
from settings import *
from sprites import WeaponPickup, MiscPickup


class Mob(pg.sprite.Sprite):
    """
    This class represents an enemy object and its
    various attributes and abilities in game
    """

    def __init__(self, game, x, y):
        """
        Initializes a mob object for use in the game
        :param game: The game to which this mob will be employed
        :param x: x location in the plane
        :param y: y location in the plane
        """
        # Used to determine when the mob will be drawn
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups)

        # Image copies are necessary because if were not
        # for the copy, any damages pasted onto the enemy
        # image would be replicated onto the other enemies
        # even if they haven't been damaged
        self.original_image = choice(game.enemy_imgs).copy()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = vec(x, y)

        # Secondary rectangle for collisions is necessary
        # because rotation of the main rectangle warps its
        # size and causes issues with collision detection.
        self.hit_rect = ENEMY_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center

        self.speed = choice(ENEMY_SPEEDS)
        self.health = choice(ENEMY_HEALTH)
        self.damage = choice(ENEMY_DAMAGE)
        self.wander_radius = choice(WANDER_RING_RADIUS)

        # Positional, speed, and acceleration vectors
        self.pos = vec(self.rect.center)
        self.vel = vec(0, 0)
        self.acc = vec(self.speed, 0).rotate(uniform(0, 360))
        self.rot = 0

        # How fast this mob is able to track
        # the player
        self.seek_force = choice(SEEK_FORCE) * self.speed
        self.desired = vec(0, 0)
        self.can_pursue = False
        self.can_attack = True
        self.last_attack_time = 0

        # How often this mob will change targets while wondering
        self.last_target_time = 0
        if self.rect.x < WIDTH + TILESIZE and self.rect.y <= HEIGHT + TILESIZE:
            self.is_onscreen = True
        else:
            self.is_onscreen = False
        self.path = None
        self.current_path_target = 0
        self.last_path_found = 0

    def track_prey(self, target):
        now = pg.time.get_ticks()
        if (self.path == None or now - self.last_path_found > 12000) and randint(1, 100) % 3 == 0:
            self.last_path_found = now
            self.path = self.game.find_path(self, target)
            self.current_path_target = len(self.path) - 2

    def pause(self):
        """
        Slows down the attacks of mobs
        to reduce instant death for the player
        :return: None
        """
        self.can_attack = False
        self.last_attack_time = pg.time.get_ticks()

    def move_from_rest(self):
        """
        Moves the mob from rest
        :return: None
        """
        self.vel += self.acc * self.game.dt
        self.vel.scale_to_length(self.speed)

    def seek(self, target):
        """
        Gives a mob the ability to seek its target
        :param target: target to seek
        :return: Vector2 representing the steering force
        """
        self.desired = target - self.pos
        self.desired.normalize_ip()
        self.desired *= self.speed
        steer = self.desired - self.vel
        if steer.length() > self.seek_force:
            steer.scale_to_length(self.seek_force)
        return steer

    def seek_with_approach(self, target):
        """
        Gives a mob the ability to seek its target
        and slow down as it approaches the target
        :param target: target to seek
        :return: Vector2 representing the steering force
        """
        self.desired = target - self.pos
        dist = self.desired.length()
        self.desired.normalize_ip()
        if dist < APPROACH_RADIUS:
            self.desired *= dist / APPROACH_RADIUS * self.speed
        else:
            self.desired *= self.speed
        steer = self.desired - self.vel
        if steer.length() > self.seek_force:
            steer.scale_to_length(self.seek_force)
        return steer

    def wander(self):
        """
        Gives a mob the ability to wander its environment
        :return: None
        """
        if self.vel.length() == 0:
            self.move_from_rest()
        circle_pos = self.pos + self.vel.normalize() * WANDER_RING_DISTANCE
        target = circle_pos + vec(self.wander_radius, 0).rotate(uniform(0, 360))
        return self.seek(target)

    def pursue(self, prey):
        """
        Gives a mob the ability to pursue its prey.
        :param prey: The mob's target
        :return:
        """
        if prey.vel.length() == 0:
            target = prey.pos
        else:
            target = prey.pos + prey.vel.normalize()
        return self.seek(target)

    def cohesion(self):
        sum = vec(0, 0)
        count = 0
        all_obstacles = [mob for mob in self.game.mobs if mob.is_onscreen]
        for mob in all_obstacles:
            distance = (self.pos - mob.pos).length_squared()
            if 0 < distance < AVOID_RADIUS ** 2:
                sum += mob.pos
                count += 1
        if count > 0:
            sum /= count
            return self.seek(sum)
        else:
            return vec(0, 0)

    def align(self):
        sum = vec(0, 0)
        count = 0
        all_obstacles = [mob for mob in self.game.mobs if mob.is_onscreen]
        for mob in all_obstacles:
            distance = (self.pos - mob.pos).length_squared()
            if 0 < distance < AVOID_RADIUS ** 2:
                sum += mob.vel
                count += 1
        steer = vec(0, 0)
        if count > 0:
            sum /= count
            if sum.length() == 0:
                return steer
            sum.normalize()
            sum *= self.speed
            steer = sum - self.vel
            steer.scale_to_length(self.seek_force)
        return steer

    def separation(self):
        """
        Gives this mob the ability to avoid
        collisions with other obstacles
        :return: None
        """
        all_obstacles = [mob for mob in self.game.mobs if mob.is_onscreen]
        sum = vec(0, 0)
        count = 0
        for mob in all_obstacles:
            distance = (self.pos - mob.pos).length_squared()
            if 0 < distance < AVOID_RADIUS ** 2:
                diff = self.pos - mob.pos
                diff.normalize()
                diff /= distance
                sum += diff
                count += 1
        if count > 0:
            sum /= count
            if sum.length() == 0:
                return vec(0, 0)
            else:
                sum.normalize()
                sum *= self.speed
                steer = sum - self.vel
                return steer
        else:
            return vec(0, 0)

    def avoid_walls(self):
        sum = vec(0, 0)
        count = 0
        for wall in self.game.walls:
            distance = (self.pos - wall.pos).length_squared()
            if 0 < distance < AVOID_RADIUS ** 2:
                diff = (self.pos - wall.pos).normalize() / distance
                sum += diff
                count += 1
        steer = vec(0, 0)
        if count > 0:
            sum /= count
            sum *= self.speed
            steer = sum - self.vel
        return steer

    def apply_flocking_behaviour(self):
        """
        Applies flcoking steering behaviours to the mob
        :return: None
        """
        self.acc += self.separation() + self.align() + self.cohesion()

    def apply_pursuing_behaviour(self):
        """
        Allows the mob to pursue the target
        :return:
        """
        self.acc += self.pursue(self.game.player) + self.separation() + self.align() + self.cohesion()

    def apply_wandering_behaviour(self):
        """
        Gives a mob the ability to wander the around.
        :return:
        """
        self.acc += self.wander() + self.separation() + self.align() + self.cohesion()

    def check_if_is_on_screen(self):
        """
        Used to check if this mob is on the screen or not
        :return: True if on the screen, False otherwise
        """
        location = vec(self.hit_rect.x + self.game.camera.camera.x, self.hit_rect.y + self.game.camera.camera.y)
        if location.x <= WIDTH + TILESIZE and location.y <= HEIGHT + TILESIZE:
            if self.pos.distance_to(self.game.player.pos) < DETECT_RADIUS:
                self.can_pursue = True
            else:
                self.can_pursue = False
            self.is_onscreen = True
        else:
            self.is_onscreen = False

    def drop_item(self):
        """
        Drops an item onto the game map where
        this mob dies
        :return: None
        """
        if uniform(0, 1) <= .5:
            WeaponPickup(self.game, self.pos)
        else:
            MiscPickup(self.game, self.pos)

    def follow_path(self):
        target = vec(0, 0)
        if self.current_path_target >= 0:
            target = self.path[self.current_path_target]
            if self.pos.distance_squared_to(target) <= DETECT_RADIUS ** 2:
                self.current_path_target -= 1
        else:
            self.path = None
        return self.seek(target)

    def update(self):
        """
        Update this mob's internal state
        :return: None
        """
        self.check_if_is_on_screen()
        if self.health <= 0:
            if uniform(0, 1) < .015:
                self.drop_item()
            self.kill()
        self.track_prey(self.game.player)
        if (self.pos - self.game.player.pos).length_squared() < DETECT_RADIUS ** 2:
            self.apply_pursuing_behaviour()
        elif self.path != None:
            self.acc += self.follow_path()
            self.apply_flocking_behaviour()
        else:
            if self.is_onscreen:
                self.apply_wandering_behaviour()
        self.acc.scale_to_length(self.seek_force)
        self.vel += self.acc * self.game.dt
        self.vel.scale_to_length(self.speed)
        if self.can_attack:
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_obstacles(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_obstacles(self, self.game.walls, 'y')
        self.rot = self.vel.angle_to(vec(1, 0))
        self.image = pg.transform.rotozoom(self.original_image, self.rot - 90, 1).copy()
        self.rect.center = self.hit_rect.center
        if pg.time.get_ticks() - self.last_attack_time > 750:
            self.can_attack = True

    def draw_health(self):
        """
        Each mob will have their health bars superimposed
        onto their sprite images so as to give the player
        visual indication that they've damaged this sprite
        :return: None
        """
        if self.health > 60:
            color = GREEN
        elif self.health > 30:
            color = YELLOW
        else:
            color = RED
        width = int(self.hit_rect.width * self.health / ENEMY_HEALTH[0])

        self.health_bar = pg.Rect(self.hit_rect.width // 3, 0, width, 7)

        if self.health < ENEMY_HEALTH[0]:
            pg.draw.rect(self.image, color, self.health_bar)
