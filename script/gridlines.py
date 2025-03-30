import pygame
from script.setting import*


#just to make sure the image is same as the tilesize
def draw_grid(screen):
        
                
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y))