import pygame as pg
import const as cn
from game import Game


# инциализация для музыки
pg.mixer.pre_init(44100,-16,2,512)
pg.init()


screen = pg.display.set_mode((cn.WIDTH,cn.HEIGHT))
clock = pg.time.Clock()


running = True
state = 'play'
game = Game()


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        game.handler_event(event)



    delta = clock.tick(cn.FPS) / 1000
    state = game.update(delta)
    game.draw(screen)
    pg.display.flip()
    fps = clock.get_fps()
    pg.display.set_caption(f'Arkanoid | fps {fps:.0f} | time {delta:.3f} ms')