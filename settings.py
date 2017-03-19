'''
@author: Ned Austin Datiles
'''
import pygame as pg
from core_functions import get_image_names
vec = pg.math.Vector2

# Define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Game settings
WIDTH = 1366   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "My game"
BGCOLOR = DARKGREY

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Bullet images
RIFLE_BULLET_IMG = 'rifle_bullet.png'
SHOTGUN_BULLET_IMG = 'shotgun_bullet.png'
HANDGUN_BULLET_IMG = 'handgun_bullet.png'

# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# Effects
MUZZLE_FLASHES = ['smokeparticleassets\\PNG\\Flash\\flash00.png',
                  'smokeparticleassets\\PNG\\Flash\\flash01.png', 
                  'smokeparticleassets\\PNG\\Flash\\flash02.png', 
                  'smokeparticleassets\\PNG\\Flash\\flash03.png', 
                  'smokeparticleassets\\PNG\\Flash\\flash04.png', 
                  'smokeparticleassets\\PNG\\Flash\\flash05.png', 
                  'smokeparticleassets\\PNG\\Flash\\flash06.png', 
                  'smokeparticleassets\\PNG\\Flash\\flash07.png', 
                  'smokeparticleassets\\PNG\\Flash\\flash08.png',  
                  ]
FLASH_DURATION = 45



# Player settings
AIM_OFFSET = 0
DEFAULT_WEAPON = 'knife'
WEAPON_ANIMATION_TIMES = {'handgun': {'idle': 100, 'melee': 50, 'move': 100, 'reload': 50, 'shoot':125},
                          'knife': {'idle': 100, 'melee': 50, 'move': 75, 'reload': 0, 'shoot':0}, 
                          'rifle': {'idle': 100, 'melee': 50, 'move': 125, 'reload': 100, 'shoot':55},
                          'shotgun': {'idle': 100, 'melee': 50, 'move': 125, 'reload': 100, 'shoot':175}}
PLAYER_SPEED = 150
PLAYER_HIT_RECT = pg.Rect(0, 0, 64, 64)
BARREL_OFFSETS = {'handgun': vec(60, 20), 'rifle': vec(80, 20), 'shotgun': vec(80, 20)}

# Weapon settings
WEAPONS = {}
WEAPONS['handgun'] = {'bullet_speed': 2000, 
                    'bullet_lifetime': 1000, 
                    'rate': 300, 
                    'kickback': 50, 
                    'spread': 1,
                    'damage': 10, 
                    'bullet_size': 'med',
                    'bullet_count': 1}

WEAPONS['rifle'] = {'bullet_speed': 2000,
                    'bullet_lifetime': 10000, 
                    'rate': 110, 
                    'kickback': 100, 
                    'spread': 3,
                    'damage': 50, 
                    'bullet_size': 'lg', 
                    'bullet_count': 1}
WEAPONS['shotgun'] = {'bullet_speed': 2000, 
                    'bullet_lifetime': 1000, 
                    'rate': 500, 
                    'kickback': 660, 
                    'spread': 10,
                    'damage': 20, 
                    'bullet_size': 'sm', 
                    'bullet_count': 11}


# Sounds
WEAPON_SOUNDS = {'handgun': ['pistol.wav'],
                'shotgun': ['shotgun.wav']}


# Animations
HANDGUN_ANIMATIONS = {}
KNIFE_ANIMATIONS = {}
RIFLE_ANIMATIONS = {}
SHOTGUN_ANIMATIONS = {}

HANDGUN_ANIMATIONS['idle'] = get_image_names('img\\Player animations\\handgun\\idle\\')
HANDGUN_ANIMATIONS['melee'] = get_image_names('img\\Player animations\\handgun\\meleeattack\\')                         
HANDGUN_ANIMATIONS['move'] = get_image_names('img\\Player animations\\handgun\\move\\')
HANDGUN_ANIMATIONS['reload'] = get_image_names('img\\Player animations\\handgun\\reload\\')
HANDGUN_ANIMATIONS['shoot'] = get_image_names('img\\Player animations\\handgun\\shoot\\')

KNIFE_ANIMATIONS['idle'] = get_image_names("img\\Player animations\\knife\\idle\\")
KNIFE_ANIMATIONS['melee'] = get_image_names("img\\Player animations\\knife\\meleeattack\\")
KNIFE_ANIMATIONS['move'] = get_image_names('img\\Player animations\\knife\\move\\')

RIFLE_ANIMATIONS['idle'] = get_image_names("img\\Player animations\\rifle\\idle\\")
RIFLE_ANIMATIONS['melee'] = get_image_names("img\\Player animations\\rifle\\meleeattack\\")
RIFLE_ANIMATIONS['move'] = get_image_names("img\\Player animations\\rifle\\move\\")
RIFLE_ANIMATIONS['reload'] = get_image_names('img\\Player animations\\rifle\\reload\\')
RIFLE_ANIMATIONS['shoot'] = get_image_names('img\\Player animations\\rifle\\shoot\\')

SHOTGUN_ANIMATIONS['idle'] = get_image_names("img\\Player animations\\shotgun\\idle\\")
SHOTGUN_ANIMATIONS['melee'] = get_image_names("img\\Player animations\\shotgun\\meleeattack\\")
SHOTGUN_ANIMATIONS['move'] = get_image_names("img\\Player animations\\shotgun\\move\\")
SHOTGUN_ANIMATIONS['reload'] = get_image_names('img\\Player animations\\shotgun\\reload\\')
SHOTGUN_ANIMATIONS['shoot'] = get_image_names('img\\Player animations\\shotgun\\shoot\\')