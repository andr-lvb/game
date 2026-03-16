import pygame as pg
import const as cn
from game import Game

pg.init()
screen = pg.display.set_mode((cn.WIDTH,cn.HEIGHT))
pg.display.set_caption('game')
clock = pg.time.Clock()


running = True
game = Game()



while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    game.update()
    game.draw(screen)
    pg.display.flip()
    clock.tick(cn.FPS)