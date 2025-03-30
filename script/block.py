import pygame
from script.setting import*


class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image, physics_enabled=True):
        
        
     #not adding it to anygroups because it will be safe into tilemap.tiles group 
        super().__init__()

        self.game = game

        self.physics_enabled = physics_enabled 

        # Grid position (tile coordinate)
        self.x = x
        self.y = y

        # Set the image for the block
       
        self.image = image
       

        # Pixel position (where to render)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILESIZE, y * TILESIZE)

#copy and paste
class Decoration(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image, physics_enabled=False):
        
        
        super().__init__()

        self.game = game

        self.physics_enabled = physics_enabled 

        
        self.x = x
        self.y = y

        # Set the image for the block
       
        self.image = image
       

        # Pixel position (where to render)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILESIZE, y * TILESIZE)


#COPY and paste
class Item(pygame.sprite.Sprite):
    def __init__(self, game, x, y, item_type, image, physics_enabled=False):
        
       
        super().__init__(game.items)

        self.game = game

        self.item_type = item_type

        self.physics_enabled = physics_enabled 

       

        # Grid position (tile coordinate)
        self.x = x
        self.y = y

        # Set the image for the block
       
        self.image = image
        

        # Pixel position (where to render)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILESIZE, y * TILESIZE)

class Door(pygame.sprite.Sprite):
    def __init__(self, game, x, y, open_image, close_image, physics_enabled=True):
        
        
     #not adding it to anygroups because it will be safe into tilemap.tiles group 
        super().__init__()

        self.game = game

        self.physics_enabled = physics_enabled 
       

        # Grid position (tile coordinate)
        self.x = x
        self.y = y

        # Set the image for the block
       
        
        self.open_image = open_image

        self.close_image = close_image


        self.open_door = False

        self.image = self.open_image

        
       
       

        # Pixel position (where to render)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILESIZE, y * TILESIZE)


    def open(self):

        self.open_door = True

        self.physics_enabled = False

    

    
    def update(self):
         self.open()
         if self.open_door == True:
            self.image = self.close_image
            print("switch to open image")
         else:
            self.image = self.open_image
            print("didn't switch")




