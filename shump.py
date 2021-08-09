# R37OOP3D by septahelix (c) copyright 2018 Licensed under a Creative Commons
# Attribution Noncommercial  (3.0) license.
# http://dig.ccmixter.org/files/septahelix/58719

import pygame
import random
import os
import time

#========Constants=========
APP_NAME = "Shoot"
WIDTH = 480
HEIGHT = 600
FPS = 60
#==========Colors==========
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
#===========================
pygame.init()
pygame.mixer.init()
display = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(APP_NAME)
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')

#drawing text on screen
def draw_text(surface,text,size,x,y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,WHITE)
    text_rect = text_surface.get_rect()
    text_rect.center = (int(x), int(y))
    # text_rect.y = int(y)
    surface.blit(text_surface,text_rect)

def draw_shieldbar(surface,x,y,pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct/100)*BAR_LENGTH
    pygame.draw.rect(surface,GREEN,[x,y,fill,BAR_HEIGHT])
    pygame.draw.rect(surface,WHITE,[x,y,BAR_LENGTH,BAR_HEIGHT],1)

def newmob():
    m = Mob()
    all_sprites.add(m)
    all_mobs.add(m)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(50,38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.shield = 100
        self.speedx = 0
        self.shoot_delay = 250
        self.last_shoot = pygame.time.get_ticks()

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            self.last_shoot = now
            bullet = Bullet(self.rect.centerx,self.rect.top)
            all_sprites.add(bullet)
            all_bullets.add(bullet)
            shoot_sound.play()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_org = random.choice(meteor_images)#pygame.transform.scale(meteor_image,(40,40))
        self.image_org.set_colorkey(BLACK)
        self.image = self.image_org.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*0.85/2)
        # pygame.draw.circle(self.image,GREEN,self.rect.center,self.radius)
        self.rect.x = random.randrange(0,WIDTH-self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedx = random.randrange(-3,3)
        self.speedy = random.randrange(1,8)
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last_updated = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_updated > 100:
            self.last_updated = now
            self.rot = (self.rot + self.rot_speed) % 360
            newimage = pygame.transform.rotate(self.image_org,self.rot)
            old_center = self.rect.center
            self.image = newimage
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.y > HEIGHT + 40 or self.rect.right < -35 or self.rect.left > WIDTH+40:
            self.rect.x = random.randrange(0,WIDTH-self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedx = random.randrange(-3,3)
            self.speedy = random.randrange(2,8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        #kill it if it crosses upper boundary
        if self.rect.bottom < 0:
            self.kill()


#graphics and sound folder setting
img_dir = os.path.join(os.path.dirname(__file__),'img')
sound_dir = os.path.join(os.path.dirname(__file__),'sound')

#loading all graphics images
background = pygame.image.load(os.path.join(img_dir,'background.png')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(os.path.join(img_dir,'playerShip2_blue.png')).convert()
#meteor_img = pygame.image.load(os.path.join(img_dir,'meteorBrown_big4.png')).convert()
bullet_img = pygame.image.load(os.path.join(img_dir,'laserRed16.png')).convert()
meteor_images = []
meteor_list = ['meteorBrown_big3.png','meteorBrown_big4.png',
                'meteorBrown_med1.png','meteorBrown_med3.png','meteorBrown_small1.png',
                'meteorGrey_big3.png','meteorGrey_big4.png','meteorGrey_med2.png']
for image in meteor_list:
    meteor_images.append(pygame.image.load(os.path.join(img_dir,image)).convert())
#load all sounds files
shoot_sound = pygame.mixer.Sound(os.path.join(sound_dir,'sfx_laser1.ogg'))
explosion_sound = pygame.mixer.Sound(os.path.join(sound_dir,'Explosion8.wav'))
pygame.mixer.music.load(os.path.join(sound_dir,'bg.wav'))
pygame.mixer.music.set_volume(0.01)

#grouping all objects
all_sprites = pygame.sprite.Group()
all_mobs = pygame.sprite.Group()
all_bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    newmob()
#game loop
gameExit = False
score = 0
pygame.mixer.music.play(loops=-1)
while not gameExit:
    #runs loop at a given speed
    clock.tick(FPS)
    #events check
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
    #update all_sprites
    all_sprites.update()
    #check to see if a mob colised with player
    hits = pygame.sprite.spritecollide(player,all_mobs,True,pygame.sprite.collide_circle)
    if hits:
        for hit in hits:
            player.shield -= hit.radius * 2
            newmob()
            if player.shield < 0:
                gameExit = True
                gameOver = True
                while gameOver:
                    display.fill(BLACK)
                    draw_text(display,"You scored {} points".format(score),18,WIDTH/2,HEIGHT/2)
                    pygame.display.update()
                    time.sleep(1)
                    gameOver = False
    #check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(all_mobs,all_bullets,True,True)
    for hit in hits:
        score += 50 - hit.radius
        #explosion_sound.play()
        newmob()
    #draw all_sprites
    display.blit(background,background_rect)
    all_sprites.draw(display)
    draw_text(display,'Score : {}'.format(score),18,10,25)
    draw_shieldbar(display,10,10,player.shield)
    pygame.display.update()

pygame.quit()
