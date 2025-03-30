import pygame
import random

from script.setting import*
from script.tilemap import*
from script.inventory1 import*
from script.projectile import EnemyProjectile

# class the universal thing for a entity
class PhysicsEntity(pygame.sprite.Sprite):
    def __init__(self, game, e_type, pos, size):
        super().__init__()
        self.game = game
        self.type = e_type

        self.x, self.y = list(pos)

        
        self.image = pygame.Surface(size)
        self.image.fill((255, 0, 0))  



    
        self.rect = self.image.get_rect(center=pos)

        self.movement = [0, 0, 0, 0]

        
        self.velocity_x , self.velocity_y = 0, 0
        
 # check the collision of 3*3 area for the entities, maybe add on projectile
    def collide_with_physical_block(self, direction):
        
        nearby_tiles = pygame.sprite.Group(self.game.tilemap.tiles_around(self.rect))
        colliding_tiles = pygame.sprite.spritecollide(self, nearby_tiles, False)

        for tile in colliding_tiles:
            if tile.physics_enabled:  
                if direction == 'x':
                    if self.velocity_x > 0:
                        self.rect.right = tile.rect.left
                    elif self.velocity_x < 0:
                        self.rect.left = tile.rect.right

                    self.velocity_x = 0
                    self.x = self.rect.x

                if direction == 'y':
                    if self.velocity_y > 0:
                        self.rect.bottom = tile.rect.top
                    elif self.velocity_y < 0:
                        self.rect.top = tile.rect.bottom

                    self.velocity_y = 0
                    self.y = self.rect.y
    
    def apply_movement(self, speed):
        self.x += self.velocity_x * speed
        self.y += self.velocity_y * speed

        self.rect.x = self.x
        self.collide_with_physical_block('x')

        

        self.rect.y = self.y
        self.collide_with_physical_block('y')

    
    

    



class Player(PhysicsEntity):
    def __init__(self, game):
        start_col, start_row = game.tilemap.player_start_pos

        self.x = start_col * TILESIZE
        self.y = start_row * TILESIZE
        
        super().__init__(game, "player", (self.x, self.y), (32, 32))

        self.inventory = Inventory(game)
        

       


        self.image = self.game.assets['player']
        self.rect = pygame.Rect(self.x,self.y, 32, 48)

        self.equipped_weapon = None

        self.speed = PLAYER_SPEED
        self.knockback = pygame.Vector2(0, 0)
        self.knockback_frame = 0

        self.health = 100
        self.last_direction = pygame.Vector2(1, 0)
# I try to add this to inventory.py but somehow it is not rendering
    


    def pick_up_items(self):
        

        pick_up_area = pygame.sprite.spritecollide(self, self.game.items, False)
        
        for item in pick_up_area:
            if self.inventory.add(item.item_type, 1):
                item.kill()
             
        

     
        self.inventory.equip_weapon()
        
#call the funtion in inventory
    def use_item(self):

        selected_item = self.inventory.slots[self.inventory.selected_slot]
        
        if selected_item.item_type in ITEM:
            if selected_item.item_type == 'key':
                door = self.game.door

                collide_with_door = self.rect.colliderect(door.rect.inflate(32, 32))

                if collide_with_door == True:
                    door.update()
                    self.game.win()
                    
                    selected_item.amount -= 1
                    if selected_item.amount <= 0:
                        selected_item.item_type = None
                    

            elif selected_item.item_type == 'health_book':
                self.game.sfx['heal'].play()
                self.game.player.health += 50

                
                selected_item.amount -= 1
                if selected_item.amount <= 0:
                    selected_item.item_type = None

    
    def player_knock_back(self, enemy_pos):
        direction = pygame.Vector2(self.rect.center) - pygame.Vector2(enemy_pos)
        angle = direction.angle_to(pygame.Vector2(1, 0))

        knockback = pygame.Vector2(20, 0).rotate(-angle)
        


        self.knockback = knockback

        self.knockback_frame = 5

        

    

    def update(self, movement):
        self.pick_up_items()

     

        if self.knockback_frame > 0:
            self.velocity_x += self.knockback.x
            self.velocity_y += self.knockback.y


            self.apply_movement(1)
            self.knockback_frame -=1

#call the update funtion of shotgun that is inheriate from Weapon class
        if self.equipped_weapon is not None:
            self.equipped_weapon.update()
        
               
     # turn the bool value to the direction (1, 0)   1 - 0 = 1 , 0 - 1 = -1 to caculate the velocity to update physics
        self.velocity_x = (movement[1] - movement[0])
        self.velocity_y = (movement[3] - movement[2])

        #make the speed of verticle speed same as straight speed through time the square root of 1/2, complicated 
        if self.velocity_x != 0 and self.velocity_y != 0:
                self.velocity_x *= 0.7071
                self.velocity_y *= 0.7071
        
        movement_vector = pygame.Vector2(self.velocity_x, self.velocity_y)

        if movement_vector.length_squared() > 0:
            self.last_direction = movement_vector.normalize()




        self.apply_movement(self.speed)

        

      
    
    def render(self, surface):

       
        player_pos = self.game.camera.apply(self.rect.topleft)
        surface.blit(self.game.assets['player'], player_pos)

        #render weapon
        if self.equipped_weapon:
            weapon_pos = self.game.camera.apply(self.equipped_weapon.rect.topleft)
            surface.blit(self.equipped_weapon.image, weapon_pos)

        #add the item image and render it 
        selected_item = self.inventory.slots[self.inventory.selected_slot]
        if selected_item.item_type is not None:

            if selected_item.item_type in ITEM:
                if selected_item.item_type == 'key':
                    self.game.enemy_spawn_limit = 80
                    print("very difficult")
                item_image = self.game.assets.get(selected_item.item_type)
                item_image2 = pygame.transform.scale(item_image, (24, 24))

                if self.equipped_weapon is not None:            
                    item_rect = self.equipped_weapon.rect
                else:
                    offset = pygame.Vector2(15, 0)
                    adjust_center = self.rect.center + offset
                    item_rect = item_image2.get_rect(center=adjust_center)
                    item_pos = self.game.camera.apply(item_rect.topleft)
                    surface.blit(item_image2, item_pos)



class Enemy(PhysicsEntity):
    def __init__(self, game, pos):
            super().__init__(game, 'enemy', pos, (32, 32))
            
            
            self.speed = ENEMY_SPEED
            self.avoid_radius = AVOID_RADIUSS
            self.separation = pygame.Vector2(0, 0)
            self.chase = False
            self.dash_speed = 3


    def collide_with_player(self, damage):
        if pygame.sprite.collide_rect(self, self.game.player):
            self.game.sfx['player_hit'].play()
            self.game.player.health -= damage
            self.game.player.player_knock_back(self.rect.center)

            if self.game.player.health <= 0:
                self.game.loss()
        


    def avoid_other_enemies(self):
        self.separation = pygame.Vector2(0, 0)
            
        for enemy in self.game.enemy_group:
            if enemy != self:
                distance = pygame.Vector2(self.rect.center) - pygame.Vector2(enemy.rect.center)
                if 0 < distance.length() < self.avoid_radius:
                    self.separation += distance.normalize()


        return self.separation
        
    def move(self):

        player_center = pygame.Vector2(self.game.player.rect.center)
        enemy_center = pygame.Vector2(self.rect.center)

        direction = player_center - enemy_center

        if direction.length() != 0:
            direction = direction.normalize()
                
        else:
            direction = pygame.Vector2(0, 0)

            
        separation = self.avoid_other_enemies()


       

        total_direction = direction + separation * 1.5
        if total_direction.length() > 0:
            total_direction = total_direction.normalize()

        self.velocity_x = total_direction.x
        self.velocity_y = total_direction.y

        self.apply_movement(self.speed)


    def dash(self):

        player_center = pygame.Vector2(self.game.player.rect.center)
        enemy_center = pygame.Vector2(self.rect.center)

        direction = player_center - enemy_center

        if direction.length() != 0:
            direction = direction.normalize()
                
        else:
            direction = pygame.Vector2(0, 0)

            
        separation = self.avoid_other_enemies()


       

        total_direction = direction + separation * 1.5
        if total_direction.length() > 0:
            total_direction = total_direction.normalize()

        self.velocity_x = total_direction.x
        self.velocity_y = total_direction.y

        self.apply_movement(self.dash_speed)


    def allign_player(self, tolerance = 32):
        player_x, player_y = self.game.player.rect.center
        enemy_x, enemy_y = self.rect.center

        x_allign_with_player = abs(player_x - enemy_x) < tolerance
        y_allign_with_player = abs(player_y - enemy_y) < tolerance

        return x_allign_with_player or y_allign_with_player
    


    
    
    def move_toward_to_allign(self):
        player_x, player_y = self.game.player.rect.center
        enemy_x, enemy_y = self.rect.center

        difference_in_x = player_x - enemy_x
        difference_in_y = player_y - enemy_y

        tolerance = 16

        if self.allign_player(tolerance):
            self.velocity_x= 0
            self.velocity_y = 0
            



        if abs(difference_in_x) > 1:
            
            if difference_in_x > 0:
                self.velocity_x = 1
                self.velocity_y = 0
            else:
                self.velocity_x = -1
                self.velocity_y = 0
            
            move_direction = pygame.Vector2(self.velocity_x, self.velocity_y)
        
        elif abs(difference_in_y) > 1:
            if difference_in_y > 0:
                self.velocity_y = 1
                self.velocity_x = 0
            else:
                self.velocity_y = -1
                self.velocity_x = 0

            move_direction = pygame.Vector2(self.velocity_x, self.velocity_y)
        
        separation = self.avoid_other_enemies()
        

        finial_direction = move_direction + separation * 8
        if finial_direction.length() > 0:
            direction = finial_direction.normalize()
            self.velocity_x = direction.x
            self.velocity_y = direction.y
            
        

        self.apply_movement(self.speed)



           
        

        
    def update(self):
            
        player_center = pygame.Vector2(self.game.player.rect.center)
        enemy_center = pygame.Vector2(self.rect.center)
        distance = player_center.distance_to(enemy_center)

        if distance > REMOVING_DISTANCE:
            self.kill()
        if distance < CHASE_DISTANCE:
            self.chase = True
        else:
            self.velocity_x = random.randint(-5, 5)
            self.velocity_y = 0
            self.apply_movement(self.speed)
            

        
class CloseRangeEnemy(Enemy):
    def __init__(self, game, pos):
        super().__init__(game, pos)

        self.image = self.game.assets['enemy']


        self.health = 75
        self.damage = CLOSE_DAMAGE

    def update(self):
        super().update()

        self.collide_with_player(self.damage)
       

        if self.chase == True:
            self.move()
    
        if self.health < 0:
            self.kill()


class LongRangeEnemy(Enemy):
    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.health = 50

        self.image = self.game.assets['longrange_enemy']
        self.last_shot = 0


    


    def shoot(self):
        player_x, player_y = self.game.player.rect.center
        enemy_x, enemy_y = self.rect.center

        difference_in_x = player_x - enemy_x
        difference_in_y = player_y - enemy_y

        if abs(difference_in_x) > abs(difference_in_y):

            if difference_in_x > 0:

                shoot_direction = pygame.Vector2(1, 0)

            else:
                shoot_direction = pygame.Vector2(-1, 0)
        else:
            if difference_in_y > 0:

                shoot_direction = pygame.Vector2(0, 1)
            else:
                shoot_direction = pygame.Vector2(0, -1)

      
        bullet = EnemyProjectile(self.game, self.rect.center, shoot_direction)
        self.game.enemy_projectile_group.add(bullet)




    
    def update(self):  
        super().update()

        if self.chase == True:
            if self.allign_player() == True:
                self.velocity_x = 0
                self.velocity_y = 0

                now = pygame.time.get_ticks()
                if now - self.last_shot > 3000:
                    self.last_shot = now
                    self.shoot()
               
                
            else:
                self.move_toward_to_allign()


class DashEnemy(Enemy):
    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.health = 50
      
        self.image = self.game.assets['dash_enemy']
        self.damage = DASH_DAMAGE


    def update(self):  
        super().update()

        self.collide_with_player(self.damage)
        if self.chase == True:
            if self.allign_player() == True:
                self.dash()
                        
            else:
                self.velocity_x = 0
                self.velocity_y = 0
                self.move_toward_to_allign()


        
        

    
    


            
            
            

            






