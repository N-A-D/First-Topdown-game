'''
@author: Ned Austin Datiles
'''

import pygame as pg
from settings import *

class Mob(pg.sprite.Sprite):
    '''
    classdocs
    '''
    def __init__(self, game, x, y):
        '''
        Constructor
        '''
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups)
