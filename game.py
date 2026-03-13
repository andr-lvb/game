import pygame as pg
import const as cn

pg.init()
screen = pg.display.set_mode((cn.WIDTH,cn.HEIGHT))
pg.display.set_caption('game')
clock = pg.time.Clock()
font = pg.font.SysFont('Arial' , 40)
running = True




while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    clock.tick(cn.FPS)