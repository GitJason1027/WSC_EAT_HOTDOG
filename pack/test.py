import pygame
from sys import exit
from random import randint
import time
from pygame.locals import *

class Wsc(pygame.sprite.Sprite):
    def __init__(self,wsc_surface,wsc_init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = wsc_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = wsc_init_pos


    def move(self,offset):
        x = self.rect.left + offset[pygame.K_RIGHT] - offset[pygame.K_LEFT]
        if x < 0:
            self.rect.left = 0
        elif x > SCREEN_WIDTH - self.rect.width:
            self.rect.left =  SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left = x

class Hotdog(pygame.sprite.Sprite):
    def __init__(self,hotdog_surface,hotdog_init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = hotdog_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = hotdog_init_pos
        self.eaten = 0

    def update(self):
        self.rect.top += HOTDOG_SPEED
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def eat(self,wsc):
        if wsc.rect.top+10<self.rect.bottom and wsc.rect.left+35<self.rect.centerx<wsc.rect.right-35:
            self.eaten+=1

class Score_plus(pygame.sprite.Sprite):
    def __init__(self,sp_surface,sp_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = sp_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = sp_pos
        self.time = time.time()

    def update(self):
        if time.time()-self.time > 1:
            self.kill()


#设置窗口分辨率
SCREEN_WIDTH = 432
SCREEN_HEIGHT = 640

#帧率
FRAME_RATE = 60

#初始化参数
offset = {pygame.K_LEFT:0, pygame.K_RIGHT:0, pygame.K_UP:0, pygame.K_DOWN:0}
speed = 2
clock = pygame.time.Clock()
ticks = 0
HOTDOG_SPEED = 4
WSC_SPEED = 5
EATEN_PER = 15

#初始化
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
pygame.display.set_caption('wsc eats hotdog')

#文字
font = pygame.font.SysFont('微软雅黑',25)

#背景图
bg = pygame.image.load('pic/bg.jpg')

#素材图
p1_img = pygame.image.load('pic/p1.png')
p1_img = pygame.transform.scale(p1_img,(50,50))
p1_group = pygame.sprite.Group()

wsc_img = pygame.image.load('pic/wsc.png')
wsc_img = pygame.transform.scale(wsc_img,(90,90))
wsc_pos = [SCREEN_WIDTH/2-45,SCREEN_HEIGHT-95]
wsc = Wsc(wsc_img,wsc_pos)

hotdog_img = pygame.image.load('pic/hotdog.png')
hotdog_img = pygame.transform.scale(hotdog_img,(57,57))

hotdogs_group = pygame.sprite.Group()

SCORE = 0
def collide_wsc_hotdog(wsc,hd):
    global SCORE
    if hd.eaten<=EATEN_PER:
        return False
    else:
        SCORE+=1
        p1_group.add(Score_plus(p1_img,(wsc.rect.left-10,wsc.rect.top-40)))
        return True

pre_time = time.time()
while True:
    clock.tick(30)
    #分数文字
    text = font.render('Score:'+str(SCORE), True, (0, 0, 0))

    #绘制屏幕
    screen.blit(bg,(0,0))

    if time.time()-pre_time > 1.5:
        hotdog_pos = [randint(10, SCREEN_WIDTH - hotdog_img.get_width()-10), -hotdog_img.get_height()]
        hotdog = Hotdog(hotdog_img, hotdog_pos)
        hotdogs_group.add(hotdog)
        pre_time = time.time()
    hotdogs_group.update()
    hotdogs_group.draw(screen)

    for i in hotdogs_group:
        i.eat(wsc)

    #注意图层额顺序，后画的在上层
    screen.blit(wsc.image, wsc.rect)
    screen.blit(text, (10, 10))

    #检测游戏退出事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key in offset:
                offset[event.key] = WSC_SPEED
            elif event.key == pygame.K_1:
                WSC_SPEED +=1
            elif event.key == pygame.K_2:
                WSC_SPEED -=1
            elif event.key == pygame.K_3:
                HOTDOG_SPEED +=1
            elif event.key == pygame.K_4:
                HOTDOG_SPEED -=1
            elif event.key == pygame.K_5:
                EATEN_PER +=1
            elif event.key == pygame.K_6:
                EATEN_PER -=1
        elif event.type == pygame.KEYUP:
            if event.key in offset:
                offset[event.key] = 0
    wsc.move(offset)

    pygame.sprite.spritecollide(wsc,hotdogs_group,True,collide_wsc_hotdog)
    p1_group.update()
    p1_group.draw(screen)

    # 更新屏幕
    pygame.display.update()

