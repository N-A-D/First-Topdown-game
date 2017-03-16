'''
Created on Mar 15, 2017

@author: Austin
'''
import pygame as pg
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

TILESIZE = 256
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Bullet image
RIFLE_BULLET_IMG = 'rifle_bullet.png'
SHOTGUN_BULLET_IMG = 'bullet.png'


# Player settings
AIM_OFFSET = 0
DEFAULT_WEAPON = 'knife'
WEAPON_ANIMATION_TIMES = {'handgun': {'idle': 100, 'melee': 50, 'move': 100, 'reload': 75, 'shoot':125}, 
                          'knife': {'idle': 100, 'melee': 50, 'move': 75, 'reload': 0, 'shoot':0}, 
                          'rifle': {'idle': 100, 'melee': 50, 'move': 125, 'reload': 150, 'shoot':55}, 
                          'shotgun': {'idle': 100, 'melee': 50, 'move': 125, 'reload': 150, 'shoot':175}}
PLAYER_SPEED = 500
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(150, 45)


# Weapon settings
WEAPONS = {}
WEAPONS['handgun'] = {'bullet_speed': 1000, 
                    'bullet_lifetime': 1000, 
                    'rate': 250, 
                    'kickback': 150, 
                    'spread': 3, 
                    'damage': 10, 
                    'bullet_size': 'lg', 
                    'bullet_count': 1}

WEAPONS['rifle'] = {'bullet_speed': 1000, 
                    'bullet_lifetime': 10000, 
                    'rate': 110, 
                    'kickback': 400, 
                    'spread': 6, 
                    'damage': 50, 
                    'bullet_size': 'lg', 
                    'bullet_count': 1}
WEAPONS['shotgun'] = {'bullet_speed': 1000, 
                    'bullet_lifetime': 1000, 
                    'rate': 400, 
                    'kickback': 1300, 
                    'spread': 15, 
                    'damage': 20, 
                    'bullet_size': 'sm', 
                    'bullet_count': 14}

# Animations
HANDGUN_ANIMATIONS = {}
KNIFE_ANIMATIONS = {}
RIFLE_ANIMATIONS = {}
SHOTGUN_ANIMATIONS = {}

HANDGUN_ANIMATIONS['idle'] = ['Player animations\handgun\idle\survivor-idle_handgun_0.png',
                                    'Player animations\handgun\idle\survivor-idle_handgun_1.png',
                                    'Player animations\handgun\idle\survivor-idle_handgun_2.png',
                                    'Player animations\handgun\idle\survivor-idle_handgun_3.png',
                                    'Player animations\handgun\idle\survivor-idle_handgun_4.png',
                                    'Player animations\handgun\idle\survivor-idle_handgun_5.png',
                                    'Player animations\handgun\idle\survivor-idle_handgun_6.png',
                                    'Player animations\handgun\idle\survivor-idle_handgun_7.png',
                                    'Player animations\handgun\idle\survivor-idle_handgun_8.png',
                                    'Player animations\handgun\idle\survivor-idle_handgun_9.png',
                                    'Player animations\handgun\idle\survivor-idle_handgun_10.png',
                                    'Player animations\handgun\idle\survivor-idle_handgun_11.png',
                                    'Player animations\handgun\idle\survivor-idle_handgun_12.png',
                                    'Player animations\handgun\idle\survivor-idle_handgun_13.png',
                                    'Player animations\handgun\idle\survivor-idle_handgun_14.png',
                                    'Player animations\handgun\idle\survivor-idle_handgun_15.png',
                                    'Player animations\handgun\idle\survivor-idle_handgun_16.png',
                                    'Player animations\handgun\idle\survivor-idle_handgun_17.png',
                                    'Player animations\handgun\idle\survivor-idle_handgun_18.png',
                                    'Player animations\handgun\idle\survivor-idle_handgun_19.png'
                                    ]
HANDGUN_ANIMATIONS['melee'] = ['Player animations\handgun\meleeattack\survivor-meleeattack_handgun_0.png',
                                           'Player animations\handgun\meleeattack\survivor-meleeattack_handgun_1.png',
                                           'Player animations\handgun\meleeattack\survivor-meleeattack_handgun_2.png',
                                           'Player animations\handgun\meleeattack\survivor-meleeattack_handgun_3.png',
                                           'Player animations\handgun\meleeattack\survivor-meleeattack_handgun_4.png',
                                           'Player animations\handgun\meleeattack\survivor-meleeattack_handgun_5.png',
                                           'Player animations\handgun\meleeattack\survivor-meleeattack_handgun_6.png',
                                           'Player animations\handgun\meleeattack\survivor-meleeattack_handgun_7.png',
                                           'Player animations\handgun\meleeattack\survivor-meleeattack_handgun_8.png',
                                           'Player animations\handgun\meleeattack\survivor-meleeattack_handgun_9.png',
                                           'Player animations\handgun\meleeattack\survivor-meleeattack_handgun_10.png',
                                           'Player animations\handgun\meleeattack\survivor-meleeattack_handgun_11.png',
                                           'Player animations\handgun\meleeattack\survivor-meleeattack_handgun_12.png',
                                           'Player animations\handgun\meleeattack\survivor-meleeattack_handgun_13.png',
                                           'Player animations\handgun\meleeattack\survivor-meleeattack_handgun_14.png'
                                           ]
HANDGUN_ANIMATIONS['move'] = ['Player animations\handgun\move\survivor-move_handgun_0.png',
                                    'Player animations\handgun\move\survivor-move_handgun_1.png',
                                    'Player animations\handgun\move\survivor-move_handgun_2.png',
                                    'Player animations\handgun\move\survivor-move_handgun_3.png',
                                    'Player animations\handgun\move\survivor-move_handgun_4.png',
                                    'Player animations\handgun\move\survivor-move_handgun_5.png',
                                    'Player animations\handgun\move\survivor-move_handgun_6.png',
                                    'Player animations\handgun\move\survivor-move_handgun_7.png',
                                    'Player animations\handgun\move\survivor-move_handgun_8.png',
                                    'Player animations\handgun\move\survivor-move_handgun_9.png',
                                    'Player animations\handgun\move\survivor-move_handgun_10.png',
                                    'Player animations\handgun\move\survivor-move_handgun_11.png',
                                    'Player animations\handgun\move\survivor-move_handgun_12.png',
                                    'Player animations\handgun\move\survivor-move_handgun_13.png',
                                    'Player animations\handgun\move\survivor-move_handgun_14.png',
                                    'Player animations\handgun\move\survivor-move_handgun_15.png',
                                    'Player animations\handgun\move\survivor-move_handgun_16.png',
                                    'Player animations\handgun\move\survivor-move_handgun_17.png',
                                    'Player animations\handgun\move\survivor-move_handgun_18.png',
                                    'Player animations\handgun\move\survivor-move_handgun_19.png'
                                    ]
HANDGUN_ANIMATIONS['reload'] = ['Player animations\\handgun\\reload\\survivor-reload_handgun_0.png',
                                      'Player animations\\handgun\\reload\\survivor-reload_handgun_1.png',
                                      'Player animations\\handgun\\reload\\survivor-reload_handgun_2.png',
                                      'Player animations\\handgun\\reload\\survivor-reload_handgun_3.png',
                                      'Player animations\\handgun\\reload\\survivor-reload_handgun_4.png',
                                      'Player animations\\handgun\\reload\\survivor-reload_handgun_5.png',
                                      'Player animations\\handgun\\reload\\survivor-reload_handgun_6.png',
                                      'Player animations\\handgun\\reload\\survivor-reload_handgun_7.png',
                                      'Player animations\\handgun\\reload\\survivor-reload_handgun_8.png',
                                      'Player animations\\handgun\\reload\\survivor-reload_handgun_9.png',
                                      'Player animations\\handgun\\reload\\survivor-reload_handgun_10.png',
                                      'Player animations\\handgun\\reload\\survivor-reload_handgun_11.png',
                                      'Player animations\\handgun\\reload\\survivor-reload_handgun_12.png',
                                      'Player animations\\handgun\\reload\\survivor-reload_handgun_13.png',
                                      'Player animations\\handgun\\reload\\survivor-reload_handgun_14.png'
                                      ]
HANDGUN_ANIMATIONS['shoot'] = ['Player animations\handgun\shoot\survivor-shoot_handgun_0.png',
                                     'Player animations\handgun\shoot\survivor-shoot_handgun_1.png',
                                     'Player animations\handgun\shoot\survivor-shoot_handgun_2.png'
                                     ]
KNIFE_ANIMATIONS['idle'] = ["Player animations\\knife\\idle\\survivor-idle_knife_0.png",
                                   "Player animations\\knife\\idle\\survivor-idle_knife_1.png",
                                   "Player animations\\knife\\idle\\survivor-idle_knife_2.png",
                                   "Player animations\\knife\\idle\\survivor-idle_knife_3.png",
                                   "Player animations\\knife\\idle\\survivor-idle_knife_4.png",
                                   "Player animations\\knife\\idle\\survivor-idle_knife_5.png",
                                   "Player animations\\knife\\idle\\survivor-idle_knife_6.png",
                                   "Player animations\\knife\\idle\\survivor-idle_knife_7.png",
                                   "Player animations\\knife\\idle\\survivor-idle_knife_8.png",
                                   "Player animations\\knife\\idle\\survivor-idle_knife_9.png",
                                   "Player animations\\knife\\idle\\survivor-idle_knife_10.png",
                                   "Player animations\\knife\\idle\\survivor-idle_knife_11.png",
                                   "Player animations\\knife\\idle\\survivor-idle_knife_12.png",
                                   "Player animations\\knife\\idle\\survivor-idle_knife_13.png",
                                   "Player animations\\knife\\idle\\survivor-idle_knife_14.png",
                                   "Player animations\\knife\\idle\\survivor-idle_knife_15.png",
                                   "Player animations\\knife\\idle\\survivor-idle_knife_16.png",
                                   "Player animations\\knife\\idle\\survivor-idle_knife_17.png",
                                   "Player animations\\knife\\idle\\survivor-idle_knife_18.png",
                                   "Player animations\\knife\\idle\\survivor-idle_knife_19.png",
                                   ]
KNIFE_ANIMATIONS['melee'] = ["Player animations\\knife\\meleeattack\\survivor-meleeattack_knife_0.png",
                                    "Player animations\\knife\\meleeattack\\survivor-meleeattack_knife_1.png",
                                    "Player animations\\knife\\meleeattack\\survivor-meleeattack_knife_2.png",
                                    "Player animations\\knife\\meleeattack\\survivor-meleeattack_knife_3.png",
                                    "Player animations\\knife\\meleeattack\\survivor-meleeattack_knife_4.png",
                                    "Player animations\\knife\\meleeattack\\survivor-meleeattack_knife_5.png",
                                    "Player animations\\knife\\meleeattack\\survivor-meleeattack_knife_6.png",
                                    "Player animations\\knife\\meleeattack\\survivor-meleeattack_knife_7.png",
                                    "Player animations\\knife\\meleeattack\\survivor-meleeattack_knife_8.png",
                                    "Player animations\\knife\\meleeattack\\survivor-meleeattack_knife_9.png",
                                    "Player animations\\knife\\meleeattack\\survivor-meleeattack_knife_10.png",
                                    "Player animations\\knife\\meleeattack\\survivor-meleeattack_knife_11.png",
                                    "Player animations\\knife\\meleeattack\\survivor-meleeattack_knife_12.png",
                                    "Player animations\\knife\\meleeattack\\survivor-meleeattack_knife_13.png",
                                    "Player animations\\knife\\meleeattack\\survivor-meleeattack_knife_14.png"
                                    ]

KNIFE_ANIMATIONS['move'] = ['Player animations\\knife\\move\\survivor-move_knife_0.png',
                                   'Player animations\\knife\\move\\survivor-move_knife_1.png', 
                                   'Player animations\\knife\\move\\survivor-move_knife_2.png', 
                                   'Player animations\\knife\\move\\survivor-move_knife_3.png', 
                                   'Player animations\\knife\\move\\survivor-move_knife_4.png', 
                                   'Player animations\\knife\\move\\survivor-move_knife_5.png', 
                                   'Player animations\\knife\\move\\survivor-move_knife_6.png', 
                                   'Player animations\\knife\\move\\survivor-move_knife_7.png', 
                                   'Player animations\\knife\\move\\survivor-move_knife_8.png', 
                                   'Player animations\\knife\\move\\survivor-move_knife_9.png', 
                                   'Player animations\\knife\\move\\survivor-move_knife_10.png', 
                                   'Player animations\\knife\\move\\survivor-move_knife_11.png', 
                                   'Player animations\\knife\\move\\survivor-move_knife_12.png', 
                                   'Player animations\\knife\\move\\survivor-move_knife_13.png', 
                                   'Player animations\\knife\\move\\survivor-move_knife_14.png', 
                                   'Player animations\\knife\\move\\survivor-move_knife_15.png', 
                                   'Player animations\\knife\\move\\survivor-move_knife_16.png', 
                                   'Player animations\\knife\\move\\survivor-move_knife_17.png', 
                                   'Player animations\\knife\\move\\survivor-move_knife_18.png', 
                                   'Player animations\\knife\\move\\survivor-move_knife_19.png',   
                                   ]

RIFLE_ANIMATIONS['idle'] = ["Player animations\\rifle\\idle\\survivor-idle_rifle_0.png",
                                   "Player animations\\rifle\\idle\\survivor-idle_rifle_1.png", 
                                   "Player animations\\rifle\\idle\\survivor-idle_rifle_2.png", 
                                   "Player animations\\rifle\\idle\\survivor-idle_rifle_3.png", 
                                   "Player animations\\rifle\\idle\\survivor-idle_rifle_4.png", 
                                   "Player animations\\rifle\\idle\\survivor-idle_rifle_5.png", 
                                   "Player animations\\rifle\\idle\\survivor-idle_rifle_6.png", 
                                   "Player animations\\rifle\\idle\\survivor-idle_rifle_7.png", 
                                   "Player animations\\rifle\\idle\\survivor-idle_rifle_8.png", 
                                   "Player animations\\rifle\\idle\\survivor-idle_rifle_9.png", 
                                   "Player animations\\rifle\\idle\\survivor-idle_rifle_10.png", 
                                   "Player animations\\rifle\\idle\\survivor-idle_rifle_11.png", 
                                   "Player animations\\rifle\\idle\\survivor-idle_rifle_12.png", 
                                   "Player animations\\rifle\\idle\\survivor-idle_rifle_13.png", 
                                   "Player animations\\rifle\\idle\\survivor-idle_rifle_14.png", 
                                   "Player animations\\rifle\\idle\\survivor-idle_rifle_15.png", 
                                   "Player animations\\rifle\\idle\\survivor-idle_rifle_16.png", 
                                   "Player animations\\rifle\\idle\\survivor-idle_rifle_17.png", 
                                   "Player animations\\rifle\\idle\\survivor-idle_rifle_18.png", 
                                   "Player animations\\rifle\\idle\\survivor-idle_rifle_19.png",  
                                   ]
RIFLE_ANIMATIONS['melee'] = ["Player animations\\rifle\\meleeattack\\survivor-meleeattack_rifle_0.png",
                                    "Player animations\\rifle\\meleeattack\\survivor-meleeattack_rifle_1.png",
                                    "Player animations\\rifle\\meleeattack\\survivor-meleeattack_rifle_2.png",
                                    "Player animations\\rifle\\meleeattack\\survivor-meleeattack_rifle_3.png",
                                    "Player animations\\rifle\\meleeattack\\survivor-meleeattack_rifle_4.png",
                                    "Player animations\\rifle\\meleeattack\\survivor-meleeattack_rifle_5.png",
                                    "Player animations\\rifle\\meleeattack\\survivor-meleeattack_rifle_6.png",
                                    "Player animations\\rifle\\meleeattack\\survivor-meleeattack_rifle_7.png",
                                    "Player animations\\rifle\\meleeattack\\survivor-meleeattack_rifle_8.png",
                                    "Player animations\\rifle\\meleeattack\\survivor-meleeattack_rifle_9.png",
                                    "Player animations\\rifle\\meleeattack\\survivor-meleeattack_rifle_10.png",
                                    "Player animations\\rifle\\meleeattack\\survivor-meleeattack_rifle_11.png",
                                    "Player animations\\rifle\\meleeattack\\survivor-meleeattack_rifle_12.png",
                                    "Player animations\\rifle\\meleeattack\\survivor-meleeattack_rifle_13.png",
                                    "Player animations\\rifle\\meleeattack\\survivor-meleeattack_rifle_14.png",
                                    ]
RIFLE_ANIMATIONS['move'] = ["Player animations\\rifle\\move\\survivor-move_rifle_0.png",
                                   "Player animations\\rifle\\move\\survivor-move_rifle_1.png",
                                   "Player animations\\rifle\\move\\survivor-move_rifle_2.png",
                                   "Player animations\\rifle\\move\\survivor-move_rifle_3.png",
                                   "Player animations\\rifle\\move\\survivor-move_rifle_4.png",
                                   "Player animations\\rifle\\move\\survivor-move_rifle_5.png",
                                   "Player animations\\rifle\\move\\survivor-move_rifle_6.png",
                                   "Player animations\\rifle\\move\\survivor-move_rifle_7.png",
                                   "Player animations\\rifle\\move\\survivor-move_rifle_8.png",
                                   "Player animations\\rifle\\move\\survivor-move_rifle_9.png",
                                   "Player animations\\rifle\\move\\survivor-move_rifle_10.png",
                                   "Player animations\\rifle\\move\\survivor-move_rifle_11.png",
                                   "Player animations\\rifle\\move\\survivor-move_rifle_12.png",
                                   "Player animations\\rifle\\move\\survivor-move_rifle_13.png",
                                   "Player animations\\rifle\\move\\survivor-move_rifle_14.png",
                                   "Player animations\\rifle\\move\\survivor-move_rifle_15.png",
                                   "Player animations\\rifle\\move\\survivor-move_rifle_16.png",
                                   "Player animations\\rifle\\move\\survivor-move_rifle_17.png",
                                   "Player animations\\rifle\\move\\survivor-move_rifle_18.png",
                                   "Player animations\\rifle\\move\\survivor-move_rifle_19.png",
                                   ]
RIFLE_ANIMATIONS['reload'] = ['Player animations\\rifle\\reload\\survivor-reload_rifle_0.png',
                                     'Player animations\\rifle\\reload\\survivor-reload_rifle_1.png',
                                     'Player animations\\rifle\\reload\\survivor-reload_rifle_2.png',
                                     'Player animations\\rifle\\reload\\survivor-reload_rifle_3.png',
                                     'Player animations\\rifle\\reload\\survivor-reload_rifle_4.png',
                                     'Player animations\\rifle\\reload\\survivor-reload_rifle_5.png',
                                     'Player animations\\rifle\\reload\\survivor-reload_rifle_6.png',
                                     'Player animations\\rifle\\reload\\survivor-reload_rifle_7.png',
                                     'Player animations\\rifle\\reload\\survivor-reload_rifle_8.png',
                                     'Player animations\\rifle\\reload\\survivor-reload_rifle_9.png',
                                     'Player animations\\rifle\\reload\\survivor-reload_rifle_10.png',
                                     'Player animations\\rifle\\reload\\survivor-reload_rifle_11.png',
                                     'Player animations\\rifle\\reload\\survivor-reload_rifle_12.png',
                                     'Player animations\\rifle\\reload\\survivor-reload_rifle_13.png',
                                     'Player animations\\rifle\\reload\\survivor-reload_rifle_14.png',
                                     'Player animations\\rifle\\reload\\survivor-reload_rifle_15.png',
                                     'Player animations\\rifle\\reload\\survivor-reload_rifle_16.png',
                                     'Player animations\\rifle\\reload\\survivor-reload_rifle_17.png',
                                     'Player animations\\rifle\\reload\\survivor-reload_rifle_18.png',
                                     'Player animations\\rifle\\reload\\survivor-reload_rifle_19.png',
                                    ]
RIFLE_ANIMATIONS['shoot'] = ['Player animations\\rifle\\shoot\\survivor-shoot_rifle_0.png',
                                     'Player animations\\rifle\\shoot\\survivor-shoot_rifle_1.png',
                                     'Player animations\\rifle\\shoot\survivor-shoot_rifle_2.png'
                                     ]

SHOTGUN_ANIMATIONS['idle'] = ["Player animations\\shotgun\\idle\\survivor-idle_shotgun_0.png",
                                   "Player animations\\shotgun\\idle\\survivor-idle_shotgun_1.png", 
                                   "Player animations\\shotgun\\idle\\survivor-idle_shotgun_2.png", 
                                   "Player animations\\shotgun\\idle\\survivor-idle_shotgun_3.png", 
                                   "Player animations\\shotgun\\idle\\survivor-idle_shotgun_4.png", 
                                   "Player animations\\shotgun\\idle\\survivor-idle_shotgun_5.png", 
                                   "Player animations\\shotgun\\idle\\survivor-idle_shotgun_6.png", 
                                   "Player animations\\shotgun\\idle\\survivor-idle_shotgun_7.png", 
                                   "Player animations\\shotgun\\idle\\survivor-idle_shotgun_8.png", 
                                   "Player animations\\shotgun\\idle\\survivor-idle_shotgun_9.png", 
                                   "Player animations\\shotgun\\idle\\survivor-idle_shotgun_10.png", 
                                   "Player animations\\shotgun\\idle\\survivor-idle_shotgun_11.png", 
                                   "Player animations\\shotgun\\idle\\survivor-idle_shotgun_12.png", 
                                   "Player animations\\shotgun\\idle\\survivor-idle_shotgun_13.png", 
                                   "Player animations\\shotgun\\idle\\survivor-idle_shotgun_14.png", 
                                   "Player animations\\shotgun\\idle\\survivor-idle_shotgun_15.png", 
                                   "Player animations\\shotgun\\idle\\survivor-idle_shotgun_16.png", 
                                   "Player animations\\shotgun\\idle\\survivor-idle_shotgun_17.png", 
                                   "Player animations\\shotgun\\idle\\survivor-idle_shotgun_18.png", 
                                   "Player animations\\shotgun\\idle\\survivor-idle_shotgun_19.png",   
                                   ]
SHOTGUN_ANIMATIONS['melee'] = ["Player animations\\shotgun\\meleeattack\\survivor-meleeattack_shotgun_0.png",
                                    "Player animations\\shotgun\\meleeattack\\survivor-meleeattack_shotgun_1.png",
                                    "Player animations\\shotgun\\meleeattack\\survivor-meleeattack_shotgun_2.png",
                                    "Player animations\\shotgun\\meleeattack\\survivor-meleeattack_shotgun_3.png",
                                    "Player animations\\shotgun\\meleeattack\\survivor-meleeattack_shotgun_4.png",
                                    "Player animations\\shotgun\\meleeattack\\survivor-meleeattack_shotgun_5.png",
                                    "Player animations\\shotgun\\meleeattack\\survivor-meleeattack_shotgun_6.png",
                                    "Player animations\\shotgun\\meleeattack\\survivor-meleeattack_shotgun_7.png",
                                    "Player animations\\shotgun\\meleeattack\\survivor-meleeattack_shotgun_8.png",
                                    "Player animations\\shotgun\\meleeattack\\survivor-meleeattack_shotgun_9.png",
                                    "Player animations\\shotgun\\meleeattack\\survivor-meleeattack_shotgun_10.png",
                                    "Player animations\\shotgun\\meleeattack\\survivor-meleeattack_shotgun_11.png",
                                    "Player animations\\shotgun\\meleeattack\\survivor-meleeattack_shotgun_12.png",
                                    "Player animations\\shotgun\\meleeattack\\survivor-meleeattack_shotgun_13.png",
                                    "Player animations\\shotgun\\meleeattack\\survivor-meleeattack_shotgun_14.png",
                                    ]
SHOTGUN_ANIMATIONS['move'] = ["Player animations\\shotgun\\move\\survivor-move_shotgun_0.png",
                                   "Player animations\\shotgun\\move\\survivor-move_shotgun_1.png",
                                   "Player animations\\shotgun\\move\\survivor-move_shotgun_2.png",
                                   "Player animations\\shotgun\\move\\survivor-move_shotgun_3.png",
                                   "Player animations\\shotgun\\move\\survivor-move_shotgun_4.png",
                                   "Player animations\\shotgun\\move\\survivor-move_shotgun_5.png",
                                   "Player animations\\shotgun\\move\\survivor-move_shotgun_6.png",
                                   "Player animations\\shotgun\\move\\survivor-move_shotgun_7.png",
                                   "Player animations\\shotgun\\move\\survivor-move_shotgun_8.png",
                                   "Player animations\\shotgun\\move\\survivor-move_shotgun_9.png",
                                   "Player animations\\shotgun\\move\\survivor-move_shotgun_10.png",
                                   "Player animations\\shotgun\\move\\survivor-move_shotgun_11.png",
                                   "Player animations\\shotgun\\move\\survivor-move_shotgun_12.png",
                                   "Player animations\\shotgun\\move\\survivor-move_shotgun_13.png",
                                   "Player animations\\shotgun\\move\\survivor-move_shotgun_14.png",
                                   "Player animations\\shotgun\\move\\survivor-move_shotgun_15.png",
                                   "Player animations\\shotgun\\move\\survivor-move_shotgun_16.png",
                                   "Player animations\\shotgun\\move\\survivor-move_shotgun_17.png",
                                   "Player animations\\shotgun\\move\\survivor-move_shotgun_18.png",
                                   "Player animations\\shotgun\\move\\survivor-move_shotgun_19.png", 
                                   ]
SHOTGUN_ANIMATIONS['reload'] = ['Player animations\\shotgun\\reload\\survivor-reload_shotgun_0.png',
                                     'Player animations\\shotgun\\reload\\survivor-reload_shotgun_1.png',
                                     'Player animations\\shotgun\\reload\\survivor-reload_shotgun_2.png',
                                     'Player animations\\shotgun\\reload\\survivor-reload_shotgun_3.png',
                                     'Player animations\\shotgun\\reload\\survivor-reload_shotgun_4.png',
                                     'Player animations\\shotgun\\reload\\survivor-reload_shotgun_5.png',
                                     'Player animations\\shotgun\\reload\\survivor-reload_shotgun_6.png',
                                     'Player animations\\shotgun\\reload\\survivor-reload_shotgun_7.png',
                                     'Player animations\\shotgun\\reload\\survivor-reload_shotgun_8.png',
                                     'Player animations\\shotgun\\reload\\survivor-reload_shotgun_9.png',
                                     'Player animations\\shotgun\\reload\\survivor-reload_shotgun_10.png',
                                     'Player animations\\shotgun\\reload\\survivor-reload_shotgun_11.png',
                                     'Player animations\\shotgun\\reload\\survivor-reload_shotgun_12.png',
                                     'Player animations\\shotgun\\reload\\survivor-reload_shotgun_13.png',
                                     'Player animations\\shotgun\\reload\\survivor-reload_shotgun_14.png',
                                     'Player animations\\shotgun\\reload\\survivor-reload_shotgun_15.png',
                                     'Player animations\\shotgun\\reload\\survivor-reload_shotgun_16.png',
                                     'Player animations\\shotgun\\reload\\survivor-reload_shotgun_17.png',
                                     'Player animations\\shotgun\\reload\\survivor-reload_shotgun_18.png',
                                     'Player animations\\shotgun\\reload\\survivor-reload_shotgun_19.png',
                                    ]
SHOTGUN_ANIMATIONS['shoot'] = ['Player animations\\shotgun\\shoot\\survivor-shoot_shotgun_0.png',
                                     'Player animations\\shotgun\\shoot\\survivor-shoot_shotgun_1.png',
                                     'Player animations\\shotgun\\shoot\survivor-shoot_shotgun_2.png'
                                     ]
