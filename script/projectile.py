import pygame
import random
from script.setting import*

class Projectile(pygame.sprite.Sprite):
    def __init__(self, game, weapon, pos, direction):
        super().__init__(game.projectiles) 
        self.game = game
        self.weapon = weapon
        
        self.speed = weapon.bullet_speed
        self.lifetime = weapon.bullet_lifetime
        self.damage = weapon.damage
        self.size = weapon.bullet_size
        self.spawn_time = pygame.time.get_ticks()
        
        self.image = self.game.assets['shotgun_ammo']
        self.rect = self.image.get_rect(center=pos)
        self.velocity = pygame.Vector2(direction) * self.speed
        
    def collision(self):
        nearby_tiles = pygame.sprite.Group(self.game.tilemap.tiles_around(self.rect))
        colliding_tiles = pygame.sprite.spritecollide(self, nearby_tiles, False)
        for tile in colliding_tiles:
            if tile.physics_enabled:
                self.kill()
        enemy_hit = pygame.sprite.spritecollide(self, self.game.enemy_group, False)
        for enemy in enemy_hit:
            self.game.sfx['hit'].play()
            enemy.health -= self.damage
            if enemy.health <= 0:
                enemy.kill()
            self.kill()
            
    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()  
        self.collision()




        

        
    



class ShotgunAmmo(Projectile):
    def __init__(self, game, weapon, pos, direction):
       
        spread_angle = random.uniform(-weapon.spread, weapon.spread)
        spread_direction = direction.rotate(spread_angle)

        super().__init__(game, weapon, pos, spread_direction) 

     
        self.image = self.game.assets['shotgun_ammo']

class StaffAmmo(Projectile):
    def __init__(self, game, weapon, pos, direction):
        spread_angle = random.uniform(-weapon.spread, weapon.spread)
        spread_direction = direction.rotate(spread_angle)

        super().__init__(game, weapon, pos, spread_direction) 
       
        self.image = self.game.assets['fireball']
class SwordAmmo(Projectile):
    def __init__(self, game, weapon, pos, direction):
        spread_angle = random.uniform(-weapon.spread, weapon.spread)
        spread_direction = direction.rotate(spread_angle)

        super().__init__(game, weapon, pos, spread_direction) 
       
        self.image = self.game.assets['sword_ammo']
       






class EnemyProjectile(pygame.sprite.Sprite):
    def __init__(self, game, pos, direction, speed=4):
        super().__init__(game.enemy_projectile_group)

        self.game = game
        self.image = self.game.assets['enemy_projectile']
        self.rect = self.image.get_rect(topleft=pos)

        self.velocity = pygame.Vector2(direction).normalize() * speed
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = random.randint(1500, 4000)
        self.damage = 10
    
    def collision(self):
        nearby_tiles = pygame.sprite.Group(self.game.tilemap.tiles_around(self.rect))
        colliding_tiles = pygame.sprite.spritecollide(self, nearby_tiles, False)

        for tile in colliding_tiles:
            if tile.physics_enabled:
                
                self.kill()  

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y


        self.collision()


        now = pygame.time.get_ticks()

        if now - self.spawn_time > self.lifetime:
            self.kill() 

        hit_player = self.rect.colliderect(self.game.player.rect)
        if hit_player:
            self.game.sfx['player_hit'].play()
            self.game.player.health -= self.damage
            self.game.player.player_knock_back(self.rect.center)

            if self.game.player.health <= 0:
                self.game.loss()

            
            
        
        
            
            

            self.kill()
