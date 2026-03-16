import  pygame as pg
import const as cn

class Platform:
    def __init__(self,x,y,width,height,speed,color):
        self.rect = pg.Rect(x,y,width,height)
        self.speed = speed
        self.color = color


    def update(self,keys):
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.rect.x += self.speed

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > cn.WIDTH:
            self.rect.right = cn.WIDTH


    def draw(self,screen):
        pg.draw.rect(screen,self.color,self.rect,border_radius = 5)



class Button:
    def __init__(self,color,x,y,width,height,text,font):
        self.color = color
        self.rect = pg.Rect(x,y,width,height)
        self.text = text
        self.font = font

    def draw(self,screen):
        pg.draw.rect(screen,self.color,self.rect,border_radius=5)
        text_surface = self.font.render(self.text,True,cn.TEXT_COLOR)
        screen.blit(text_surface,(
                self.rect.centerx - text_surface.get_width()//2),
                self.rect.centery - text_surface.get_width()//2)



class Ball:
    def __init__(self,x,y,radius,speed,color):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.color = color

    def update(self):
        self.x = self.speed
        self.y = self.speed

    def draw(self,screen):





class Block:
    def __init__(self,x,y,width,height,color):
        self.rect = pg.Rect(x,y,width,height)
        self.color = color
        self.alive = True

    def draw(self,screen):
        if self.alive:
            pg.draw.rect(screen,self.color,self.rect)

class Text:
    def __init__(self,x,y,color,font_size,text):
        self.font_size =
        self.x = x
        self.y = y
        self.color = color
        self.text = text

    def draw(self,screen):
        text_surface = pg.font.render(self.text,True,self.color)
        pg.blit(text_surface,(self.x,self.y))