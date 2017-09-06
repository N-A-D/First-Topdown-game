import pygame as pg
from random import choice, uniform, random
from core_functions import collide_with_obstacles
from settings import MOB_LAYER, ENEMY_HIT_RECT, ENEMY_SPEEDS, ENEMY_HEALTH, ENEMY_DAMAGE, WANDER_RING_RADIUS, \
    SEEK_FORCE, WIDTH, HEIGHT, TILESIZE, DETECT_RADIUS, GREEN, RED, YELLOW, vec, WANDER_RING_DISTANCE, \
    ENEMY_LINE_OF_SIGHT, AVOID_RADIUS, APPROACH_RADIUS, ENEMY_ATTACK_RATE, WIDTH
from sprites import Item
from math import sqrt


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

        # Image copies are necessary. The reason being is that
        # if were not for the copy, any damage pasted onto the enemy
        # image would have been replicated onto the other enemies
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
        self._health = self.health
        self.MAX_HEALTH = self.health
        self.damage = choice(ENEMY_DAMAGE)
        self.wander_radius = choice(WANDER_RING_RADIUS)

        # Positional, speed, and acceleration vectors
        self.pos = vec(self.rect.center)
        self.vel = vec(0, 0)
        self.acc = vec(self.speed, 0).rotate(uniform(0, 360))
        self.rot = 0
        self.radius = sqrt(self.hit_rect.width ** 2 + self.hit_rect.height ** 2) / 2
        # How fast this mob is able to track
        # the player
        self.seek_force = choice(SEEK_FORCE) * self.speed
        self.desired = vec(0, 0)
        self.can_attack = True
        self.last_attack_time = 0

        # How often this mob will change targets while wondering
        self.last_target_time = 0
        self.is_onscreen = False
        self.path = None
        self.current_path_target = 0
        self.can_find_path = False

    def track_prey(self, target):
        """
        Gives a mob a path to follow in order for it to track its prey
        :param target: The mob's prey.
        :return:
        """
        if self.can_find_path and not self.path:
            dist = self.pos.distance_to(self.game.player.pos)
            if dist > DETECT_RADIUS * 2 and uniform(0, 1) <= .75:
                self.path = self.game.find_path(self, target)
                if self.path:
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
            self.target = prey.pos
        else:
            self.target = prey.pos + prey.vel.normalize()
        return self.seek(self.target)

    def cohesion(self):
        """
        Cohesion steering behaviour. This steer's a mob towards the
        center of its neighbours.
        :return: Vector2 object to steer towards
        """
        sum = vec(0, 0)
        count = 0
        mobs = [mob for mob in self.game.mobs if mob.is_onscreen]
        for mob in mobs:
            if mob != self:
                dist = self.pos.distance_to(mob.pos)
                if 0 < dist < AVOID_RADIUS:
                    sum += mob.pos
                    count += 1
        if count > 0:
            sum /= count
            if sum.length() == 0:
                return vec(0, 0)
            return self.seek(sum)
        else:
            return vec(0, 0)

    def align(self):
        """
        Alignment steering behaviour. This steer's a mob in the same direction as
        its neighbours.
        :return: Vector2 object to steer towards
        """
        sum = vec(0, 0)
        count = 0
        mobs = [mob for mob in self.game.mobs if mob.is_onscreen]
        for mob in mobs:
            if mob != self:
                dist = self.pos.distance_to(mob.pos)
                if 0 < dist < AVOID_RADIUS:
                    sum += mob.vel
                    count += 1
        if count > 0:
            sum /= count
            if sum.length() == 0:
                return vec(0, 0)
            sum.normalize()
            sum *= self.speed
            steer = sum - self.vel
            steer.scale_to_length(self.seek_force)
            return steer
        else:
            return vec(0, 0)

    def separation(self):
        """
        Gives this mob the ability to avoid
        collisions with other obstacles
        :return: None
        """
        sum = vec(0, 0)
        count = 0
        mobs = [mob for mob in self.game.mobs if mob.is_onscreen]
        for mob in mobs:
            if mob != self:
                dist = self.pos.distance_to(mob.pos)
                if 0 < dist < self.radius * 1.5:
                    diff = self.pos - mob.pos
                    diff.normalize()
                    diff /= dist
                    sum += diff
                    count += 1
        if count > 0:
            sum /= count
            if sum.length() == 0:
                return vec(0, 0)
            sum.normalize()
            sum *= self.speed
            steer = sum - self.vel
            steer.scale_to_length(self.seek_force)
            return steer
        else:
            return vec(0, 0)

    @staticmethod
    def find_collision(obs, ahead, further_ahead, pos):
        """
        Checks to see if there is potential for a collision with
        the observed object.
        :param obs: The object under consideration.
        :param ahead: Secondary line of sight.
        :param further_ahead: Main line of sight.
        :param pos: The mob's position
        :return: True if there is a potential collision False otherwise
        """
        obs_center = vec(obs.rect.center)
        d1 = obs_center.distance_to(ahead)
        d2 = obs_center.distance_to(further_ahead)
        d3 = obs_center.distance_to(pos)
        return (d1 <= obs.radius) or (d2 <= obs.radius) or (d3 <= obs.radius)

    def find_most_threatening_obstacle(self, ahead, further_ahead, pos):
        """
        Finds the most threatening object and returns its position.
        :param ahead: Secondary line of sight
        :param further_ahead: Primary line of sight
        :param pos: mob's position
        :return: Vector2 object containing the location of the most
                threatening obstacle in the mob's path.
        """
        most_threatening = None
        for wall in self.game._walls:
            collide = self.find_collision(wall, ahead, further_ahead, pos)
            if collide and (not most_threatening or self.pos.distance_to(wall.rect.center) < self.pos.distance_to(
                    most_threatening)):
                most_threatening = wall.pos
        return most_threatening

    def obstacle_avoidance(self):
        """
        Gives a mob the ability to avoid obstacles in its path.
        :return: Vector2 object representing the force needed to avoid
                a potential collision.
        """
        if self.vel.length() == 0:
            self.move_from_rest()
        further_ahead = self.pos + self.vel.normalize() * ENEMY_LINE_OF_SIGHT
        ahead = self.pos + self.vel.normalize() * ENEMY_LINE_OF_SIGHT / 2
        most_threatening = self.find_most_threatening_obstacle(ahead, further_ahead, self.pos)
        avoidance_force = vec(0, 0)
        if most_threatening:
            avoidance_force = further_ahead - most_threatening
            avoidance_force.normalize()
            avoidance_force.scale_to_length(self.speed)
        return avoidance_force

    def apply_flocking_behaviour(self):
        """
        Applies flcoking steering behaviours to the mob
        :return: None
        """
        self.acc += self.obstacle_avoidance() * 1.75
        self.acc += self.separation() * 2
        self.acc += self.align()
        self.acc += self.cohesion()

    def apply_pursuing_behaviour(self):
        """
        Allows the mob to pursue the target
        :return:
        """
        self.acc += self.pursue(self.game.player) * 2.75
        self.acc += self.obstacle_avoidance() * 2.5
        self.acc += self.separation() * 2.6
        self.acc += self.align()
        self.acc += self.cohesion()

    def apply_wandering_behaviour(self):
        """
        Gives a mob the ability to wander the around.
        :return:
        """
        self.acc += self.wander()
        self.acc += self.obstacle_avoidance() * 1.75
        self.acc += self.separation() * 2
        self.acc += self.align()
        self.acc += self.cohesion()

    def check_if_is_on_screen(self):
        """
        Used to check if this mob is on the screen or not
        :return: True if on the screen, False otherwise
        """
        location = vec(self.game.camera.apply_rect(self.hit_rect.copy()).topleft)
        if location.x <= WIDTH + TILESIZE and location.y <= HEIGHT + TILESIZE:
            self.is_onscreen = True
        else:
            self.is_onscreen = False

    def drop_item(self):
        """
        Drops an item onto the game map where
        this mob dies
        :return: None
        """
        if uniform(0, 1) < .5:
            Item(self.game, int(self.pos.x), int(self.pos.y), choice(['rifle', 'shotgun', 'handgun']))
        else:
            Item(self.game, int(self.pos.x), int(self.pos.y), choice(['health', 'ammo', 'armour']))

    def follow_path(self):
        """
        Path following algorithm.
        :return:
        """
        if self.current_path_target >= 0:
            target = self.path[self.current_path_target]
            if self.pos.distance_to(target) <= DETECT_RADIUS:
                self.current_path_target -= 1
            return self.seek(target)
        else:
            self.current_path_target = 0
            self.path = None
            return vec(0, 0)

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
            self.game.map_img.blit(self.game._death_splat, self.hit_rect.topleft)
        if self.is_onscreen:
            self.track_prey(self.game.player)
            if self.pos.distance_to(self.game.player.pos) < DETECT_RADIUS:
                if random() < 0.007:
                    snd = choice(self.game.zombie_moan_sounds)
                    if snd.get_num_channels() > 2:
                        snd.stop()
                    snd.play()
                self.apply_pursuing_behaviour()
                self.rot = (self.target - self.pos).angle_to(vec(1, 0))
            elif self.path:
                self.target = self.follow_path()
                self.acc += self.target
                self.apply_flocking_behaviour()
                self.rot = (self.target - self.pos).angle_to(vec(1, 0))
            else:
                if self.is_onscreen:
                    self.apply_wandering_behaviour()
                self.rot = self.vel.angle_to(vec(1, 0))
            self.vel += self.acc * self.game.dt
            self.vel.scale_to_length(self.speed)
            if self.can_attack:
                self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
                self.hit_rect.centerx = self.pos.x
                collide_with_obstacles(self, self.game.all_walls, 'x')
                self.hit_rect.centery = self.pos.y
                collide_with_obstacles(self, self.game.all_walls, 'y')
            self.image = pg.transform.rotozoom(self.original_image, self.rot - 90, 1).copy()
            self.rect.center = self.hit_rect.center
            now = pg.time.get_ticks()
            if now - self.last_attack_time > ENEMY_ATTACK_RATE:
                self.can_attack = True
                self.last_attack_time = now

    def render_health(self):
        """
        Each mob will have their health bars superimposed
        onto their sprite images so as to give the player
        visual indication that they've damaged this sprite
        :return: None
        """
        if self.health > .6 * self.MAX_HEALTH:
            color = GREEN
        elif self.health > .3 * self.MAX_HEALTH:
            color = YELLOW
        else:
            color = RED
        width = int(self.hit_rect.width * self.health / self.MAX_HEALTH)
        self.health_bar = pg.Rect(self.hit_rect.width // 3, 0, width, 7)
        if self.health < self.MAX_HEALTH:
            pg.draw.rect(self.image, color, self.health_bar)