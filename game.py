import pygame as pg
import const as cn
from random import randint
from objects import Platform , Ball , Block , Text

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
        
        self.balls = [Ball(
            self.platform.rect.centerx,
            self.platform.rect.top - cn.BALL_RADIUS,
            cn.BALL_RADIUS,
            cn.BALL_SPEED_X,
            cn.BALL_SPEED_Y,
            cn.BALL_COLOR
        )]

        self.blocks = []
        self.total_blocks = cn.BLOCK_COLS * cn.BLOCK_ROWS

        for row in range(cn.BLOCK_ROWS):
            for col in range(cn.BLOCK_COLS):
                x = cn.BLOCK_LEFT_OFFSET + col * (cn.BLOCK_WIDTH + cn.BLOCK_SPACING)
                y = cn.BLOCK_TOP_OFFSET + row * (cn.BLOCK_HEIGHT + cn.BLOCK_SPACING)
                number = randint(1,5)
                if number not in (1,2):
                    number = 0

                block = Block(x, y, cn.BLOCK_WIDTH, cn.BLOCK_HEIGHT, cn.COLOR_BLOCK)
                block.bonus = number
                self.blocks.append(block)


        self.state = 'play'
        self.text_win = Text(
            cn.TEXT_X,
            cn.TEXT_Y,
            cn.TEXT_COLOR,
            cn.FONT_SIZE,
            'You Win'
        )


        self.game_over = Text(
            cn.TEXT_X,
            cn.TEXT_Y,
            cn.TEXT_COLOR,
            cn.FONT_SIZE,
            'Game Over'
        )

        self.paused = False


                # МУЗЫКА

        self.start_background_music()
        self.load_effect_sound()

    def start_background_music(self):
        if not pg.mixer.get_init():
            return
        pg.mixer.music.load('assets/moodmode-8-bit-arcade-mode-158814.mp3')
        pg.mixer.music.set_volume(0.15)
        pg.mixer.music.play(-1,fade_ms=1000)

    def load_effect_sound(self):
        if not pg.mixer.get_init():
            return
        self.platform_sound = pg.mixer.Sound('assets/hitting-the-ball-with-an-aluminum-bat (mp3cut.net).wav')
        self.platform_sound.set_volume(0.3)




                # ФУНКЦИИ СТОЛКНОВЕНИЙ

    def collision_wall(self):
        for ball in self.balls:
            if ball.x + ball.radius >= cn.WIDTH:
                ball.x = cn.WIDTH - ball.radius
                ball.change_x()
            if ball.y - ball.radius <= 0:
                ball.y = ball.radius
                ball.change_y()
            if ball.x - ball.radius <= 0:
                ball.x = ball.radius
                ball.change_x()

    def collision_platform(self):
        for ball in self.balls:
            rect_ball = ball.get_rect()
            if rect_ball.colliderect(self.platform.rect):
                self.platform_sound.play()
                ball.y = self.platform.rect.top - ball.radius
                ball.change_y()
                offset = ball.x - self.platform.rect.centerx
                dol = offset/(self.platform.rect.width/2)
                ball.speed_x = dol * cn.BALL_SPEED_X

    def collision_blocks(self):
        for ball in self.balls:
            rect_ball = ball.get_rect()
            for block in self.blocks:
                if block.alive and rect_ball.colliderect(block.rect):
                    if block.bonus in (1,2):
                        for _ in range(block.bonus):
                            self.balls.append(Ball(
                                self.platform.rect.centerx,
                                self.platform.rect.top - cn.BALL_RADIUS,
                                cn.BALL_RADIUS,
                                cn.BALL_SPEED_X,
                                cn.BALL_SPEED_Y,
                                cn.BALL_COLOR
                            ))

                    self.platform_sound.play()
                    block.alive = False
                    self.total_blocks -= 1
                    ball.change_y()
                    break




               # ОБНОВЛЕНИЕ

    def update(self,delta):
        i = 0
        while i < len(self.balls):
            ball = self.balls[i]
            if ball.y - ball.radius > cn.HEIGHT:
                del self.balls[i]
            else:
                i += 1
                if len(self.balls) == 0:
                    self.state = 'lose'
                    return
            ball.update(delta)


        if self.total_blocks == 0:
            self.state = 'win'
            return

        if self.paused:
            return



        keys = pg.key.get_pressed()

        self.platform.update(keys,delta)
        self.collision_wall()
        self.collision_platform()
        self.collision_blocks()
        self.state = 'play'




                # ОТРИСОВКА

    def draw(self,screen):
        screen.fill((255, 255, 255))
        if self.state == 'play':
            self.platform.draw(screen)
            for ball in self.balls:
                ball.draw(screen)

            for block in self.blocks:
                if block.alive:
                   block.draw(screen)

        elif self.state == 'win':
            self.text_win.draw(screen)
        elif self.state == 'lose':
            self.game_over.draw(screen)



    def handler_event(self,event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                self.__init__()
            if event.key == pg.K_p:
                self.paused = not self.paused
                if self.paused:
                    pg.mixer.music.pause()
                else:
                    pg.mixer.music.unpause()









