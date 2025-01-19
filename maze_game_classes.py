import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self,x_pos,y_pos,width,height):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = pygame.Surface((width,height))
        self.rect = self.image.get_rect(topright=(self.x_pos,self.y_pos))
        self.image.fill('black')