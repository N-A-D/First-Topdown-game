'''
Created on Mar 15, 2017

@author: Ned Austin Datiles
'''
import pygame as pg
from settings import TILESIZE, WIDTH, HEIGHT, vec


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
        """
        Creates a camera object 
        :param width: The width of the cameras view
        :param height: The height of the cameras view
        """
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        """
        Applies the camera's focus on the target entity
        :param entity: The focus of the camera
        :return: The entity's rect moved according to the camera position
        """
        # Applies the camera offset to the entity
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        """
        Applies the camera's focus on the target rectangle
        :param rect: The focus of the camera
        :return: The moved rectangle according to the camera's position
        """
        # Applies the camera offset to 
        # a rectangle
        return rect.move(self.camera.topleft)

    def apply_vec(self, vector):
        tl = vec(self.camera.topleft)
        return vector + tl

    def update(self, target):
        """
        Updates the location of the camera relative to the target
        :param target: The focus of the camera
        :return: None
        """
        # Get how much the target moved in the x & y 
        # Objects that the pass by the target move in the opposite direction of the target
        x = -target.rect.centerx + (WIDTH // 2)
        y = -target.rect.centery + (HEIGHT // 2)

        # Limit the scrolling on all four sides of the screen
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom

        # Update the camera
        self.camera = pg.Rect(x, y, self.width, self.height)
