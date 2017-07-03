'''
@author: Ned Austin Datiles
'''
import pygame as pg
from core_functions import collide_with_obstacles
from settings import PLAYER_LAYER, PLAYER_HEALTH, PLAYER_STAMINA, PLAYER_HIT_RECT, vec, WEAPONS, PLAYER_SPEED
from random import uniform
from sprites import Bullet, MuzzleFlash
from sprites import WeaponPickup, SwingArea
from random import choice


class Player(pg.sprite.Sprite):
    """
    This class represents a player object in the game
    and its various attributes and abilities
    """

    def __init__(self, game, x, y):
        """
        Initializes a player object for use within the game.
        :param game: The game object the player belongs to
        :param x: x coordinate of the player's location
        :param y: y coordinate of the player's location
        """
        # When the player's sprite will be drawn.
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # Player's physical attributes
        self.health = PLAYER_HEALTH
        self.stamina = PLAYER_STAMINA

        # Used to identify when to decrease the player's stamina
        self.stamina_decrease_time = 0
        # Used to identify when to increase the player's stamina
        self.stamina_increase_time = 0

        # Current weapon & action
        self.weapon = self.game.default_player_weapon
        self.action = self.game.default_player_action

        # Houses the player's arsenal characteristics
        self.arsenal = {'handgun': {'clip': 0, 'reloads': 0, 'hasWeapon': False},
                        'rifle': {'clip': 0, 'reloads': 0, 'hasWeapon': False},
                        'shotgun': {'clip': 0, 'reloads': 0, 'hasWeapon': False},
                        'knife': {'hasWeapon': True}
                        }

        # Current player animation & frame
        self.animations = self.game.player_animations[self.weapon][self.action]
        self.current_frame = 0
        self.last_update = 0
        # Set the current frame to the first in the queue
        self.image = self.animations[self.current_frame]
        self.rect = self.image.get_rect()

        # Secondary rectangle is needed since rotating rectangles warps it.
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center

        # Paces the player's shots
        self.last_shot = 0

        # Adds weapon sway while moving which contributes to poorer accuracy
        self.aim_wobble = 0

        # Positional and velocity vectors
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rect.center = self.pos

        # Player rotation
        self.rot = 0

        # Forces all melee or reload animation frames to be used at most
        # once before returning back to regular action
        self.play_static_animation = False
        # Either reload or melee
        self.canned_action = ''

        # The direction the player is facing
        self.direction = 'E'

        self.step_sounds = None
        self.current_step_sound = 0
        self.last_step_time = 0

    def decrease_stamina(self, decrease_rate):
        """
        Decreases the player's stamina
        :param decrease_rate: The amount to decrease the player's stamina by
        :return: None
        """
        now = pg.time.get_ticks()
        if now - self.stamina_decrease_time > 75:
            self.stamina -= decrease_rate
            self.stamina_decrease_time = now
            if self.stamina < 0:
                self.stamina = 0

    def increase_stamina(self, increase_rate):
        """
        Increases the player's stamina
        :param increase_rate: The amount to increase the player's stamina by
        :return: None
        """
        if self.stamina < 100:
            now = pg.time.get_ticks()
            if now - self.stamina_increase_time > 250:
                self.stamina += increase_rate
                self.stamina_increase_time = now
        else:
            self.stamina = 100

    def shoot(self):
        """
        Fires a bullet from the muzzle of the player's weapon
        :return: None
        """
        now = pg.time.get_ticks()
        if now - self.last_shot > WEAPONS[self.weapon]['rate']:
            self.last_shot = now
            direction = vec(1, 0).rotate(-self.rot)
            pos = self.pos + WEAPONS[self.weapon]['barrel offset'].rotate(-self.rot)
            self.vel = vec(-WEAPONS[self.weapon]['kickback'], 0).rotate(-self.rot)

            for _ in range(WEAPONS[self.weapon]['bullet_count']):
                spread = uniform(-WEAPONS[self.weapon]['spread'] - self.aim_wobble,
                                 WEAPONS[self.weapon]['spread'] + self.aim_wobble)
                Bullet(self.game, pos, direction.rotate(spread), WEAPONS[self.weapon]['damage'])
                snd = self.game.weapon_sounds[self.weapon]['attack']
                if snd.get_num_channels() > 2:
                    snd.stop()
                snd.play()

            MuzzleFlash(self.game, pos)
            self.arsenal[self.weapon]['clip'] -= 1

    def reload(self):
        """
        Reload's the player's weapon magazine
        :return: 
        """
        self.arsenal[self.weapon]['reloads'] -= 1
        self.arsenal[self.weapon]['clip'] = WEAPONS[self.weapon]['clip size']
        self.action = 'reload'
        self.canned_action = self.action
        self.current_frame = 0
        self.play_static_animation = True
        self.game.weapon_sounds[self.weapon]['reload'].play()

    def process_input(self, _input):
        """
        Processes keyboard inputs relevant to the player's character
        :param _input: The list of input keys
        :return:
        """
        self.rot = 0
        self.vel = vec(0, 0)
        self.action = 'idle'
        self.aim_wobble = 0
        self.update_rotation()
        self.handle_player_movement(keys=_input)
        if not self.play_static_animation:
            self.handle_weapon_selection(keys=_input)
            self.handle_combat_controls(keys=_input)

        # Accommodates for diagonal movement being slightly faster than pure horizontal or vertical movement
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
        if self.action == 'idle':
            self.aim_wobble = WEAPONS[self.weapon]['wobble']['idle']
            self.increase_stamina(1 / WEAPONS[self.weapon]['weight'])

    def handle_combat_controls(self, keys):
        """
        Processes any combat related key pressed

        Left mouse click --> shoot
        Right mouse click --> butt stroke
        R (r key) --> reload
        :param keys: The list of keys pressed
        :return: None
        """
        lc, _, rc = pg.mouse.get_pressed()
        if lc and not self.weapon == 'knife':
            if self.arsenal[self.weapon]['clip'] != 0:
                self.action = 'shoot'
                self.shoot()
            else:
                if self.arsenal[self.weapon]['reloads'] > 0:
                    if not self.play_static_animation:
                        self.reload()

        if keys[pg.K_r] and self.weapon != 'knife' and self.action != 'reload':
            if self.arsenal[self.weapon]['reloads'] > 0:
                self.reload()

        if rc and self.action != 'reload' and self.stamina > 0:
            self.game.swing_noises[self.weapon].play()
            self.action = 'melee'
            self.current_frame = 0
            self.canned_action = self.action
            self.play_static_animation = True
            self.decrease_stamina(WEAPONS[self.weapon]['weight'])

            # Find the area where the player is
            # swinging their weapon and create
            # a hit box to collide with any
            # enemy in the vicinity
            self.swing_weapon()

    def handle_weapon_selection(self, keys):
        """
        Update's the player's current weapon to whichever
        he/she chooses if they have that weapon
        :param keys: The list of keys pressed
        :return: None
        """
        if keys[pg.K_1] and self.arsenal['rifle']['hasWeapon'] and not self.weapon == 'rifle':
            self.current_frame = 0
            self.weapon = 'rifle'
        elif keys[pg.K_2] and self.arsenal['shotgun']['hasWeapon'] and not self.weapon == 'shotgun':
            self.current_frame = 0
            self.weapon = 'shotgun'
        elif keys[pg.K_3] and self.arsenal['handgun']['hasWeapon'] and not self.weapon == 'handgun':
            self.current_frame = 0
            self.weapon = 'handgun'
        # Player always has a knife
        elif keys[pg.K_4] and not self.weapon == 'knife':
            self.current_frame = 0
            self.weapon = 'knife'
            self.game.weapon_sounds[self.weapon]['draw'].play()

    def play_foot_step_sounds(self, sprinting, terrain='dirt'):
        """
        Plays the sound a foot step would make on a given terrain
        :param sprinting: If the player is sprinting, the step sounds are more frequent.
        :param terrain: The type of surface the player is moving on.
        :return: None
        """
        now = pg.time.get_ticks()
        self.step_sounds = self.game.player_foot_steps[terrain]
        if sprinting:
            self.current_step_sound %= len(self.step_sounds)
            if now - self.last_step_time > 300:
                self.last_step_time = now
                self.current_step_sound = (self.current_step_sound + 1) % len(self.step_sounds)
                snd = self.step_sounds[self.current_step_sound]
                if snd.get_num_channels() > 2:
                    snd.stop()
                snd.play()
        else:
            self.current_step_sound %= len(self.step_sounds)
            if now - self.last_step_time > 750:
                self.last_step_time = now
                self.current_step_sound = (self.current_step_sound + 1) % len(self.step_sounds)
                snd = self.step_sounds[self.current_step_sound]
                if snd.get_num_channels() > 2:
                    snd.stop()
                snd.play()

    def handle_player_movement(self, keys):
        """
        Updates the player's velocity such that the player
        can move in the game map
        :param keys: The list of keys pressed
        :return: None
        """
        is_sprinting = False
        if keys[pg.K_SPACE] and self.stamina > 0:
            is_sprinting = True
            if keys[pg.K_a]:
                self.vel.x = -PLAYER_SPEED * 2
                self.action = 'move'
                self.aim_wobble = WEAPONS[self.weapon]['wobble']['sprint']
                self.decrease_stamina(WEAPONS[self.weapon]['weight'] / 2)
            if keys[pg.K_d]:
                self.vel.x = PLAYER_SPEED * 2
                self.action = 'move'
                self.aim_wobble = WEAPONS[self.weapon]['wobble']['sprint']
                self.decrease_stamina(WEAPONS[self.weapon]['weight'] / 2)
            if keys[pg.K_w]:
                self.vel.y = -PLAYER_SPEED * 2
                self.action = 'move'
                self.aim_wobble = WEAPONS[self.weapon]['wobble']['sprint']
                self.decrease_stamina(WEAPONS[self.weapon]['weight'] / 2)
            if keys[pg.K_s]:
                self.vel.y = PLAYER_SPEED * 2
                self.action = 'move'
                self.aim_wobble = WEAPONS[self.weapon]['wobble']['sprint']
                self.decrease_stamina(WEAPONS[self.weapon]['weight'] / 2)
        else:
            if keys[pg.K_a]:
                self.vel.x = -PLAYER_SPEED * 1
                self.action = 'move'
                self.aim_wobble = WEAPONS[self.weapon]['wobble']['walk']
                self.increase_stamina(1 / WEAPONS[self.weapon]['weight'])
            if keys[pg.K_d]:
                self.vel.x = PLAYER_SPEED * 1
                self.action = 'move'
                self.aim_wobble = WEAPONS[self.weapon]['wobble']['walk']
                self.increase_stamina(1 / WEAPONS[self.weapon]['weight'])
            if keys[pg.K_w]:
                self.vel.y = -PLAYER_SPEED * 1
                self.action = 'move'
                self.aim_wobble = WEAPONS[self.weapon]['wobble']['walk']
                self.increase_stamina(1 / WEAPONS[self.weapon]['weight'])
            if keys[pg.K_s]:
                self.vel.y = PLAYER_SPEED * 1
                self.action = 'move'
                self.aim_wobble = WEAPONS[self.weapon]['wobble']['walk']
                self.increase_stamina(1 / WEAPONS[self.weapon]['weight'])

        if self.vel.length() != 0:
            self.play_foot_step_sounds(sprinting=is_sprinting)
        else:
            self.current_step_sound = 0

    def swing_weapon(self):
        """
        Creates a zone which damages any enemy caught in it
        :return: None
        """
        if self.direction == 'E':
            self.game.swingAreas.add(SwingArea(self.game, self.hit_rect.midright, self.direction))
        elif self.direction == 'NE':
            self.game.swingAreas.add(SwingArea(self.game, self.hit_rect.topright, self.direction))
        elif self.direction == 'N':
            self.game.swingAreas.add(SwingArea(self.game, self.hit_rect.midtop, self.direction))
        elif self.direction == 'NW':
            self.game.swingAreas.add(SwingArea(self.game, self.hit_rect.topleft, self.direction))
        elif self.direction == 'W':
            self.game.swingAreas.add(SwingArea(self.game, self.hit_rect.midleft, self.direction))
        elif self.direction == 'SW':
            self.game.swingAreas.add(SwingArea(self.game, self.hit_rect.bottomleft, self.direction))
        elif self.direction == 'S':
            self.game.swingAreas.add(SwingArea(self.game, self.hit_rect.midbottom, self.direction))
        elif self.direction == 'SE':
            self.game.swingAreas.add(SwingArea(self.game, self.hit_rect.bottomright, self.direction))

    def animate(self):
        """
        Switches the player's current animation frame to the next
        :return: None
        """
        now = pg.time.get_ticks()
        # if the player is not swinging their weapon or reloading
        if not self.play_static_animation:
            self.animations = self.game.player_animations[self.weapon][self.action]
            self.current_frame %= len(self.animations)
            if now - self.last_update > WEAPONS['animation times'][self.weapon][self.action]:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.animations)
            self.image = pg.transform.rotozoom(self.animations[self.current_frame], self.rot, 1)
            self.rect = self.image.get_rect()
        else:
            self.animations = self.game.player_animations[self.weapon][self.canned_action]
            if now - self.last_update > WEAPONS['animation times'][self.weapon][self.canned_action]:
                self.last_update = now
                self.current_frame += 1
                # Keep the player in the reload or melee animation
                # until all of the frames for that specific action
                # have been used up.
                try:
                    self.image = pg.transform.rotozoom(self.animations[self.current_frame], self.rot, 1)
                    self.rect = self.image.get_rect()
                except IndexError:
                    self.play_static_animation = False
                    self.canned_action = ''
                    self.current_frame = 0

    def pickup_item(self, item):
        """
        Adds the item to the player's belongings
        :param item: the item to add
        :return: None
        """
        if isinstance(item, WeaponPickup):
            if self.arsenal[item.type]['hasWeapon']:
                self.arsenal[item.type]['reloads'] += item.ammo_boost
            else:
                self.arsenal[item.type]['hasWeapon'] = True
                self.arsenal[item.type]['reloads'] = item.ammo_boost - 1
                self.arsenal[item.type]['clip'] = WEAPONS[item.type]['clip size']
        else:
            if item.type == 'ammo':
                if self.weapon == 'knife':
                    keys = ['rifle', 'shotgun', 'handgun']
                    firearm = choice(keys)
                    self.arsenal[firearm]['reloads'] += item.AMMO_BOOST

                else:
                    self.arsenal[self.weapon]['reloads'] += item.AMMO_BOOST
            else:
                if self.health + item.HEALTH_BOOST > PLAYER_HEALTH:
                    self.health = PLAYER_HEALTH
                else:
                    self.health += item.HEALTH_BOOST

    def update_rotation(self):
        """
        Finds the angle to rotate the player sprite by
        according to the mouse's location
        :return: None
        """
        mouse_vec = vec(pg.mouse.get_pos())
        # Mouse location is relative to the top left 
        # corner of the window. This method modifies
        # the mouse's location so that its relative
        # to the top-left of the camera
        mouse_vec.x -= self.game.camera.camera.x
        mouse_vec.y -= self.game.camera.camera.y
        target_dist = mouse_vec - self.pos
        self.rot = target_dist.angle_to(vec(1, 0)) + 2
        self.update_direction()

    def update_direction(self):
        """
         Finds the compass direction from the player's
         current rotation. 
         Directions are given as a range
         E: (-22.5, 22.5)
         NE: (22.5, 67.5)
         N: (67.5, 112.5)
         NW: (112.5, 157.5)
         W: (157.5, 180) and (-180, -157.5)
         SW: (-157.5, -112.5)
         S: (-112.5, -67.5)
         SE: (-67.5, -22.5)
        :return: None
        """
        if -22.5 < self.rot <= 22.5:
            self.direction = 'E'
        elif 22.5 < self.rot <= 67.5:
            self.direction = 'NE'
        elif 67.5 < self.rot <= 112.5:
            self.direction = 'N'
        elif 112.5 < self.rot <= 157.5:
            self.direction = 'NW'
        elif 157.5 < self.rot <= 180 or -180 < self.rot <= -157.5:
            self.direction = 'W'
        elif -157.5 < self.rot <= -112.5:
            self.direction = 'SW'
        elif -112.5 < self.rot <= -67.5:
            self.direction = 'S'
        elif -67.5 < self.rot <= -22.5:
            self.direction = 'SE'

    def update(self, keyboard_input):
        """
        Updates the player character.
        :param keyboard_input: The list of keyboard inputs given.
        :return: None
        """
        self.process_input(keyboard_input)
        self.animate()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_obstacles(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_obstacles(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
