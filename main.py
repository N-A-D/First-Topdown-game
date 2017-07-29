import pygame as pg
import pygame.gfxdraw
import sys
from os import path
from settings import WIDTH, HEIGHT, TITLE, TILESIZE, \
    ITEM_IMAGES, WEAPONS, RIFLE_BULLET_IMG, HANDGUN_BULLET_IMG, SHOTGUN_BULLET_IMG, \
    MUZZLE_FLASHES, ENEMY_IMGS, HANDGUN_ANIMATIONS, KNIFE_ANIMATIONS, RIFLE_ANIMATIONS, \
    SHOTGUN_ANIMATIONS, FPS, LIGHTGREY, WHITE, DARKGREY, RED, GREEN, BLOOD_SHADES, \
    vec, PLAYER_HIT_SOUNDS, ZOMBIE_MOAN_SOUNDS, ENEMY_HIT_SOUNDS, PLAYER_FOOTSTEPS, \
    NIGHT_COLOR, LIGHT_MASK, LIGHT_RADIUS, PLAYER_SWING_NOISES, BG_MUSIC, \
    GAME_OVER_MUSIC, MAIN_MENU_MUSIC, HUD_FONT, TITLE_FONT, BLACK, YELLOW, ORANGE, \
    RIFLE_HUD_IMG, SHOTGUN_HUD_IMG, PISTOL_HUD_IMG, KNIFE_HUD_IMG, DEEPSKYBLUE, ENEMY_KNOCKBACK
from random import choice, randrange, random
from player import Player
from mobs import Mob
from tilemap import Map, Camera, TiledMap
from sprites import Obstacle, WeaponPickup, MiscPickup
from core_functions import collide_hit_rect
from pathfinding import Pathfinder, WeightedGraph


class GameEngine:
    """
    Game objects
    """

    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.pre_init(44100, -16, 1, 1024)
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.HWSURFACE | pg.DOUBLEBUF)
        self.screen.set_alpha(None)
        self.screen_width = WIDTH
        self.screen_height = HEIGHT
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()

        # Resource folders
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'img')
        self.maps_folder = path.join(self.img_folder, 'maps')
        self.snd_folder = path.join(self.game_folder, 'snd')
        self.music_folder = path.join(self.snd_folder, 'Music')
        self.item_folder = path.join(self.img_folder, 'Items')
        self.font_folder = path.join(self.img_folder, 'Fonts')
        self.hud_folder = path.join(self.img_folder, 'HUD')
        # Loads game assets
        self.load_data()

        # Game running flags
        self.running = True
        self.playing = True

        # Debugging flags
        self.debug = False

        # Gameplay flags
        self.hardcore_mode = False
        self.paused = False

        # Menu Flags
        self.on_control_screen = False

    def load_data(self):
        """
        Loads the necessary assets for the game. 
        :return: None
        """
        # Game map
        # self.map = TiledMap(path.join(self.img_folder, 'level1.tmx'))
        # self.map_img = self.map.make_map()
        # self.map_rect = self.map_img.get_rect()
        self.map = Map(path.join(self.game_folder, 'map3.txt'))

        # Dims the pause screen!
        self.pause_screen_effect = pg.Surface(self.screen.get_size()).convert()
        self.pause_screen_effect.fill((0, 0, 0, 225))

        # Fog of war
        self.fog = pg.Surface(self.screen.get_size()).convert()
        self.fog.fill(NIGHT_COLOR)

        # Light on the player
        self.light_mask = pg.image.load(path.join(self.img_folder, LIGHT_MASK)).convert_alpha()
        self.light_mask = pg.transform.smoothscale(self.light_mask, (LIGHT_RADIUS, LIGHT_RADIUS))
        self.light_rect = self.light_mask.get_rect()

        # Item pickups
        self.pickup_items = {}
        for item in ITEM_IMAGES:
            self.pickup_items[item] = []
            self.pickup_items[item] = pg.image.load(path.join(self.item_folder, ITEM_IMAGES[item])).convert_alpha()

        # Fonts
        self.hud_font = path.join(self.font_folder, HUD_FONT)
        self.title_font = path.join(self.font_folder, TITLE_FONT)

        # HUD
        self.hud_images = {'rifle': pg.image.load(path.join(self.hud_folder, RIFLE_HUD_IMG)).convert_alpha(),
                           'shotgun': pg.image.load(path.join(self.hud_folder, SHOTGUN_HUD_IMG)).convert_alpha(),
                           'handgun': pg.image.load(path.join(self.hud_folder, PISTOL_HUD_IMG)).convert_alpha(),
                           'knife': pg.image.load(path.join(self.hud_folder, KNIFE_HUD_IMG)).convert_alpha()
                           }

        # Sound loading
        self.music_tracks = {"main menu": MAIN_MENU_MUSIC, 'Game over': GAME_OVER_MUSIC, 'background music': BG_MUSIC}

        self.swing_noises = {}
        for weapon in PLAYER_SWING_NOISES:
            noise = pg.mixer.Sound(path.join(self.snd_folder, PLAYER_SWING_NOISES[weapon]))
            noise.set_volume(.25)
            self.swing_noises[weapon] = noise

        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pg.mixer.Sound(path.join(self.snd_folder, snd)))

        self.weapon_sounds = {}
        for weapon in WEAPONS['sound']:
            self.weapon_sounds[weapon] = {}
            sound_list = {}
            for snd in WEAPONS['sound'][weapon]:
                noise = pg.mixer.Sound(path.join(self.snd_folder, WEAPONS['sound'][weapon][snd]))
                noise.set_volume(.9)
                sound_list[snd] = noise
            self.weapon_sounds[weapon] = sound_list

        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            noise = pg.mixer.Sound(path.join(self.snd_folder, snd))
            noise.set_volume(.45)
            self.zombie_moan_sounds.append(noise)

        self.zombie_hit_sounds = {}
        for type in ENEMY_HIT_SOUNDS:
            self.zombie_hit_sounds[type] = []
            for snd in ENEMY_HIT_SOUNDS[type]:
                snd = pg.mixer.Sound(path.join(self.snd_folder, snd))
                snd.set_volume(1)
                self.zombie_hit_sounds[type].append(snd)

        self.player_foot_steps = {}
        for terrain in PLAYER_FOOTSTEPS:
            self.player_foot_steps[terrain] = []
            for snd in PLAYER_FOOTSTEPS[terrain]:
                snd = pg.mixer.Sound(path.join(self.snd_folder, snd))
                snd.set_volume(.5)
                self.player_foot_steps[terrain].append(snd)

        # Bullets
        self.bullet_images = {}
        self.bullet_images['lg'] = pg.transform.smoothscale(pg.image.load(path.join(self.img_folder, RIFLE_BULLET_IMG)),
                                                            (10, 3)).convert_alpha()
        self.bullet_images['med'] = pg.transform.smoothscale(
            pg.image.load(path.join(self.img_folder, HANDGUN_BULLET_IMG)), (5, 3)).convert_alpha()
        self.bullet_images['sm'] = pg.transform.smoothscale(pg.image.load(
            path.join(self.img_folder, SHOTGUN_BULLET_IMG)).convert_alpha(), (7, 7))

        # Effects
        self.gun_flashes = [pg.image.load(path.join(self.img_folder, flash)).convert_alpha() for flash in
                            MUZZLE_FLASHES]

        # Load enemy animations
        self.enemy_imgs = [pg.transform.smoothscale(pg.image.load(path.join(self.game_folder, name)),
                                                    (TILESIZE + 20, TILESIZE + 20)).convert_alpha() for name in
                           ENEMY_IMGS]
        # Load player animations
        self.default_player_weapon = 'knife'
        self.default_player_action = 'idle'
        self.player_animations = {'handgun': {}, 'knife': {}, 'rifle': {}, 'shotgun': {}, 'feet': {}}

        # Create all hand gun animations
        self.player_animations['handgun']['idle'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha()
                                                     for name in HANDGUN_ANIMATIONS['idle']]
        self.player_animations['handgun']['melee'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha()
                                                      for name in HANDGUN_ANIMATIONS['melee']]
        self.player_animations['handgun']['move'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha()
                                                     for name in HANDGUN_ANIMATIONS['move']]
        self.player_animations['handgun']['reload'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha()
                                                       for name in HANDGUN_ANIMATIONS['reload']]
        self.player_animations['handgun']['shoot'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha()
                                                      for name in HANDGUN_ANIMATIONS['shoot']]

        # Create all knife animations
        self.player_animations['knife']['idle'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha() for
                                                   name in KNIFE_ANIMATIONS['idle']]
        self.player_animations['knife']['melee'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha() for
                                                    name in KNIFE_ANIMATIONS['melee']]
        self.player_animations['knife']['move'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha() for
                                                   name in KNIFE_ANIMATIONS['move']]

        # Create all rifle animations
        self.player_animations['rifle']['idle'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha() for
                                                   name in RIFLE_ANIMATIONS['idle']]
        self.player_animations['rifle']['melee'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha() for
                                                    name in RIFLE_ANIMATIONS['melee']]
        self.player_animations['rifle']['move'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha() for
                                                   name in RIFLE_ANIMATIONS['move']]
        self.player_animations['rifle']['reload'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha()
                                                     for name in RIFLE_ANIMATIONS['reload']]
        self.player_animations['rifle']['shoot'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha() for
                                                    name in RIFLE_ANIMATIONS['shoot']]

        # Create all shotgun animations
        self.player_animations['shotgun']['idle'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha()
                                                     for name in SHOTGUN_ANIMATIONS['idle']]
        self.player_animations['shotgun']['melee'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha()
                                                      for name in SHOTGUN_ANIMATIONS['melee']]
        self.player_animations['shotgun']['move'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha()
                                                     for name in SHOTGUN_ANIMATIONS['move']]
        self.player_animations['shotgun']['reload'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha()
                                                       for name in SHOTGUN_ANIMATIONS['reload']]
        self.player_animations['shotgun']['shoot'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha()
                                                      for name in SHOTGUN_ANIMATIONS['shoot']]

    def new(self):
        """
        Creates a new game
        :return: None
        """
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.swingAreas = pg.sprite.Group()
        self.camera = Camera(self.map.width, self.map.height)
        self.paused = False
        self.running = True
        self.pathfinder = Pathfinder()
        self.game_graph = WeightedGraph()
        mob_positions = []
        wall_positions = []
        self.game_graph.walls = []
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    wall_positions.append((col * TILESIZE, row * TILESIZE))
                if tile == 'P':
                    self.player = Player(self, col * TILESIZE, row * TILESIZE)
                if tile == 'E':
                    mob_positions.append((col * TILESIZE, row * TILESIZE))
                if tile == 'W':
                    WeaponPickup(self, (col * TILESIZE, row * TILESIZE))

        # self.player = Player(self, 5, 5)

        for position in wall_positions:
            Obstacle(self, position[0], position[1])

        for position in mob_positions:
            Mob(self, position[0], position[1])

        self.game_graph.walls = [(int(wall[0] // TILESIZE), int(wall[1] // TILESIZE)) for wall in wall_positions]
        self.player_curr_pos = self.player.pos
        self.mob_idx = 0
        self.last_queue_update = 0
        self.points = []
        self.intersects = []
        g.run()

    def run(self):
        """
        Runs the game
        :return: None
        """
        self.play_music('background music')
        self.playing = True
        while self.playing:
            pg.display.set_caption("{:.1f}".format(self.clock.get_fps()))
            # Time taken in between frames
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.render()

    def update(self):
        """
        Updates game state
        :return: None
        """
        self.impact_positions = []
        for sprite in self.all_sprites:
            if sprite == self.player:
                sprite.update(pg.key.get_pressed())
            else:
                sprite.update()
        self.camera.update(self.player)
        self.swingAreas.update()
        self.update_pathfinding_queue()

        # Player hits mobs
        hit_melee_box = pg.sprite.groupcollide(self.mobs, self.swingAreas, False, True, collide_hit_rect)
        for hit in hit_melee_box:
            choice(self.zombie_hit_sounds['bash']).play()
            hit.health -= hit.health
            self.impact_positions.append(hit.rect.center)

        # Enemy hits player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        if hits:
            self.player.pos += vec(ENEMY_KNOCKBACK, 0).rotate(-hits[0].rot)
            for hit in hits:
                if random() < .7:
                    choice(self.player_hit_sounds).play()
                if hit.can_attack:
                    self.impact_positions.append(self.player.rect.center)
                    if self.player.has_armour:
                        self.player.armour -= hit.damage
                    else:
                        self.player.health -= hit.damage
                    hit.vel.normalize()
                    hit.pause()
                    if self.player.health <= 0:
                        self.playing = False

        # Bullet collisions
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, False, collide_hit_rect)
        for mob in hits:
            for bullet in hits[mob]:
                self.impact_positions.append(bullet.rect.center)
                mob.health -= bullet.damage
                mob.pos += vec(WEAPONS[self.player.weapon]['damage'] // 10, 0).rotate(-self.player.rot)
            # Drowns out blood gushing noises the further the collision is from the player
            dist = self.player.pos.distance_to(mob.pos)
            ratio = 1
            if dist > 0:
                ratio = round(200 / dist, 2)
                if ratio > 1:
                    ratio = 1
            snd = choice(self.zombie_hit_sounds['bullet'])
            snd.set_volume(ratio)
            if snd.get_num_channels() > 2:
                snd.stop()
            snd.play()

        # Item collisions
        item_collisions = pg.sprite.spritecollide(self.player, self.items, True, collide_hit_rect)
        for item in item_collisions:
            self.player.pickup_item(item)
            if isinstance(item, WeaponPickup):
                snd = self.weapon_sounds[item.type]['pickup']
                snd.play()
            else:
                pass

    def events(self):
        """
        Game loop event handling
        :return: None
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = not self.playing
                self.running = False
                _quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_b:
                    self.debug = not self.debug
                if event.key == pg.K_p:
                    self.paused = not self.paused
                if event.key == pg.K_h:
                    self.hardcore_mode = not self.hardcore_mode
                if event.key == pg.K_c:
                    self.on_control_screen = not self.on_control_screen

    def render(self):
        """
        renders the updated game state onto the screen
        :return: None
        """
        self.screen.fill(DARKGREY)
        # self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        if self.debug:
            self.render_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.debug:
                pg.draw.rect(self.screen, (0, 255, 255), self.camera.apply_rect(sprite.hit_rect), 1)
        self.render_blood_splatters()
        self.render_fog()
        # render hud information
        if not self.hardcore_mode:
            self.render_hud()
        if self.paused:
            self.screen.blit(self.pause_screen_effect, (0, 0))
            self.render_text('Paused', self.title_font, 105, RED, WIDTH / 2, HEIGHT / 2, align='center')
        if self.on_control_screen:
            self.control_screen()
        pg.display.flip()

    def render_grid(self):
        """
        Used for debugging
        :return: None
        """
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def render_fog(self):
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply_rect(self.player.hit_rect.copy()).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_RGB_MULT)

    def render_hud(self):
        """
        Updates the HUD information for the player to see
        :return: None
        """
        x, y = pg.mouse.get_pos()
        pygame.gfxdraw.aacircle(self.screen, x, y,
                                WEAPONS[self.player.weapon]['crosshair radius'], WHITE)
        pygame.gfxdraw.circle(self.screen, x, y, 2, WHITE)
        pg.draw.rect(self.screen, WHITE, pg.Rect(45, HEIGHT - 155, 100, 100), 3)

        if not self.player.has_armour:
            if self.player.health > 75:
                color = GREEN
            elif 50 < self.player.health <= 75:
                color = YELLOW
            elif 25 < self.player.health <= 50:
                color = ORANGE
            else:
                color = RED
        else:
            color = DEEPSKYBLUE
        self.render_text(str(self.player.health) + "%", self.hud_font, 30, color, 50, HEIGHT - 150, align='nw')

        if self.player.stamina > 75:
            color = GREEN
        elif 50 < self.player.stamina <= 75:
            color = YELLOW
        elif 25 < self.player.stamina <= 50:
            color = ORANGE
        else:
            color = RED

        self.render_text("{:.0f}".format(self.player.stamina) + "%", self.hud_font, 30, color, 50, HEIGHT - 125,
                         align='nw')
        if self.player.weapon != 'knife':
            self.render_text(str(self.player.arsenal[self.player.weapon]['clip']) + " - " + \
                             str(self.player.arsenal[self.player.weapon]['reloads'] * \
                                 WEAPONS[self.player.weapon]['clip size']), self.hud_font, 30, WHITE, 50, HEIGHT - 100,
                             'nw')
        else:
            self.render_text("---", self.hud_font, 40, WHITE, 60, HEIGHT - 100)
        self.screen.blit(self.hud_images[self.player.weapon], (120, HEIGHT - 90))

    def render_text(self, text, font_name, size, color, x, y, align='nw'):
        """
        renders informative text.
        :param text: The text to render.
        :param font_name: The font to use.
        :param size: The size of the font.
        :param color: The colour of the font.
        :param x: The x-coordinate of the location
        :param y: The y-coordinate of the location 
        :param align: Compass location
        :return: None
        """
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)

        self.screen.blit(text_surface, text_rect)

    def render_blood_splatters(self):
        if self.impact_positions:
            for pos in self.impact_positions:
                impact = True
                while impact:
                    self.events()
                    for magnitude in range(1, randrange(40, 60)):
                        exploding_bit_x = pos[0] + randrange(-1 * magnitude, magnitude) + self.camera.camera.x
                        exploding_bit_y = pos[1] + randrange(-1 * magnitude, magnitude) + self.camera.camera.y
                        pg.draw.circle(self.screen, choice(BLOOD_SHADES), (exploding_bit_x, exploding_bit_y),
                                       randrange(1, 5))
                    impact = False
            self.impact_positions.clear()

    def find_path(self, predator, prey):
        """
        Finds a path for the predator to reach its prey
        :param predator: The entity who seeks
        :param prey: The unknowning target
        :return: A list of Vector2 objects to guide the predator
        """
        print("Finding path")
        return self.pathfinder.a_star_search(self.game_graph,
                                             vec(predator.pos.x // TILESIZE, predator.pos.y // TILESIZE),
                                             vec(prey.pos.x // TILESIZE, prey.pos.y // TILESIZE))

    def update_pathfinding_queue(self):
        """
        Gives each mob on the level the opportunity to find a path
        to its prey (the player). Each mob will be given this
        opportunity in order according to their list position into
        the mobs group.
        :return: None
        """
        now = pg.time.get_ticks()
        if now - self.last_queue_update > 5000:
            self.last_queue_update = now
            if self.mob_idx == len(self.mobs):
                self.mob_idx = 0
            count = 0
            for mob in self.mobs:
                mob.can_find_path = False
                if count == self.mob_idx:
                    mob.can_find_path = True
                count += 1
            self.mob_idx += 1

    def start_screen(self):
        """
        Displays the start screen for the game
        :return: None
        """
        # self.play_music('main menu')
        self.screen.fill(BLACK)
        self.render_text('The Undead', self.title_font, 150, WHITE, WIDTH / 2, HEIGHT * 1 / 4, align='center')
        self.render_text('Press any key to start', self.title_font, 65, WHITE, WIDTH / 2, HEIGHT * 3 / 4,
                         align='center')
        pg.display.flip()
        self.wait_for_key()

    def control_screen(self, goodluck=False):
        """ Displays the controls to the player. """
        self.screen.fill(BLACK)
        self.render_text('CONTROLS', self.title_font, 50, WHITE, WIDTH / 2, 20, align='center')
        self.render_text('MOVEMENT:', self.title_font, 30, WHITE, WIDTH / 2, 65, align='center')
        self.render_text('Forwards: W', self.title_font, 20, WHITE, WIDTH / 2 + 5, 105, align='center')
        self.render_text('Left: A', self.title_font, 20, WHITE, WIDTH / 2 + 5, 135, align='center')
        self.render_text('Right: S', self.title_font, 20, WHITE, WIDTH / 2 + 5, 165, align='center')
        self.render_text('Backwards: D', self.title_font, 20, WHITE, WIDTH / 2 + 5, 195, align='center')
        self.render_text('Sprint: SPACE', self.title_font, 20, WHITE, WIDTH / 2 + 5, 225, align='center')

        self.render_text('COMBAT:', self.title_font, 30, WHITE, WIDTH / 2, 260, align='center')
        self.render_text('Fire: LMB', self.title_font, 20, WHITE, WIDTH / 2 + 5, 300, align='center')
        self.render_text('Melee: RMB', self.title_font, 20, WHITE, WIDTH / 2 + 5, 330, align='center')
        self.render_text('Reload: R', self.title_font, 20, WHITE, WIDTH / 2 + 5, 360, align='center')

        self.render_text('WEAPON SELECTION:', self.title_font, 30, WHITE, WIDTH / 2, 400, align='center')
        self.render_text('1: Rifle', self.title_font, 20, WHITE, WIDTH / 2, 440, align='center')
        self.render_text('2: Shotgun', self.title_font, 20, WHITE, WIDTH / 2, 470, align='center')
        self.render_text('3: Hand gun', self.title_font, 20, WHITE, WIDTH / 2, 500, align='center')
        self.render_text('4: Knife', self.title_font, 20, WHITE, WIDTH / 2, 530, align='center')
        if goodluck:
            pg.display.flip()
            self.wait_for_key()
            self.screen.fill(BLACK)
            self.render_text('GOODLUCK OUT THERE!', self.title_font, 60, WHITE, WIDTH / 2, HEIGHT / 2, align='center')
            pg.display.flip()
            self.wait_for_key()

    def intro_screen(self):
        """
        Gives an introduction to the game
        """
        pass

    def game_over_screen(self):
        """
        Displays the gameover screen for the game
        :return: None
        """
        self.play_music('Game over')
        self.screen.fill(BLACK)
        self.render_text("You died", self.title_font, 125, RED, WIDTH / 2, HEIGHT * 1 / 4, align='center')
        self.render_text("Better luck next time!", self.title_font, 80, RED, WIDTH / 2, HEIGHT * 2 / 4, align='center')
        self.render_text('Press c key to restart', self.title_font, 65, WHITE, WIDTH / 2, HEIGHT * 3 / 4,
                         align='center')
        pg.display.flip()
        self.wait_for_key(pg.K_c)

    def credit_screen(self):
        """Displays the credits"""
        pass

    def wait_for_key(self, key=None):
        """ Used for transitions between screens"""
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    _quit()
                if event.type == pg.KEYUP:
                    if key and event.key == key:
                        waiting = False
                    else:
                        waiting = False

    def play_music(self, track):
        """
        Plays the given track
        """
        pg.mixer.music.load(path.join(self.music_folder, self.music_tracks[track]))
        pg.mixer.music.set_volume(.5)
        pg.mixer.music.play(loops=-1)


def _quit():
    pg.quit()
    sys.exit()


if __name__ == '__main__':
    g = GameEngine()
    g.start_screen()
    g.control_screen(True)
    g.intro_screen()
    while g.running:
        g.new()
        g.game_over_screen()
    _quit()
