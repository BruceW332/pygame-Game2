import pygame
from script.setting import WEAPONS
from script.projectile import ShotgunAmmo, StaffAmmo, SwordAmmo



#get the universal thing for weapon
class Weapon(pygame.sprite.Sprite):
    def __init__(self, game, weapon_type, player, image):
        super().__init__()
        
        

        self.game = game
        self.weapon_type = weapon_type
        self.player = player

        #load the WEAPONS dictionary from setting
        self.propertie = WEAPONS.get(weapon_type, {})

        #get all the values

        self.bullet_speed = self.propertie.get('bullet_speed', 0)
        self.bullet_lifetime = self.propertie.get('bullet_lifetime', 0)
       
        self.spread = self.propertie.get('spread', 0)
        self.damage = self.propertie.get('damage', 0)
        self.bullet_size = self.propertie.get('bullet_size', 0)
        self.bullet_count = self.propertie.get('bullet_count', 0)


        
        
        self.original_image = image

        self.flipped_image = pygame.transform.flip(self.original_image, False, True)  

        
        self.rect = self.original_image.get_rect()
        self.rot = 0 

        
        self.offset = pygame.Vector2(20, 10)

        
    
    def update(self):
        #get the movement of player and rotate the shotgun image base on it , maybe make the shotgun rotate base on the closest enemy position
        

       
        self.rot = self.player.last_direction.angle_to((1, 0))

        adjust_offset = self.offset + pygame.Vector2(0, -10)

        base_image = self.original_image


        if self.player.last_direction.x < 0:
            base_image = self.flipped_image

       
        

        self.image = pygame.transform.rotate(base_image, self.rot)

 

        #add flip funtion , complicated

        



        self.rect = self.image.get_rect(center=self.player.rect.center + adjust_offset.rotate(-self.rot))

    
class ShotGun(Weapon):
    def __init__(self, game, player):
        super().__init__(game=game, weapon_type='shotgun', player=player, image=game.assets['shotgun'])

       
# not finish yet because this need to call the projectile sprite
    def attack(self):

        self.game.sfx['shoot'].play()
       

        base_direction = self.player.last_direction

        spawn_pos = self.player.rect.center + pygame.Vector2(56, 0).rotate(-self.rot) 

      
        for i in range(self.bullet_count):        
            ShotgunAmmo(self.game, self, spawn_pos, base_direction)
          

       
class Staff(Weapon):
    def __init__(self, game, player):
        super().__init__(game=game, weapon_type='staff',player=player,image=game.assets['staff'])

    def attack(self):

        self.game.sfx['fire'].play()

        base_direction = self.player.last_direction

        spawn_pos = self.player.rect.center + pygame.Vector2(30, 0).rotate(-self.rot) 

        for i in range(self.bullet_count):
            StaffAmmo(self.game, self, spawn_pos, base_direction)
            
class Sword(Weapon):
    def __init__(self, game, player):
        super().__init__(game=game, weapon_type='sword',player=player,image=game.assets['sword'])

    def attack(self):

        self.game.sfx['sword'].play()

        base_direction = self.player.last_direction

        spawn_pos = self.player.rect.center + pygame.Vector2(30, 0).rotate(-self.rot) 

        for i in range(self.bullet_count):
            SwordAmmo(self.game, self, spawn_pos, base_direction)
            















