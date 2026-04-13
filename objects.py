from operator import index

import  pygame as pg
import const as cn

class Platform:
    def __init__(self,x,y,width,height,speed,color):
        self.rect = pg.Rect(x,y,width,height)
        self.speed = speed
        self.color = color

    def update(self,keys,delta):
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            self.rect.x -= self.speed * delta

        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.rect.x += self.speed * delta

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > cn.WIDTH:
            self.rect.right = cn.WIDTH

    def draw(self,screen):
        pg.draw.rect(screen,self.color,self.rect,border_radius = 5)





class Button:
    def __init__(self,color,x,y,width,height,text,font_size):
        self.color = color
        self.rect = pg.Rect(x,y,width,height)
        self.text = text
        self.font_size = font_size
        self.font = pg.font.SysFont(None,self.font_size)

    def draw(self,screen):
        pg.draw.rect(screen,self.color,self.rect,border_radius=5)
        text_surface = self.font.render(self.text,True,cn.TEXT_COLOR)
        screen.blit(text_surface,(
                self.rect.centerx - text_surface.get_width()//2,
                self.rect.centery - text_surface.get_height()//2))





class Ball:
    def __init__(self,x,y,radius,speed_x,speed_y,color):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = color

    def update(self,delta):
        self.x += self.speed_x * delta * 1.02
        self.y += self.speed_y * delta * 1.02

    def draw(self,screen):
        pg.draw.circle(screen,self.color,(int(self.x),int(self.y)),self.radius)

    def get_rect(self):
        return pg.Rect(self.x - self.radius,self.y - self.radius,self.radius*2,self.radius*2)

    def change_x(self):
        self.speed_x *= -1
    def change_y(self):
        self.speed_y *= -1


class Fire_ball(Ball):
    def __init__(self, x, y, radius, speed_x, speed_y, color1, color2):
        super().__init__(x, y, radius, speed_x, speed_y, color1)
        self.out_color = color2

    def draw(self, screen):
        pg.draw.circle(screen,self.out_color,(int(self.x),int(self.y)),self.radius+2)
        pg.draw.circle(screen,self.color,(int(self.x),int(self.y)),self.radius)



class Block:
    def __init__(self,x,y,width,height,color):
        self.rect = pg.Rect(x,y,width,height)
        self.color = color
        self.alive = True
        self._bonus = 0

    def draw(self,screen):
        if self.alive:
            if self.bonus != 0:
                pg.draw.rect(screen,(222,222,222),self.rect)
            else:
                pg.draw.rect(screen,self.color,self.rect)


    @property
    def bonus(self):
        return self._bonus
    @bonus.setter
    def bonus(self,value):
        self._bonus = value




class Text:
    def __init__(self,x,y,color,font_size,text):
        self.font_size = font_size
        self.x = x
        self.y = y
        self.color = color
        self.text = text
        self.font = pg.font.SysFont(None,self.font_size)

    def draw(self,screen):
        text_surface = self.font.render(self.text,True,self.color)
        screen.blit(text_surface,(self.x,self.y))

    def draw_in_center(self,screen,center_x,center_y):
        text_surface = self.font.render(self.text,True,self.color)
        text_rect = text_surface.get_rect(center=(center_x,center_y))
        screen.blit(text_surface,text_rect)



class Explosion:
    list_of_frames = []
    @classmethod
    def load_frames(cls):
        image = pg.image.load('assets/explosion_spritesheet.png').convert_alpha()
        frame_count = 8
        frame_width = image.get_width() // frame_count
        frame_height = image.get_height()
        for i in range(frame_count):
            frame = pg.Surface((frame_width,frame_height),pg.SRCALPHA)
            frame.blit(image,(0,0),(i*frame_width,0, frame_width,frame_height))
            cls.list_of_frames.append(frame)


    def __init__(self,x,y):
        self.load_frames()
        self.x = int(x)
        self.y = int(y)
        self.frame_duration = 0.05
        self.scale = 0.8
        self.frame_index = 0
        self.timer = 0
        self.finished = False
        self.scaled_img = []
        for frame in self.list_of_frames:
            self.scaled_img.append(pg.transform.smoothscale(frame, (frame.get_width()* self.scale, frame.get_height()* self.scale)))


    def update(self,delta):
        self.timer += delta
        while self.timer >= self.frame_duration and not self.finished:
            self.timer -= self.frame_duration
            self.frame_index += 1
            if self.frame_index >= len(self.scaled_img):
                self.finished = True


    def draw(self,screen):
        if self.finished:
            return
        img = self.scaled_img[self.frame_index]
        rect = img.get_rect(center=(self.x, self.y))
        screen.blit(img,rect)










