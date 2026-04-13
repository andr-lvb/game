import pygame as pg
import const as cn
from random import randint
from objects import Platform, Ball, Block, Text, Button, Fire_ball , Explosion
from math import hypot

class Game:
    game_mode = ''
    pause = pg.K_p
    def __init__(self):
        self.paused = False
        self.key_restart = False
        self.restart = pg.K_r
        self.key_pause = False
        self.start_state = 'menu'
        self.state = ''

        self.explosions = []


        self.platform = Platform(
            (cn.WIDTH-cn.PLATFORM_WIDTH)//2,
            cn.HEIGHT-cn.PLATFORM_BUTTOM_OFFSET,
            cn.PLATFORM_WIDTH,
            cn.PLATFORM_HEIGHT,
            cn.PLATFORM_SPEED,
            cn.PLATFORM_COLOR
        )


        self.balls = [Fire_ball(
            self.platform.rect.centerx,
            self.platform.rect.top - cn.BALL_RADIUS,
            cn.BALL_RADIUS,
            cn.BALL_SPEED_X,
            cn.BALL_SPEED_Y,
            cn.BALL_COLOR,
            cn.BALL_COLOR2
        )]


        self.blocks = []
        self.total_blocks = cn.BLOCK_COLS * cn.BLOCK_ROWS

        for row in range(cn.BLOCK_ROWS):
            for col in range(cn.BLOCK_COLS):
                x = cn.BLOCK_LEFT_OFFSET + col * (cn.BLOCK_WIDTH + cn.BLOCK_SPACING)
                y = cn.BLOCK_TOP_OFFSET + row * (cn.BLOCK_HEIGHT + cn.BLOCK_SPACING)

                if self.game_mode == 'classic':
                    number = 0
                else:
                    number = randint(1,21)
                    if number not in (1,2):
                        number = 0


                block = Block(x, y, cn.BLOCK_WIDTH, cn.BLOCK_HEIGHT, cn.COLOR_BLOCK)
                block.bonus = number
                self.blocks.append(block)


        self.text_win = Text(
            cn.TEXT_X_MAIN_TEXT,
            cn.TEXT_Y_MAIN_TEXT,
            cn.TEXT_COLOR,
            cn.FONT_SIZE_TO_MAIN,
            'You Win'
        )


        self.text_game_over = Text(
            cn.TEXT_X_MAIN_TEXT,
            cn.TEXT_Y_MAIN_TEXT,
            cn.TEXT_COLOR,
            cn.FONT_SIZE_TO_MAIN,
            'Game Over'
        )


        self.Start_game = Button(
            cn.BUTTON_COLOR,
            cn.BUTTON_X,
            cn.BUTTON_START_Y,
            cn.BUTTON_WIDTH,
            cn.BUTTON_HEIGHT,
            'Start new game with buf',
            20
        )


        self.Start_classic_game = Button(
            cn.BUTTON_COLOR,
            cn.BUTTON_X,
            cn.BUTTON_START_CLS_Y,
            cn.BUTTON_WIDTH,
            cn.BUTTON_HEIGHT,
            'Start classic game',
            20
        )


        self.Shortcut_keys = Button(
            cn.BUTTON_COLOR,
            cn.BUTTON_X,
            cn.BUTTON_HOT_KEYS_Y,
            cn.BUTTON_WIDTH,
            cn.BUTTON_HEIGHT,
            'Shortcut keys',
            20
        )


        self.text_shortcut_key_pause = Text(
            cn.TEXT_X_SHORTCUT_KEYS,
            cn.TEXT_Y_SHORTCUT_KEYS_PAUSE,
            cn.TEXT_COLOR,
            cn.TEXT_SIZE_TO_SHORTCUT_KEYS,
            'Для того что бы остановить игру нажмите английскую:'
        )


        self.button_shortcut_key_pause = Button(
            cn.BUTTON_COLOR,
            cn.BUTTON_SHORTCUT_KEY_PAUSE_X,
            cn.BUTTON_SHORTCUT_KEY_PAUSE_Y,
            cn.BUTTON_SHORTCUT_KEY_WIDTH,
            cn.BUTTON_SHORTCUT_KEY_HEIGHT,
            'P',
            20

        )


        self.text_shortcut_key_restart = Text(
            cn.TEXT_X_SHORTCUT_KEYS,
            cn.TEXT_Y_SHORTCUT_KEYS_RESTART,
            cn.TEXT_COLOR,
            cn.TEXT_SIZE_TO_SHORTCUT_KEYS,
            'Для того что бы вернутся в меню нажмите английскую:'
        )


        self.button_shortcut_key_restart = Button(
            cn.BUTTON_COLOR,
            cn.BUTTON_SHORTCUT_KEY_RESTART_X,
            cn.BUTTON_SHORTCUT_KEY_RESTART_Y,
            cn.BUTTON_SHORTCUT_KEY_WIDTH,
            cn.BUTTON_SHORTCUT_KEY_HEIGHT,
            'R',
            20

        )


        self.button_back = Button(
            cn.BUTTON_COLOR,
            cn.BUTTON_BACK_X,
            cn.BUTTON_BACK_Y,
            cn.BUTTON_WIDTH,
            cn.BUTTON_HEIGHT,
            'назад в меню',
            20
        )











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

                    block.alive = False
                    self.platform_sound.play()
                    self.total_blocks -= 1

                    if isinstance(ball, Fire_ball):
                        self.explosion(block)
                        self.explosions.append(Explosion(
                            block.rect.centerx,block.rect.centery
                        ))

                    if block.bonus in (1,2):
                        self.spawn_from_bonus_block(
                            block.rect.centerx ,
                            block.rect.centery)

                    ball.change_y()
                    break


    def collid_two_balls(self,ball1,ball2):
        dx = ball2.x - ball1.x
        dy = ball2.y - ball1.y
        dist = hypot(dx,dy)
        if dist > ball1.radius + ball2.radius:
            return
        if dist == 0:
            return
        nx = dx / dist
        ny = dy / dist
        tx = -ny
        ty = nx
        v1t = ball1.speed_x * tx + ball1.speed_y * ty
        v2t = ball2.speed_x * tx + ball2.speed_y * ty
        v1n = ball1.speed_x * nx + ball1.speed_y * ny
        v2n = ball2.speed_x * nx + ball2.speed_y * ny
        if v2n - v1n >= 0:
            return

        v1n , v2n = v2n , v1n
        ball1.speed_x = v1n * nx + v1t * tx
        ball1.speed_y = v1n * ny + v1t * ty
        ball2.speed_x = v2n * nx + v2t * tx
        ball2.speed_y = v2n * ny + v2t * ty
        overlap = ball1.radius + ball2.radius - dist
        if overlap > 0:
            correction = overlap / 2
            ball1.x -= nx * correction
            ball1.y -=  ny * correction
            ball2.x += tx * correction
            ball2.y += ty * correction


    def collid_for_balls(self):
        for i in range(len(self.balls)):
            for b in range(i+1,len(self.balls)):
                self.collid_two_balls(self.balls[i], self.balls[b])


    def explosion(self,block):
        for b in self.blocks:
            if not b.alive:
                continue
            if abs(b.rect.x - block.rect.x) <= cn.BLOCK_WIDTH + cn.BLOCK_SPACING and abs(b.rect.y - block.rect.y) <= cn.BLOCK_HEIGHT + cn.BLOCK_SPACING:
                if block.bonus != 0:
                    self.spawn_from_bonus_block(block.rect.centerx,block.rect.centery )
                b.alive = False
                self.total_blocks -= 1


    def spawn_fire_ball(self,x,y):
        self.balls.append(
            Fire_ball(
                x,
                y,
                cn.BALL_RADIUS,
                cn.BALL_SPEED_X,
                cn.BALL_SPEED_Y,
                cn.BALL_COLOR,
                cn.BALL_COLOR2
            )
        )


    def spawn_from_bonus_block(self,x,y):
        if randint(1,10) == 1:
            self.spawn_fire_ball(x,y)
        else:
            self.balls.append(
                Ball(
                    x,
                    y,
                    cn.BALL_RADIUS,
                    cn.BALL_SPEED_X,
                    cn.BALL_SPEED_Y,
                    cn.BALL_COLOR
                )
            )












               # ОБНОВЛЕНИЕ

    def update(self,delta):
        for i in range(len(self.explosions)):
            expl = self.explosions[i]
            expl.update(delta)
            if expl.finished:
                del self.explosions[i]
        if self.paused:
            return

        i = 0
        while i < len(self.balls):
            ball = self.balls[i]
            if ball.y - ball.radius > cn.HEIGHT:
                del self.balls[i]
            else:
                i += 1
                ball.update(delta)

        if len(self.balls) == 0:
            self.state = 'lose'
            return

        if self.total_blocks == 0:
            self.state = 'win'
            return

        keys = pg.key.get_pressed()

        self.platform.update(keys,delta)
        self.collision_wall()
        self.collision_platform()
        self.collision_blocks()
        self.collid_for_balls()






                # ОТРИСОВКА

    def draw(self,screen):
        screen.fill((255, 255, 255))
        if self.start_state == 'menu':
            self.Start_game.draw(screen)
            self.Start_classic_game.draw(screen)
            self.Shortcut_keys.draw(screen)
        if self.start_state == 'play':
            self.platform.draw(screen)

            for ball in self.balls:
                ball.draw(screen)

            for block in self.blocks:
                if block.alive:
                   block.draw(screen)

            for expl in self.explosions:
                expl.draw(screen)

        if self.start_state == 'settings':
            self.text_shortcut_key_pause.draw(screen)
            self.text_shortcut_key_restart.draw(screen)
            self.button_shortcut_key_pause.draw(screen)
            self.button_shortcut_key_restart.draw(screen)
            self.button_back.draw(screen)


        if self.state == 'win':
            self.text_win.draw_in_center(screen, cn.WIDTH//2, cn.HEIGHT//2)
        elif self.state == 'lose':
            self.text_game_over.draw_in_center(screen, cn.WIDTH//2, cn.HEIGHT//2)



    def handler_event(self,event):
        if event.type == pg.KEYDOWN:
            if self.key_restart:
                print(1)
                self.restart = event.key
                self.key_restart = False
            if event.key == self.restart:
                self.__init__()
            if self.key_pause:
                print(1)
                self.pause = event.key
                self.key_pause = False
                self.button_shortcut_key_pause.text =  pg.key.name(self.pause).upper()

            if event.key == self.pause:

                self.paused = not self.paused
                if self.paused:
                    pg.mixer.music.pause()
                else:
                    pg.mixer.music.unpause()


        if event.type == pg.MOUSEBUTTONDOWN:
            if self.start_state == 'menu':
                if self.Start_game.rect.collidepoint(event.pos):
                    self.game_mode = 'bonus'
                    self.__init__()
                    self.start_state = 'play'
                    self.paused = False
                if self.Start_classic_game.rect.collidepoint(event.pos):
                    self.game_mode = 'classic'
                    self.__init__()
                    self.start_state = 'play'
                    self.paused = False
                if self.Shortcut_keys.rect.collidepoint(event.pos):
                    self.start_state = 'settings'
                    self.paused = False
            elif self.start_state == 'settings':
                if self.button_shortcut_key_restart.rect.collidepoint(event.pos):
                    self.key_restart = True
                if self.button_shortcut_key_pause.rect.collidepoint(event.pos):
                    self.button_shortcut_key_pause.text = ''
                    self.key_pause = True
                if self.button_back.rect.collidepoint(event.pos):
                    self.start_state = 'menu'

