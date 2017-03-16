'''
Created on Mar 15, 2017

@author: Austin
'''
import pygame as pg
from os import path
from settings import *
from player import Player
from tilemap import Map, Camera
from sprites import Obstacle

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        # Resource folders
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'img')
        
        self.load_data()
        self.running = True
    
    def load_data(self):
        # Game map
        self.map = Map(path.join(self.game_folder, 'map.txt'))
        self.bullet_images = {}
        self.bullet_images['lg'] = pg.transform.smoothscale(pg.image.load(path.join(self.img_folder, RIFLE_BULLET_IMG)), (7, 2))
        self.bullet_images['sm'] = pg.transform.smoothscale(pg.image.load(path.join(self.img_folder, SHOTGUN_BULLET_IMG)), (3, 3))
        
        # 
        
        # Load player animations
        self.default_player_weapon = 'knife'
        self.default_player_action = 'idle'
        
        self.player_animations = {'handgun': {}, 'knife': {}, 'rifle': {}, 'shotgun': {}}
        # Create all hand gun images
        self.player_animations['handgun']['idle'] = [pg.image.load(path.join(self.img_folder, name)).convert_alpha() for name in HANDGUN_ANIMATIONS['idle']]
        self.player_animations['handgun']['melee'] = [pg.image.load(path.join(self.img_folder, name)).convert_alpha() for name in HANDGUN_ANIMATIONS['melee']]
        self.player_animations['handgun']['move'] = [pg.image.load(path.join(self.img_folder, name)).convert_alpha() for name in HANDGUN_ANIMATIONS['move']]
        self.player_animations['handgun']['reload'] = [pg.image.load(path.join(self.img_folder, name)).convert_alpha() for name in HANDGUN_ANIMATIONS['reload']]
        self.player_animations['handgun']['shoot'] = [pg.image.load(path.join(self.img_folder, name)).convert_alpha() for name in HANDGUN_ANIMATIONS['shoot']]
        
        # Create all knife images
        self.player_animations['knife']['idle'] = [pg.image.load(path.join(self.img_folder, name)).convert_alpha() for name in KNIFE_ANIMATIONS['idle']]
        self.player_animations['knife']['melee'] = [pg.image.load(path.join(self.img_folder, name)).convert_alpha() for name in KNIFE_ANIMATIONS['melee']]
        self.player_animations['knife']['move'] = [pg.image.load(path.join(self.img_folder, name)).convert_alpha() for name in KNIFE_ANIMATIONS['move']]
        
        # Create all rifle images
        self.player_animations['rifle']['idle'] = [pg.image.load(path.join(self.img_folder, name)).convert_alpha() for name in RIFLE_ANIMATIONS['idle'] ]
        self.player_animations['rifle']['melee'] = [pg.image.load(path.join(self.img_folder, name)).convert_alpha() for name in RIFLE_ANIMATIONS['melee']]
        self.player_animations['rifle']['move'] = [pg.image.load(path.join(self.img_folder, name)).convert_alpha() for name in RIFLE_ANIMATIONS['move']]
        self.player_animations['rifle']['reload'] = [pg.image.load(path.join(self.img_folder, name)).convert_alpha() for name in RIFLE_ANIMATIONS['reload']]
        self.player_animations['rifle']['shoot'] = [pg.image.load(path.join(self.img_folder, name)).convert_alpha() for name in RIFLE_ANIMATIONS['shoot']]
        
        # Create all shotgun images
        self.player_animations['shotgun']['idle'] = [pg.image.load(path.join(self.img_folder, name)).convert_alpha() for name in SHOTGUN_ANIMATIONS['idle']]
        self.player_animations['shotgun']['melee'] = [pg.image.load(path.join(self.img_folder, name)).convert_alpha() for name in SHOTGUN_ANIMATIONS['melee']]
        self.player_animations['shotgun']['move'] = [pg.image.load(path.join(self.img_folder, name)).convert_alpha() for name in SHOTGUN_ANIMATIONS['move']]
        self.player_animations['shotgun']['reload'] = [pg.image.load(path.join(self.img_folder, name)).convert_alpha() for name in SHOTGUN_ANIMATIONS['reload']]
        self.player_animations['shotgun']['shoot'] = [pg.image.load(path.join(self.img_folder, name)).convert_alpha() for name in SHOTGUN_ANIMATIONS['shoot']]
        
    def new(self):
        # Starts a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Obstacle(self, col, row, TILESIZE, TILESIZE)
                if tile == 'P':
                    self.player = Player(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)
        g.run()

    def run(self):
        # Game loop
        self.playing = True
        while self.playing:
            pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
        
    def update(self):
        # Game loop - update
        self.all_sprites.update()
        self.camera.update(self.player)
        
    def events(self):
        # Game loop - events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
            
    def draw(self):
        # Game loop - draw
        self.screen.fill(BLACK)
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()
      
    def show_start_screen(self):
        # game splash screen/start screen
        pass
        
    def show_gameover_screen(self):
        # game over screen
        pass
        
g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_gameover_screen()
    
pg.quit()