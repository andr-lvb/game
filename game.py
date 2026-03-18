import pygame as pg
import const as cn
from objects import Platform , Ball


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
        self.ball = Ball(
            self.platform.rect.centerx,
            self.platform.rect.top - cn.BALL_RADIUS,
            cn.BALL_RADIUS,
            cn.BALL_SPEED_X,
            cn.BALL_SPEED_Y,
            cn.BALL_COLOR
        )

    def collision_wall(self):
        if self.ball.x + self.ball.radius >= cn.WIDTH:
            self.ball.change_x()
        if self.ball.y - self.ball.radius <= 0:
            self.ball.change_y()
        if self.ball.x - self.ball.radius <= 0:
            self.ball.change_x()

    def collision_platform(self):
        rect_ball = self.ball.get_rect()
        if rect_ball.colliderect(self.platform.rect):
            self.ball.change_y()
            # self.ball.change_x()
            offset = self.ball.x - self.platform.rect.centerx
            dol = offset/(self.platform.rect.width/2)
            self.ball.speed_x = dol * cn.BALL_SPEED_X


    def update(self):
        keys = pg.key.get_pressed()
        self.platform.update(keys)
        self.ball.update()
        self.collision_wall()
        self.collision_platform()



    def draw(self,screen):
        screen.fill((255,255,255))
        self.platform.draw(screen)
        self.ball.draw(screen)
