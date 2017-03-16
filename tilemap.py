'''
Created on Mar 15, 2017

@author: Austin
'''
import pygame as pg 
from settings import TILESIZE, WIDTH, HEIGHT

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as file:
            for line in file:
                self.data.append(line.strip())
                
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE
        
class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
    
    def apply(self, entity):
        # Applies the camera offset, i.e, 
        # moves this entity the camera's 
        # topleft corner
        return entity.rect.move(self.camera.topleft)
    
    def apply_rect(self, rect):
        # Applies the camera offset to 
        # a rectangle
        return rect.move(self.camera.topleft())
    
    def update(self, target):
        # Get how much the target moved in the x & y 
        # (WIDTH // 2) & (HEIGHT // 2) since the target
        # is dead center in camera view
        x = -target.rect.centerx + (WIDTH // 2)
        y = -target.rect.centery + (HEIGHT // 2)
        
        # Limit the scrolling on all four sides of the screen
        x = min(0, x) # left
        y = min(0, y) # right
        x = max(-(self.width - WIDTH), x) # right
        y = max(-(self.height - HEIGHT), y) # bottom
        # Update the camera
        self.camera = pg.Rect(x, y, self.width, self.height)