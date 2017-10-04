import pygame as pg
import re
from os import listdir
from os.path import isfile, join

vec = pg.math.Vector2

def collide_hit_rect(first, second):
    """
    Call back function which checks if two rectangles have collided with each other
    :param first: the first rectangle
    :param second: the second rectangle
    :return: True if first collided with second. False otherwise
    """
    return first.hit_rect.colliderect(second.hit_rect) or first.hit_rect.colliderect(second.hit_rect)

def world_shift_pos(position, camera):
    vector = vec(position[0], position[1])
    vector.x -= camera.x
    vector.y -= camera.y
    return vector

def collide_with_obstacles(sprite, group, direction):
    """
    Checks where the sprite has collided with an obstacle
    
    direction is needed to allow a sprite that collides 
    horizontally to continue moving vertically if its movement
    was in a diagonal. Same goes for blocked vertical movement
    and continued horizontal movement.
    :param sprite: The sprite to check
    :param group: The group of obstacles to check
    :param direction: For vertical or horizontal movement
    :return: True if there is a collision. False otherwise
    """
    collided = False
    if direction == 'x':
        collided = True
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # If the sprite is moving right, stop it and
            # set its right face on the left side of the object it collided with.
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            # If the sprite is moving right, stop it and
            # set its left face on the left side of the object it collided with.
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            # Completely stop the sprite
            sprite.vel.x = 0
            # Update the sprite's center to the new position
            sprite.hit_rect.centerx = sprite.pos.x
    if direction == 'y':
        collided = True
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # If the sprite is moving upwards, then
            # set its top to the bottom of the sprite it collided with.
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            # If the sprite is moving downwards, then
            # set its bottom to the top of the sprite it collided with.
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            # Completely stop the sprite
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y
    return collided


def get_image_names(path, index=2):
    files = [file for file in listdir(path) if isfile(join(path, file))]
    return [path + file for file in sorted(files, key=lambda x: int(re.split(r'[_.]', x)[index]))]
