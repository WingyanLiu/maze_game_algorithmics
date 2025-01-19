#Maze game algorithmic

import pygame
from sys import exit
from random import randint
from maze_game_classes import Wall
from maze_wall_generator import maze_wall_generator

map_x_dim = 500
map_y_dim = 500

pygame.init()
screen = pygame.display.set_mode((map_x_dim,map_y_dim))
pygame.display.set_caption("Maze")
global running
running = True
clock = pygame.time.Clock()

game_over_img = pygame.image.load("./images/game_over.jpg")
game_over_img = pygame.transform.scale(game_over_img,(map_x_dim,map_y_dim))
game_over = False

win_img = pygame.image.load("./images/winning_screen.png")
win_img = pygame.transform.scale(win_img,(map_x_dim,map_y_dim))
win = False



class Player(pygame.sprite.Sprite):
    def __init__(self,width,height):
        super().__init__()
        self.x_pos = 0
        self.y_pos = 0
        self.image = pygame.image.load("./images/ghost_blue.jpg").convert_alpha()
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(self.image,(self.width,self.height))
        self.rect = self.image.get_rect(topleft=(self.x_pos,self.y_pos))
        self.lastmove = ''
        self.orientation = 'right'
        self.speed = 4
        self.gameover =False
        self.win = False
    
    def action(self):
        key = pygame.key.get_pressed()
        if self.collide(walls)==False:
            if key[pygame.K_UP]:
                if self.rect.y >0:
                    self.rect.y -= self.speed
                else:
                    self.rect.y = 0
                self.lastmove = 'up'
                
            if key[pygame.K_DOWN]:
                if self.rect.y+self.height <map_y_dim:
                    self.rect.y +=self.speed
                else:
                    self.rect.y = map_y_dim - self.height
                self.lastmove='down'

            if key[pygame.K_LEFT]:
                if self.rect.x>0:
                    self.rect.x-=self.speed
                else:
                    self.rect.x = 0
                if self.orientation == 'right':
                    self.image = pygame.transform.flip(self.image,True,False)
                    self.orientation = 'left'
                self.lastmove = 'left'

            if key[pygame.K_RIGHT]:
                if self.rect.x +self.width<map_x_dim:
                    self.rect.x +=self.speed
                else:
                    self.rect.x = map_x_dim - self.width
                if self.orientation == 'left':
                    self.image = pygame.transform.flip(self.image,True,False)
                    self.orientation = 'right'
                self.lastmove = 'right'
        else:
            if self.lastmove == 'up':
                self.rect.y+=self.speed
            if self.lastmove == 'down':
                self.rect.y-=self.speed
            if self.lastmove == 'left':
                self.rect.x +=self.speed
            if self.lastmove == 'right':
                self.rect.x -=self.speed
        
    def collide(self,object):
        if pygame.sprite.spritecollide(self,object,False)!=[]:
            return True
        else:
            return False

    def update(self):
        if self.win == True:
            screen.blit(win_img,(0,0))
        elif self.gameover==True:
            screen.blit(game_over_img,(0,0))
        else:
            if self.collide(enemy)==True:
                self.gameover = True
            else:
                self.action()

directions = ['left','right','up','down']

class Enemy(pygame.sprite.Sprite):
    def __init__(self,width,height):
        super().__init__()
        self.x_pos = map_x_dim - width - 5
        self.y_pos = map_y_dim - height -5
        self.image = pygame.image.load("./images/cyborg.jpg").convert_alpha()
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(self.image,(self.width,self.height))
        self.rect = self.image.get_rect(topleft=(self.x_pos,self.y_pos))
        self.lastmoves = ['','']
        self.orientation = 'right'
        self.speed = 3
        self.direction = directions[randint(0,3)]
    
    def update_last_move(self,new_last_move):
        self.lastmoves[0]=self.lastmoves[1]
        self.lastmoves[1]=new_last_move

    def go_up(self):
        if self.rect.y >0:
            self.rect.y -= self.speed
        else:
            self.rect.y = 0
        self.update_last_move('up')

    def go_down(self):
        if self.rect.y + self.height<map_y_dim:
            self.rect.y +=self.speed
        else:
            self.rect.y = map_y_dim - self.height 
        self.update_last_move('down')

    def go_left(self):
        if self.rect.x>0:
            self.rect.x-=self.speed
        else:
            self.rect.x = 0
        if self.orientation == 'right':
            self.image = pygame.transform.flip(self.image,True,False)
            self.orientation = 'left'
        self.update_last_move('left')
    
    def go_right(self):
        if self.rect.x +self.height<map_x_dim:
            self.rect.x +=self.speed
        else:
            self.rect.x = map_x_dim - self.width
        if self.orientation == 'left':
            self.image = pygame.transform.flip(self.image,True,False)
            self.orientation = 'right'
        self.update_last_move('right')
    
    def check_hit_wall(self):
        if (self.rect.x<=0) or (self.rect.x >= map_x_dim-(self.width)) or (self.rect.y<=0) or (self.rect.y >= map_y_dim-(self.height )):
            return True
        else:
            return False

    def action(self):
        if self.collide(walls)==False and self.check_hit_wall()==False:
            if self.direction == 'up':
                self.go_up()
            if self.direction == 'down':
                self.go_down()
            if self.direction == 'left':
                self.go_left()
            if self.direction == 'right':
                self.go_right()
        else:
            self.direction = directions[randint(0,3)]
            '''while self.direction in self.lastmoves:
                self.direction = directions[randint(0,3)]'''
            if self.lastmoves[1] == 'up':
                self.rect.y+=self.speed
            if self.lastmoves[1] == 'down':
                self.rect.y-=self.speed
            if self.lastmoves[1] == 'left':
                self.rect.x +=self.speed
            if self.lastmoves[1] == 'right':
                self.rect.x -=self.speed


        
    def collide(self,object):
        if pygame.sprite.spritecollide(self,object,False)!=[]:
            return True
        else:
            return False

    def update(self):
        self.action()


class Bullet(pygame.sprite.Sprite):
    def __init__(self,x_pos,y_pos,direction):
        super().__init__()
        print('bullet created')
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = pygame.image.load("./images/bullet.jpg").convert_alpha()
        self.image = pygame.transform.scale(self.image,(20,10))
        self.rect = self.image.get_rect(topleft=(self.x_pos,self.y_pos))
        self.direction = direction
        self.win = False

    def action(self):
        if self.direction == "left":
            self.image= pygame.transform.rotate(self.image,180)
            self.rect.x -=4
        if self.direction == "right":
            self.image= pygame.transform.rotate(self.image,0)
            self.rect.x +=4
    
    def collide(self,object):
        if pygame.sprite.spritecollide(self,object,False)!=[]:
            return True
        else:
            return False
        
    def update(self):
        if self.collide(walls) or self.rect.x <0 or self.rect.x >map_x_dim or self.rect.y <0 or self.rect.y >map_y_dim:
            self.kill()
        if self.collide(enemy):
            cyborg.kill()
            hero.win = True
            self.kill()
        self.action()



walls = pygame.sprite.Group()

'''walls.add(Wall(400,200,100,40))
walls.add(Wall(90,300,170,60))
walls.add(Wall(300,0,50,200))'''

walls_list = maze_wall_generator(100, 100, map_x_dim, map_y_dim)
print(walls_list)
print(len(walls_list))
for type_of_wall in walls_list:
    for list in type_of_wall:
        for wall in list:
            if wall !=0:
                walls.add(wall)

player = pygame.sprite.Group()
hero = Player(80,80)
player.add(hero)

enemy = pygame.sprite.GroupSingle()
cyborg = Enemy(80,80)
enemy.add(cyborg)


while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                if len(player) == 1:
                    player.add(Bullet(hero.rect.x,hero.rect.y+50,hero.orientation))

    
    screen.fill('White')
    walls.draw(screen)
    enemy.update()
    enemy.draw(screen)

    player.draw(screen)
    player.update()
    
    pygame.display.update()
    clock.tick(60)
