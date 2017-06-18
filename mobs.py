'''
@author: Ned Austin Datiles
'''

import pygame as pg
from random import choice, uniform
from core_functions import collide_with_obstacles
from settings import *
from sprites import WeaponPickup, MiscPickup
from pathfinding import Pathfinder, WeightedGrid


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
        self.radius = self.rect.width * .7071

        self.speed = choice(ENEMY_SPEEDS)
        self.health = choice(ENEMY_HEALTH)
        self.damage = choice(ENEMY_DAMAGE)
        self.wander_radius = choice(WANDER_RING_RADIUS)

        # Positional, speed, and acceleration vectors
        self.pos = vec(self.rect.center)
        self.vel = vec(0, 0)
        self.acc = vec(self.speed, 0).rotate(uniform(0, 360))
        self.rot = 0
        self.current_rot = 0

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

        print(x, y)
        self.pathfinder = Pathfinder()
        self.game_grid = WeightedGrid()
        self.game_grid.walls = [(int(wall.pos.x // TILESIZE), int(wall.pos.y // TILESIZE)) for wall in game.walls]

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
        self.target = self.pos + self.vel.normalize() * WANDER_RING_DISTANCE
        target = self.target + vec(self.wander_radius, 0).rotate(uniform(0, 360))
        return self.seek(target)

    def pursue(self):
        """
        Gives this mob the ability to
        pursue a target by predicting
        the target's future location
        :return:
        """
        if self.game.player.vel.length() == 0:
            self.target = self.game.player.pos
        else:
            self.target = self.game.player.pos + self.game.player.vel.normalize()
        return self.seek(self.target)  # self.seek_with_approach(self.target)

    def cohesion(self):
        sum = vec(0, 0)
        count = 0
        all_obstacles = [mob for mob in self.game.mobs if mob.is_onscreen]
        for mob in all_obstacles:
            distance = (self.pos - mob.pos).length()
            if 0 < distance < AVOID_RADIUS:
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
            distance = (self.pos - mob.pos).length()
            if 0 < distance < AVOID_RADIUS:
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

    def seperation(self):
        """
        Gives this mob the ability to avoid
        collisions with other obstacles
        :return: None
        """
        all_obstacles = [mob for mob in self.game.mobs if mob.is_onscreen]
        sum = vec(0, 0)
        count = 0
        for mob in all_obstacles:
            distance = (self.pos - mob.pos).length()
            if 0 < distance < AVOID_RADIUS:
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
        pass

    def apply_behaviours(self):
        """
        Applies steering behaviours to the mob
        :return: None
        """
        steering_force = vec(0, 0)
        if not self.can_pursue:
            steering_force = self.wander() + self.seperation() + self.align() + self.cohesion()
        else:
            steering_force = self.pursue() + self.seperation() + self.align() + self.cohesion()
        # steering_force = self.wander() + self.seperation() + self.align() + self.cohesion()
        self.acc += steering_force

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

    def update_mob_locations(self):
        self.game_grid.enemies = [(int(enemy.pos.x // TILESIZE), int(enemy.pos.y // TILESIZE)) for enemy in
                                  self.game.mobs
                                  if enemy != self]

    def update(self):
        """
        Update his mob's internal state
        :return: None
        """
        if self.health <= 0:
            if uniform(0, 1) < .025:
                self.drop_item()
            self.kill()
        self.update_mob_locations()
        self.path = self.pathfinder.a_star_search(self.game_grid,
                                                  vec(self.game.player.pos.x // TILESIZE,
                                                      self.game.player.pos.y // TILESIZE),
                                                  vec(self.pos.x // TILESIZE, self.pos.y // TILESIZE))
        print(len(self.game_grid.enemies))
        # self.check_if_is_on_screen()
        # if self.is_onscreen:
        #     self.apply_behaviours()
        #     self.vel += self.acc * self.game.dt
        #     self.vel.scale_to_length(self.speed)
        #     if self.can_attack:
        #         self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        #         self.hit_rect.centerx = self.pos.x
        #         collide_with_obstacles(self, self.game.walls, 'x')
        #         self.hit_rect.centery = self.pos.y
        #         collide_with_obstacles(self, self.game.walls, 'y')
        #     self.rot = self.vel.angle_to(vec(1, 0))
        #     self.image = pg.transform.rotozoom(self.original_image, self.rot - 90, 1).copy()
        #     self.rect.center = self.hit_rect.center
        #     if pg.time.get_ticks() - self.last_attack_time > 500:
        #         self.can_attack = True

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
