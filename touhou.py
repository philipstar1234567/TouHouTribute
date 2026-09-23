import pygame as pg
from pygame import * 
import math as m
from math import *
import random as rd
from random import *
import os

pg.init()
pg.font.init()
pg.mixer.init()

script_dir = os.path.dirname(os.path.abspath(__file__))
song_path = os.path.join(script_dir, "A_Soul_as_Red_as_a_Ground_Cherry.mp3")
pg.mixer.music.load(song_path)
pg.mixer.music.play(loops=-1)

clock = pg.time.Clock()
FPS = 60

bredde = 0
hoyde = 0
vindu = pg.display.set_mode([bredde, hoyde])
print(type(vindu))

Enemies = pg.sprite.Group()
Bullets = pg.sprite.Group()
lives = 3

font = pg.font.Font(os.path.join(script_dir, "YOZAKURA-Regular.otf"), 100)
smallfont = pg.font.Font(os.path.join(script_dir, "YOZAKURA-Regular.otf"), 40)
gameovertext = font.render("GAME OVER", False, (255, 255, 255))
gameoverrect = gameovertext.get_rect(center=(vindu.get_width()/2, vindu.get_height()/2))

class Player():
    def __init__(self, x, y, bredde, hoyde, vel, lives):
        self.x = x
        self.y = y
        self.bredde = bredde
        self.hoyde = hoyde
        self.vel = vel
        self.lives = lives
        self.score = 0
        self.timer = 60
        
        self.rect = pg.Rect(self.x, self.y, self.bredde, self.hoyde)
        
    def Draw(self):
        pg.draw.rect(vindu, (0, 255, 255), (self.x, self.y, self.bredde, self.hoyde))
        self.rect = pg.Rect(self.x, self.y, self.bredde, self.hoyde)
        
    def Move(self, keys):
        original_vel = self.vel
        if keys[K_RSHIFT] or keys[K_LSHIFT]:
            self.vel = self.vel/3
        if keys[K_w] and self.y > 0:
            self.y -= self.vel
        if keys[K_s] and self.y < vindu.get_height()-self.hoyde:
            self.y += self.vel
        if keys[K_a] and self.x > 0:
            self.x -= self.vel
        if keys[K_d] and self.x < vindu.get_width()-self.bredde:
            self.x += self.vel
        self.vel = original_vel
        
    def Hit(self, hitter):
        hitter.kill()
        self.lives -= 1
        
    def Score(self, difficulty):
        pointtimer = 60
        if self.timer == 0:
            self.score += 1
            self.timer = pointtimer
            Spawn(difficulty)
        else:
            self.timer -= 1
        
class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y, size, vel, farge, cd, b_vel, b_size):
        super().__init__()
        self.x = x
        self.y = y
        self.size = size
        self.vel = vel
        self.farge = farge
        self.cd = cd
        self.orig_cd = cd
        self.b_vel = b_vel
        self.b_size = b_size
        
        Enemies.add(self)
        
    def FindCoords(self):
        tip = (self.x, self.y+(self.size*2))
        left = (self.x-self.size, self.y-(self.size*2))
        right = (self.x+self.size, self.y-(self.size*2))
        
        return (tip, left, right)
        
    def Draw(self):
        pg.draw.polygon(vindu, self.farge, self.FindCoords())
        
    def Move(self):
        if self.y - self.size < vindu.get_height():
            self.y += self.vel
        else:
            self.kill()
            
    def Shoot(self, playerpos):
        if self.cd > 0:
            self.cd -= 1
        else:
            bullet = Bullet(self.x, self.y, playerpos[0], playerpos[1], self.b_vel, self.b_size)
            self.cd = self.orig_cd

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, px, py, vel, size):
        super().__init__()
        self.x = x
        self.y = y
        self.vel = vel
        self.size = size
        self.px = px
        self.py = py
        self.lifeholder = lives
        self.dir = (px - x, py - y)  
        self.len = m.sqrt(self.dir[0]**2 + self.dir[1]**2)
        
        self.rect = pg.Rect(self.x, self.y, (self.size/2)*sqrt(2), (self.size/2)*sqrt(2), center=(self.x, self.y))
        self.rect.center = (self.x, self.y)
        
        Bullets.add(self)
        
    def Move(self):
        self.x += self.vel * (self.dir[0] / self.len)
        self.y += self.vel * (self.dir[1] / self.len)        
        if self.x < 0 or self.x > vindu.get_width() or self.y < 0 or self.y > vindu.get_height():
            self.kill()
            
    def Draw(self):
        pg.draw.circle(vindu, (255, 255, 255), (self.x, self.y), self.size)
        pg.draw.circle(vindu, (0, 0, 0), (self.x, self.y), self.size/2)
        self.rect = pg.Rect(self.x, self.y, (self.size/2)*sqrt(2), (self.size/2)*sqrt(2))
        self.rect.center = (self.x, self.y)
        
        
def Iterate_Enemies():
    for enemy in Enemies.sprites():
        enemy.Move()
        enemy.Draw()
        enemy.Shoot((player.x, player.y))
        
def Iterate_Bullets():
    for bullet in Bullets.sprites():
        bullet.Move()
        bullet.Draw()
        if bullet.rect.colliderect(player.rect):
            player.Hit(bullet)

difficulty = 1
def Write():
    lifetext = smallfont.render(f"LIVES: {player.lives}", False, (255, 255, 255))
    liferect = lifetext.get_rect(topleft=(0, 0))
    scoretext = smallfont.render(f"SCORE: {player.score}", False, (255, 255, 255))
    scorerect = scoretext.get_rect(topleft=(0, lifetext.get_height()))
    difftext = smallfont.render(f"DIFFICULTY: {difficulty}", False, (255, max(255-difficulty, 0), max(255-difficulty, 0)))
    diffrect = difftext.get_rect(topleft=(0, lifetext.get_height()+scoretext.get_height()))
    vindu.blit(lifetext, liferect)
    vindu.blit(scoretext, scorerect)
    vindu.blit(difftext, diffrect)
    
def Spawn(difficulty):
    rate = 49 + m.ceil(difficulty/4)
    pull = rd.randint(1, 100)
    if pull < rate:
        enemy = Enemy(rd.randint(10, vindu.get_width()-10), 0, 10, 2, (255, max(255-difficulty, 0), max(255-difficulty, 0)), max(100-m.ceil(difficulty/3), 0), 2, 6)
    if pull in [1, 2, 3]:
        if difficulty < 100:
            enemy = Enemy(rd.randint(10, vindu.get_width()-10), 0, 20, 5, (0, 0, 0), 0, 3, 6)
        else:
            enemy = Enemy(rd.randint(10, vindu.get_width()-10), 0, 20, 5, (0, 0, 0), 1, 3, 6)
            enemy = Enemy(rd.randint(10, vindu.get_width()-10), 0, 20, 5, (0, 0, 0), 1, 3, 6)
            enemy = Enemy(rd.randint(10, vindu.get_width()-10), 0, 20, 5, (0, 0, 0), 1, 3, 6)
    if pull in [4, 5, 6]:
        if difficulty < 100:
            enemy = Enemy(rd.randint(10, vindu.get_width()-10), 0, 15, 1, (255, 255, 0), 30, 8, 10)
        else:
            enemy = Enemy(rd.randint(10, vindu.get_width()-10), 0, 15, 1, (255, 255, 0), 30, 8, 10)
            enemy = Enemy(rd.randint(10, vindu.get_width()-10), 0, 15, 1, (255, 255, 0), 30, 8, 10)
            enemy = Enemy(rd.randint(10, vindu.get_width()-10), 0, 15, 1, (255, 255, 0), 30, 8, 10)
    if pull in [7, 8, 9]:
        if difficulty < 100:
            enemy = Enemy(rd.randint(10, vindu.get_width()-10), 0, 35, 1, (0, 255, 0), 60, 1, 60)
        else:
            enemy = Enemy(rd.randint(10, vindu.get_width()-10), 0, 35, 1, (0, 255, 0), 60, 1, 60)
            enemy = Enemy(rd.randint(10, vindu.get_width()-10), 0, 35, 1, (0, 255, 0), 60, 1, 60)
            enemy = Enemy(rd.randint(10, vindu.get_width()-10), 0, 35, 1, (0, 255, 0), 60, 1, 60)
            

player = Player(vindu.get_width()/2, vindu.get_height()/2, 20, 40, 6, 3)



gameloop = True
while gameloop:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameloop = False
    keys = pg.key.get_pressed()
    if keys[K_ESCAPE]:
        gameloop = False
        
    vindu.fill((0, 0, 100))
    Write()
    if player.lives > 0:
        player.Move(keys)
        player.Draw()
        difficulty = player.score
        if difficulty >= 255:
            difficulty = 255
        player.Score(difficulty)
        
        Iterate_Enemies()
        Iterate_Bullets()
    
    else:
        vindu.blit(gameovertext, gameoverrect)
        
    pg.display.flip()
pg.quit()