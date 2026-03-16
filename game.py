import pygame as pg
import const as cn
from objects import Platform

class Game:
    def __init__(self):
        self.platform = Platform(
            (cn.WIDTH-cn.PLATFORM_WIDTH)//2,
            cn.HEIGHT-cn.PLATFORM_BUTTOM_OFFSET,
            cn.PLATFORM_WIDTH,
            cn.PLATFORM_HEIGHT,
            cn.PLATFORM_SPEED,
            cn.PLATFORM_COLOR
        )


    def update(self):
        keys = pg.key.get_pressed()
        self.platform.update(keys)


    def draw(self,screen):
        screen.fill((255,255,255))
        self.platform.draw(screen)