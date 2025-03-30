import pygame
from script.setting import*

#make everything move to the opposite direction the player move
class Camera(pygame.sprite.Sprite):
    def __init__ (self, width, height):
        super().__init__()

        self.offset = pygame.Vector2(100, 80)

        self.width = width
        self.height = height


    def update(self, player):
        self.offset.x = player.rect.centerx - WIDTH//2
        self.offset.y = player.rect.centery - HEIGHT//2


    def apply(self, pos):
        return pos[0] - self.offset.x, pos[1] - self.offset.y
    
 
        

    
