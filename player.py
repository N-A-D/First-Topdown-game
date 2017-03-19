'''
@author: Ned Austin Datiles
'''
import pygame as pg
from core_functions import collide_with_obstacles
from settings import *
from random import uniform, choice
from sprites import Bullet, MuzzleFlash
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites  # So that the player can be drawn
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # Current weapon & action
        self.weapon = self.game.default_player_weapon
        self.action = self.game.default_player_action

        # Current player animations & frame
        self.animations = self.game.player_animations[self.weapon][self.action]
        self.current_frame = 0
        self.last_update = 0
        self.image = self.animations[self.current_frame]
        self.rect = self.image.get_rect()
        # Hit box needed since rotating sprite's will have varying
        # image rectangle sizes
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.last_shot = 0

        # Additional aim shake when moving
        self.aim_wobble = 0

        # Position & speed vector
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos

        self.rot = 0

        self.play_static_animation = False
        self.static_action = ''

    def handle_controls(self):
        self.rot = 0
        self.vel = vec(0, 0)
        self.action = 'idle'
        self.aim_wobble = 0
        keys = pg.key.get_pressed()

        self.update_direction()
        # Handle player movement Walking & Running

        # Handle combat controls
        if keys[pg.K_r] and self.weapon != 'knife':
            self.action = 'reload'
            self.static_action = self.action
            self.current_frame = 0
            self.play_static_animation = True
        elif keys[pg.K_f]:
            self.action = 'melee'
            self.current_frame = 0
            self.static_action = self.action
            self.play_static_animation = True

        if keys[pg.K_a] and keys[pg.K_SPACE]:
            self.vel.x = -PLAYER_SPEED * 2
            self.action = 'move'
            self.aim_wobble = 15
        elif keys[pg.K_a] and not keys[pg.K_SPACE]:
            self.vel.x = -PLAYER_SPEED
            self.action = 'move'
        if keys[pg.K_d] and keys[pg.K_SPACE]:
            self.vel.x = PLAYER_SPEED * 2
            self.action = 'move'
            self.aim_wobble = 15
        elif keys[pg.K_d] and not keys[pg.K_SPACE]:
            self.vel.x = PLAYER_SPEED
            self.action = 'move'
        if keys[pg.K_w] and keys[pg.K_SPACE]:
            self.vel.y = -PLAYER_SPEED * 2
            self.action = 'move'
            self.aim_wobble = 15
        elif keys[pg.K_w] and not keys[pg.K_SPACE]:
            self.vel.y = -PLAYER_SPEED
            self.action = 'move'
        if keys[pg.K_s] and keys[pg.K_SPACE]:
            self.vel.y = PLAYER_SPEED * 2
            self.action = 'move'
            self.aim_wobble = 15
        elif keys[pg.K_s] and not keys[pg.K_SPACE]:
            self.vel.y = PLAYER_SPEED
            self.action = 'move'

        if not self.play_static_animation:
            # Handle player weapon selection
            if keys[pg.K_1]:
                self.current_frame = 0
                self.weapon = 'rifle'
            elif keys[pg.K_2]:
                self.current_frame = 0
                self.weapon = 'shotgun'
            elif keys[pg.K_3]:
                self.current_frame = 0
                self.weapon = 'handgun'
            elif keys[pg.K_4]:
                self.current_frame = 0
                self.weapon = 'knife'

        # Handle mouse clicks
        lc, _, _ = pg.mouse.get_pressed()
        if lc and not self.weapon == 'knife':
            self.action = 'shoot'
            self.shoot()

        # Handles too fast diagonal movement
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > WEAPONS[self.weapon]['rate']:
            self.last_shot = now
            direction = vec(1, 0).rotate(-self.rot)
            pos = self.pos + BARREL_OFFSETS[self.weapon].rotate(-self.rot)
            self.vel = vec(-WEAPONS[self.weapon]['kickback'], 0).rotate(-self.rot)
            for _ in range(WEAPONS[self.weapon]['bullet_count']):
                spread = uniform(-WEAPONS[self.weapon]['spread'] - self.aim_wobble,
                                 WEAPONS[self.weapon]['spread'] + self.aim_wobble)
                Bullet(self.game, pos, direction.rotate(spread), WEAPONS[self.weapon]['damage'])
                snd = choice(self.game.weapon_sounds[self.weapon])
                if snd.get_num_channels() > 2:
                    snd.stop()
                snd.play()
            MuzzleFlash(self.game, pos)

    def animate_old(self):
        now = pg.time.get_ticks()
        self.animations = self.game.player_animations[self.weapon][self.action]
        self.current_frame %= len(self.animations)
        if now - self.last_update > WEAPON_ANIMATION_TIMES[self.weapon][self.action]:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.animations)
        self.image = pg.transform.rotozoom(self.animations[self.current_frame], self.rot, 1)
        self.rect = self.image.get_rect()

    def animate(self):
        now = pg.time.get_ticks()
        if not self.play_static_animation:
            self.animations = self.game.player_animations[self.weapon][self.action]
            self.current_frame %= len(self.animations)
            if now - self.last_update > WEAPON_ANIMATION_TIMES[self.weapon][self.action]:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.animations)
            self.image = pg.transform.rotozoom(self.animations[self.current_frame], self.rot, 1)
            self.rect = self.image.get_rect()
        else:
            self.animations = self.game.player_animations[self.weapon][self.static_action]
            if now - self.last_update > WEAPON_ANIMATION_TIMES[self.weapon][self.static_action]:
                self.last_update = now
                self.current_frame += 1
                try:
                    self.image = pg.transform.rotozoom(self.animations[self.current_frame], self.rot, 1)
                    self.rect = self.image.get_rect()
                except IndexError:
                    self.play_static_animation = False
                    self.static_action = ''
                    self.current_frame = 0

    def update_direction(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        self.mouse_vec = vec(mouse_x, mouse_y)
        # Mouse location is relative to the top left 
        # corner of the window. Updates it so that
        # its relative to the top-left of the camera
        self.mouse_vec.x -= self.game.camera.camera.x
        self.mouse_vec.y -= self.game.camera.camera.y
        target_dist = self.mouse_vec - self.pos
        self.rot = target_dist.angle_to(vec(1, 0))
        self.rot += 3

    def update(self):
        self.handle_controls()
        self.animate()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_obstacles(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_obstacles(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center