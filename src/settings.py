import pygame as pg
from core_functions import get_image_names

vec = pg.math.Vector2

# GAME LEVELS
GAME_LEVELS = [
    'Apartments1.tmx',
]

# Define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
DARKRED = (139, 0, 0)
YELLOW = (255, 255, 0)
SANDYBROWN = (244, 164, 96)
DEEPSKYBLUE = (0, 191, 255)
DODGERBLUE = (30, 144, 255)
LIMEGREEN = (50, 205, 50)
GOLD = (255, 215, 0)
NIGHT_COLOR = (20, 20, 20)
LIGHTSLATEGREY = (119, 136, 153, 127)
ORANGE = (255, 165, 0)

# Game settings
WIDTH = 896  # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 512  # 16 * 48 or 32 * 24 or 64 * 12

FPS = 60
TITLE = "The Evil Dead"
BGCOLOR = DARKGREY

TILESIZE = 64
GRIDWIDTH = 32
GRIDHEIGHT = 24

# Fonts
HUD_FONT = 'kenpixel_high_square.ttf'
TITLE_FONT = 'kenpixel_high.ttf'

# HUD
RIFLE_HUD_IMG = 'rifle.png'
SHOTGUN_HUD_IMG = 'shotgun.png'
PISTOL_HUD_IMG = 'pistol.png'
KNIFE_HUD_IMG = 'knife.png'
GAME_ICON = 'Game_icon.png'

# Bullet images
RIFLE_BULLET_IMG = 'Bullets/rifle_bullet.png'
SHOTGUN_BULLET_IMG = 'Bullets/shotgun_bullet.png'
HANDGUN_BULLET_IMG = 'Bullets/handgun_bullet.png'

# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# Effects
MUZZLE_FLASHES = ['smokeparticleassets/PNG/Flash/flash00.png',
                  'smokeparticleassets/PNG/Flash/flash01.png',
                  'smokeparticleassets/PNG/Flash/flash02.png',
                  'smokeparticleassets/PNG/Flash/flash03.png',
                  'smokeparticleassets/PNG/Flash/flash04.png',
                  'smokeparticleassets/PNG/Flash/flash05.png',
                  'smokeparticleassets/PNG/Flash/flash06.png',
                  'smokeparticleassets/PNG/Flash/flash07.png',
                  'smokeparticleassets/PNG/Flash/flash08.png',
                  ]
FLASH_DURATION = 60
LASER_SIGHT_COLORS = [(124, 252, 0), (50, 205, 50), (173, 255, 47), (152, 251, 152), (34, 139, 34)]
LIGHT_MASK = 'light_falloff100.png'  #
LIGHT_RADIUS = 550
BLOOD_SHADES = [(value, 0, 0) for value in range(255, 16, -8)]
BLOOD_SPLAT = 'Blood/splat red.png'
BG_MUSIC = 'Infested City.ogg'
GAME_OVER_MUSIC = 'Death is Just Another Path.ogg'
MAIN_MENU_MUSIC = 'zombie main music.ogg'

# Item settings
BOB_RANGE = 20
BOB_SPEED = .5

# Player settings
SPRINT_BOOST = 2.25
DEFAULT_WEAPON = 'knife'
PLAYER_SPEED = 150
PLAYER_HIT_RECT = pg.Rect(0, 0, 50, 50)
PLAYER_MELEE_RECTS = {
    'knife': pg.Rect(0, 0, 50, 50),
    'handgun': pg.Rect(0, 0, 50, 50),
    'rifle': pg.Rect(0, 0, 64, 64),
    'shotgun': pg.Rect(0, 0, 64, 64)
}
PLAYER_HEALTH = 100
PLAYER_STAMINA = 100
PLAYER_MELEE_STUMBLE = 100
PLAYER_HIT_SOUNDS = ['Player/Pain/8.wav', 'Player/Pain/9.wav', 'Player/Pain/10.wav',
                     'Player/Pain/11.wav', 'Player/Pain/12.wav', 'Player/Pain/13.wav',
                     'Player/Pain/14.wav']
PLAYER_SWING_NOISES = {
    'handgun': 'Player/Bash/Handgun swing.ogg',
    'rifle': 'Player/Bash/Temp Swing.ogg',
    'shotgun': 'Player/Bash/Temp Swing.ogg',
    'knife': 'Player/Bash/Knife swing.ogg'}

PLAYER_FOOTSTEPS = {'dirt': [
    'Player/Footsteps/Dirt/stepdirt_1.ogg',
    'Player/Footsteps/Dirt/stepdirt_2.ogg',
    'Player/Footsteps/Dirt/stepdirt_3.ogg',
    'Player/Footsteps/Dirt/stepdirt_4.ogg',
    'Player/Footsteps/Dirt/stepdirt_5.ogg',
    'Player/Footsteps/Dirt/stepdirt_6.ogg',
    'Player/Footsteps/Dirt/stepdirt_7.ogg',
    'Player/Footsteps/Dirt/stepdirt_8.ogg',
],
    'snow': [
        'Player/Footsteps/Snow/stepsnow_1.ogg',
        'Player/Footsteps/Snow/stepsnow_2.ogg'
    ],
    'stone': [
        'Player/Footsteps/Stone/stepstone_1.ogg',
        'Player/Footsteps/Stone/stepstone_2.ogg',
        'Player/Footsteps/Stone/stepstone_3.ogg',
        'Player/Footsteps/Stone/stepstone_4.ogg',
        'Player/Footsteps/Stone/stepstone_5.ogg',
        'Player/Footsteps/Stone/stepstone_6.ogg',
        'Player/Footsteps/Stone/stepstone_7.ogg',
        'Player/Footsteps/Stone/stepstone_8.ogg',
    ],
    'water': ['Player/Footsteps/Water/stepwater_1.ogg',
              'Player/Footsteps/Water/stepwater_2.ogg'
              ],
    'wood': ['Player/Footsteps/Wood/stepwood_1.ogg',
             'Player/Footsteps/Wood/stepwood_2.ogg'
             ],
}

PLAYER_FOOTSTEP_INTERVAL_TIMES = {
    'run': 350,
    'walk': 750
}

# Enemy settings
ENEMY_ATTACK_RATE = 500
ENEMY_DAMAGE = [x for x in range(50, 75)]
ENEMY_KNOCKBACK = 10
ENEMY_LINE_OF_SIGHT = TILESIZE / 2.75
ENEMY_HIT_RECT = pg.Rect(0, 0, TILESIZE + 16, TILESIZE + 16)
ENEMY_SPEEDS = [speed for speed in range(70, 150, 10)]
ENEMY_HEALTH = [dmg for dmg in range(500, 1000, 100)]
DETECT_RADIUS = 400
APPROACH_RADIUS = 150
AVOID_RADIUS = 10
SEEK_FORCE = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
WANDER_RING_DISTANCE = 100
WANDER_RING_RADIUS = [x for x in range(40, 100, 10)]
ENEMY_HIT_SOUNDS = {'bash': ['zombies/Hit sounds/Bash/Bash hit 1.ogg',
                             'zombies/Hit sounds/Bash/Bash hit 2.ogg',
                             'zombies/Hit sounds/Bash/Bash hit 3.ogg',
                             'zombies/Hit sounds/Bash/Bash hit 4.ogg',
                             'zombies/Hit sounds/Bash/Bash hit 5.ogg'
                             ],
                    'bullet': ['zombies/Hit sounds/Bullet/Bullet hit 1.ogg',
                               'zombies/Hit sounds/Bullet/Bullet hit 2.ogg',
                               'zombies/Hit sounds/Bullet/Bullet hit 3.ogg',
                               'zombies/Hit sounds/Bullet/Bullet hit 4.ogg'
                               ]
                    }
ZOMBIE_MOAN_SOUNDS = [
    'zombies/Moans/zombie-1.ogg',
    'zombies/Moans/zombie-2.ogg',
    'zombies/Moans/zombie-3.ogg',
    'zombies/Moans/zombie-4.ogg',
    'zombies/Moans/zombie-5.ogg',
    'zombies/Moans/zombie-6.ogg',
    'zombies/Moans/zombie-7.ogg',
    'zombies/Moans/zombie-8.ogg',
    'zombies/Moans/zombie-9.ogg',
    'zombies/Moans/zombie-10.ogg',
    'zombies/Moans/zombie-11.ogg',
    'zombies/Moans/zombie-12.ogg',
    'zombies/Moans/zombie-13.ogg',
    'zombies/Moans/zombie-14.ogg',
    'zombies/Moans/zombie-15.ogg',
    'zombies/Moans/zombie-16.ogg',
    'zombies/Moans/zombie-17.ogg',
    'zombies/Moans/zombie-18.ogg',
    'zombies/Moans/zombie-19.ogg',
    'zombies/Moans/zombie-20.ogg',
    'zombies/Moans/zombie-21.ogg',
    'zombies/Moans/zombie-22.ogg',
    'zombies/Moans/zombie-23.ogg',
    'zombies/Moans/zombie-24.ogg',
]

# Weapon settings
WEAPONS = {}

BULLET_SPEED = 3000
BULLET_LIFETIME = 2000

WEAPONS['penetration depreciation'] = {'rifle': .15, 'handgun': .5, 'shotgun': .2}

WEAPONS['animation times'] = {'handgun': {'idle': 100, 'melee': 45, 'move': 100, 'reload': 75, 'shoot': 125},
                              'knife': {'idle': 100, 'melee': 30, 'move': 75, 'reload': 0, 'shoot': 0},
                              'rifle': {'idle': 100, 'melee': 45, 'move': 125, 'reload': 100, 'shoot': 55},
                              'shotgun': {'idle': 100, 'melee': 45, 'move': 125, 'reload': 110, 'shoot': 175}}

WEAPONS['sound'] = {'handgun': {'attack': 'Weapons/Attack/pistol.wav', 'pickup': 'Weapons/Pickup/gun_pickup.wav',
                                'reload': 'Weapons/Reload/Handgun1.ogg'},
                    'shotgun': {'attack': 'Weapons/Attack/shotgun.wav', 'pickup': 'Weapons/Pickup/gun_pickup.wav',
                                'reload': 'Weapons/Reload/Shotgun1.ogg'},
                    'rifle': {'attack': 'Weapons/Attack/rifle.wav', 'pickup': 'Weapons/Pickup/gun_pickup.wav',
                              'reload': 'Weapons/Reload/Rifle1.ogg'},
                    'knife': {'draw': 'Weapons/Draw/knifedraw.wav'}
                    }

WEAPONS['handgun'] = {'bullet_speed': BULLET_SPEED,
                      'bullet_lifetime': BULLET_LIFETIME,
                      'rate': 200,
                      'kickback': 65,
                      'spread': 1,
                      'damage': 100,
                      'bullet_size': 'med',
                      'clip size': 15,
                      'weight': 3,
                      'wobble': {'sprint': 3, 'walk': 2, 'idle': 1},
                      'muzzle flash range': [25, 35],
                      'barrel offset': vec(45, 22),
                      'crosshair radius': 10,
                      'knockback': vec(20, 0),
                      'bullet_count': 1}

WEAPONS['rifle'] = {'bullet_speed': BULLET_SPEED,
                    'bullet_lifetime': BULLET_LIFETIME,
                    'rate': 100,
                    'kickback': 200,
                    'spread': 2,
                    'damage': 80,
                    'bullet_size': 'lg',
                    'clip size': 40,
                    'weight': 5,
                    'wobble': {'sprint': 5, 'walk': 4, 'idle': 3},
                    'muzzle flash range': [35, 60],
                    'barrel offset': vec(60, 22),
                    'crosshair radius': 15,
                    'knockback': vec(25, 0),
                    'bullet_count': 1}

WEAPONS['shotgun'] = {'bullet_speed': BULLET_SPEED,
                      'bullet_lifetime': BULLET_LIFETIME,
                      'rate': 600,
                      'kickback': 300,
                      'spread': 8,
                      'damage': 45,
                      'bullet_size': 'sm',
                      'clip size': 8,
                      'weight': 5,
                      'wobble': {'sprint': 4, 'walk': 3, 'idle': 2},
                      'muzzle flash range': [50, 70],
                      'barrel offset': vec(67, 22),
                      'crosshair radius': 20,
                      'knockback': vec(25, 0),
                      'bullet_count': 16}
WEAPONS['knife'] = {
    'damage': 205,
    'weight': 2,
    'knockback': 20,
    'crosshair radius': 5,
    'spread': 1,
    'knockback': vec(30, 0),
    'wobble': {'sprint': 0, 'walk': 0, 'idle': 0}
}

WEAPONS['melee'] = {
    'handgun': 120,
    'rifle': 170,
    'shotgun': 190,
    'knife': 140
}

ITEMS = {}
ITEMS['weapon'] = {'rifle': [i for i in range(4, 7)], 'handgun': [i for i in range(4, 9)],
                   'shotgun': [i for i in range(4, 7)]}
ITEMS['consumable'] = {'health': [i for i in range(10, 21)], 'ammo': [i for i in range(1, 5)]}

# Item images
ITEM_IMAGES = {'rifle': 'rifle.png',
               'handgun': 'glock.png',
               'shotgun': 'shotgun.png',
               'ammo': 'Ammo.png',
               'health': 'health.png'
               }

# Enemy Animations
ENEMY_IMGS = [
    '../data/img/Enemies/citizenzombie1.png',
    '../data/img/Enemies/citizenzombie2.png',
    '../data/img/Enemies/citizenzombie3.png',
    '../data/img/Enemies/citizenzombie4.png',
    '../data/img/Enemies/citizenzombie5.png',
    '../data/img/Enemies/citizenzombie6.png',
    '../data/img/Enemies/citizenzombie7.png',
    '../data/img/Enemies/citizenzombie8.png',
    '../data/img/Enemies/citizenzombie9.png',
    '../data/img/Enemies/citizenzombie10.png',
]

# Player Animations
HANDGUN_ANIMATIONS = {}
KNIFE_ANIMATIONS = {}
RIFLE_ANIMATIONS = {}
SHOTGUN_ANIMATIONS = {}
FEET_ANIMATIONS = {}

HANDGUN_ANIMATIONS['idle'] = get_image_names('../data/img/Player animations/handgun/idle/')
HANDGUN_ANIMATIONS['melee'] = get_image_names('../data/img/Player animations/handgun/meleeattack/')
HANDGUN_ANIMATIONS['move'] = get_image_names('../data/img/Player animations/handgun/move/')
HANDGUN_ANIMATIONS['reload'] = get_image_names('../data/img/Player animations/handgun/reload/')
HANDGUN_ANIMATIONS['shoot'] = get_image_names('../data/img/Player animations/handgun/shoot/')

KNIFE_ANIMATIONS['idle'] = get_image_names("../data/img/Player animations/knife/idle/")
KNIFE_ANIMATIONS['melee'] = get_image_names("../data/img/Player animations/knife/meleeattack/")
KNIFE_ANIMATIONS['move'] = get_image_names('../data/img/Player animations/knife/move/')

RIFLE_ANIMATIONS['idle'] = get_image_names("../data/img/Player animations/rifle/idle/")
RIFLE_ANIMATIONS['melee'] = get_image_names("../data/img/Player animations/rifle/meleeattack/")
RIFLE_ANIMATIONS['move'] = get_image_names("../data/img/Player animations/rifle/move/")
RIFLE_ANIMATIONS['reload'] = get_image_names('../data/img/Player animations/rifle/reload/')
RIFLE_ANIMATIONS['shoot'] = get_image_names('../data/img/Player animations/rifle/shoot/')

SHOTGUN_ANIMATIONS['idle'] = get_image_names("../data/img/Player animations/shotgun/idle/")
SHOTGUN_ANIMATIONS['melee'] = get_image_names("../data/img/Player animations/shotgun/meleeattack/")
SHOTGUN_ANIMATIONS['move'] = get_image_names("../data/img/Player animations/shotgun/move/")
SHOTGUN_ANIMATIONS['reload'] = get_image_names('../data/img/Player animations/shotgun/reload/')
SHOTGUN_ANIMATIONS['shoot'] = get_image_names('../data/img/Player animations/shotgun/shoot/')
