#-------------------------------------------------------------------------------------------------------------
# Mendefinisikan Module Game
#-------------------------------------------------------------------------------------------------------------
import sys
import random

import pygame
from pygame.locals import *

pygame.init()

#-------------------------------------------------------------------------------------------------------------
# Mendefinisikan Asset Game
#-------------------------------------------------------------------------------------------------------------
player_ship = 'spaceShips_008.png'
enemy_ship1 = 'ship_sidesC.png'
enemy_ship2 = 'spaceships_007.png'
player_bullet = 'spaceMissiles_040.png'
enemy1_bullet = 'meteor_squareDetailedSmall.png'
bos_bullet = 'meteor_squareLarge.png'


#-------------------------------------------------------------------------------------------------------------
# Membuat Screen Game 
#-------------------------------------------------------------------------------------------------------------
screen = pygame.display.set_mode((0,0), FULLSCREEN)
s_width, s_height = screen.get_size()


#-------------------------------------------------------------------------------------------------------------
# Mendefinisikan Resolusi Game
#-------------------------------------------------------------------------------------------------------------
clock = pygame.time.Clock()
FPS = 60
font = pygame.font.Font(None, 32)

#-------------------------------------------------------------------------------------------------------------
# Mendefinisikan Group 
#-------------------------------------------------------------------------------------------------------------
background_grup = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy1_group = pygame.sprite.Group()
bos_group = pygame.sprite.Group()
playerbullet_group = pygame.sprite.Group()
enemy1bullet_group = pygame.sprite.Group()
bosbullet_group = pygame.sprite.Group()
sprite_group = pygame.sprite.Group()

#-------------------------------------------------------------------------------------------------------------
# Mendefinisikan Class Game
#-------------------------------------------------------------------------------------------------------------
class Background(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((x,y))
        self.image.fill('white')
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += 1
        self.rect.x += 0.5
        if self.rect.y >s_height:
            self.rect.y = random.randrange(-10,0)
            self.rect.x = random.randrange(-400,s_width)

class Player(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.image.set_colorkey('#000080')

    def update(self):
        mouse = pygame.mouse.get_pos()
        self.rect.x = mouse[0]
        self.rect.y = mouse[1]    

    def luncurkan(self):
        bullet = PlayerBullet(player_bullet)
        mouse = pygame.mouse.get_pos()
        bullet.rect.x = mouse[0]
        bullet.rect.y = mouse[1] 
        playerbullet_group.add(bullet)
        sprite_group.add(bullet)

class Enemy1(Player):
    def __init__(self, img):
        super().__init__(img)
        self.rect.x = random.randrange(0, s_width)
        self.rect.y = random.randrange(-500, 0)
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.y += 1
        if self.rect.y > s_height:
            self.rect.x = random.randrange(0, s_width)
            self.rect.y = random.randrange(-2000, 0)
        self.luncurkan()

    def luncurkan(self):
        if self.rect.y in (0, 30, 100, 500, 700,1000):
            enemy1bullet = Enemy1Bullet(enemy1_bullet)
            enemy1bullet.rect.x = self.rect.x
            enemy1bullet.rect.y = self.rect.y 
            enemy1bullet_group.add(enemy1bullet)
            sprite_group.add(enemy1bullet)

class Bos(Enemy1):
    def __init__(self, img):
        super().__init__(img)
        self.rect.x = -0
        self.rect.y = 200
        self.move = 1

    def update(self):
        self.rect.x += self.move
        if self.rect.x > s_height + 200:
            self.move = -1
        elif self.rect.x < -200:
            self.move *= -1    
        self.luncurkan()

    def luncurkan(self):
        if self.rect.x % 100 ==0:
            bosbullet = Enemy1Bullet(bos_bullet)
            bosbullet.rect.x = self.rect.x + 50
            bosbullet.rect.y = self.rect.y  + 70
            bosbullet_group.add(bosbullet)
            sprite_group.add(bosbullet)       

class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.image.set_colorkey('#000080')

    def update(self):
        self.rect.y -= 6
        if self.rect.y < 0:
            self.kill()

class Enemy1Bullet(PlayerBullet):
    def __init__(self, img):
        super().__init__(img)
        self.image.set_colorkey('white')
    def update(self):
        self.rect.y += 3
        if self.rect.y > s_height :
            self.kill()

class Game:
    def __init__(self):
        self.count_hit = 0
        self.count_hit2 = 0

        self.lives = 5
        self.run_game()

    def create_beckground(self):
        for i in range(50):
            x = random.randint(1,4)
            beckground_image = Background(x,x)
            beckground_image.rect.x = random.randrange(0, s_width)
            beckground_image.rect.y = random.randrange(0, s_height)
            background_grup.add(beckground_image)
            sprite_group.add(beckground_image)

    def create_player(self):
        self.player = Player(player_ship)
        
        player_group.add(self.player)
        sprite_group.add(self.player)

    def create_enemy1(self):
        for i in range(10):
            self.enemy1 = Enemy1(enemy_ship1)
            enemy1_group.add(self.enemy1)
            sprite_group.add(self.enemy1)

    def create_bos(self):
            for i in range(1):
                self.bos = Bos(enemy_ship2)
                bos_group.add(self.bos)
                sprite_group.add(self.bos)

    def playerbullet_hit_enemy1(self):
        hits = pygame.sprite.pygame.sprite.groupcollide(enemy1_group, playerbullet_group, False, True)
        for i in hits :
            self.count_hit += 1
            if self.count_hit == 2 :
                i.rect.x = random.randrange(0, s_width)
                i.rect.y = random.randrange(-3000,-100)
                self.count_hit = 0

    def playerbullet_hit_Bos(self):
        hits = pygame.sprite.groupcollide(bos_group, playerbullet_group, False, True)
        for i in hits :
            self.count_hit2 += 1
            if self.count_hit2 == 10:
                i.rect.x = -199
                self.count_hit2 = 0

    def enemy1bullet_hit_player(self):
        hits = pygame.sprite.spritecollide(self.player, enemy1bullet_group, True )
        if hits :
            self.lives -= 1
            if self.lives < 0:
                pygame.quit()
                sys.exit()

    def Bos_hit_player(self):
        hits = pygame.sprite.spritecollide(self.player, bosbullet_group, True)   
        if hits :
            self.lives -=2
            if self.lives < 0 :
                pygame.quit()
                sys.exit()         

    def create_lives(self):
        self.lives_img = pygame.image.load(player_ship)
        self.lives_img = pygame.transform.scale(self.lives_img , (40,40))
        n = 0
        for i in range (self.lives):
            screen.blit(self.lives_img, (0 + n, s_height-50))
            n+= 60

    def run_update(self):
        sprite_group.draw(screen)
        sprite_group.update()

    def run_game(self):
        self.create_beckground()
        self.create_player()
        self.create_enemy1()
        self.create_bos()
        while True:
            screen.fill('#000080')
            self.playerbullet_hit_enemy1()
            self.playerbullet_hit_Bos()
            self.enemy1bullet_hit_player()
            self.Bos_hit_player()
            self.create_lives()
            self.run_update()
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    self.player.luncurkan()
            pygame.display.update()
            clock.tick(FPS)

#-------------------------------------------------------------------------------------------------------------
# Running Game
#-------------------------------------------------------------------------------------------------------------
def main():
    game = Game()

if __name__=='__main__':
    main()  


                   