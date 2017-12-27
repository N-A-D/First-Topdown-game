import pygame as pg
import pytmx
from settings import WIDTH, HEIGHT


class TiledMap:
    def __init__(self, filename):
        self.tmxdata = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.tmxdata.width * self.tmxdata.tilewidth
        self.height = self.tmxdata.height * self.tmxdata.tileheight

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


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

    def apply_to_point(self, point):
        return [point[0] + self.camera.x, point[1] + self.camera.y]


    def apply_rect(self, rect, copy=False):
        """
        Applies the camera's focus on the target rectangle
        :param rect: The focus of the camera
        :return: The moved rectangle according to the camera's position
        """
        # Applies the camera offset to 
        # a rectangle
        if not copy:
            return rect.move(self.camera.topleft)
        else:
            x = rect.copy()
            return x.move(self.camera.topleft)

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
