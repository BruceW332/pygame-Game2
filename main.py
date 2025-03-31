import pygame
import sys
import random
import asyncio
from script.setting import*
from script.sprites import Player, CloseRangeEnemy, LongRangeEnemy, DashEnemy
from script.gridlines import draw_grid
from script.utils import load_image
from script.tilemap import Tilemap
from script.camera import Camera
from script.inventory1 import Inventory
from script.weapon import ShotGun


#UI

def draw_text(surf, text, font, colour, x, y):
    img = font.render(text, True, colour)
    text_rect = img.get_rect(center=(x, y))
    surf.blit(img, text_rect)



def draw_health(surf, x, y, percent):
    if percent < 0:
        percent = 0
    Length = 100
    Height = 20
    fill = percent * Length
    outline_rect = pygame.Rect(x, y, Length, Height)
    fill_rect = pygame.Rect(x, y, fill, Height)
    if percent > 0.3:
        colour = GREEN
    else:
        colour = RED
    pygame.draw.rect(surf, WHITE, outline_rect)
    pygame.draw.rect(surf, colour, fill_rect)
    

# load everything
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.pre_init(44100, -16, 1, 2048)
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        

        self.assets = {
            'player' : load_image('kunkun_player.png'),
            'enemy' : load_image('heizi_enemy5.png'),
            'block' : load_image('wall4.png'),
            'floor' : load_image('floor3.png'),
            'key' : load_image('key2.png'),
            'shotgun' : load_image('shotgun1.png'),
            'ammo' : load_image('kundan.png'),
            'open_door': load_image('open_door.png'),
            'close_door' : load_image('close_door.png'),
            'longrange_enemy' : load_image('bomb_thrower3.png'),
            'enemy_projectile' : load_image('enemy_projectile1.png'),
            'dash_enemy' : load_image('dash_enemy1.png'),
            'shotgun_ammo' : load_image('kundan2.png'),
            'health_book' : load_image('health_book.png'),
            'staff' : load_image('staff.png'),
            'fireball' : load_image('fireball.png'),
            'water' : load_image('water.png'),
            'sword' : load_image('sword.png'),
            'sword_ammo' : load_image('sword_projectile.png')
        }

        self.sfx = {
            'shoot' : pygame.mixer.Sound('data/sfx/shoot.wav'),
            'background' : pygame.mixer.Sound('data/sfx/background.wav'),
            'hit' : pygame.mixer.Sound('data/sfx/hit.wav'),
            'player_hit' : pygame.mixer.Sound('data/sfx/player_hit.wav'),
            'fire' : pygame.mixer.Sound('data/sfx/fire.wav'),
            'heal' : pygame.mixer.Sound('data/sfx/heal.wav'),
            'sword' : pygame.mixer.Sound('data/sfx/sword1.wav'),
            'win' : pygame.mixer.Sound('data/sfx/win.wav'),
            'die' : pygame.mixer.Sound('data/sfx/die.wav'),
            'equip' : pygame.mixer.Sound('data/sfx/equip.wav')         
        }

        self.sfx['hit'].set_volume(0.4)
        self.sfx['shoot'].set_volume(0.2)
        self.sfx['player_hit'].set_volume(0.2)
        self.sfx['fire'].set_volume(0.3)
        self.sfx['heal'].set_volume(0.2)
        self.sfx['background'].set_volume(0.3)
        self.sfx['win'].set_volume(0.6)
        self.sfx['die'].set_volume(0.6)
        self.sfx['sword'].set_volume(0.2)
      
         
        self.door = None
        self.all_sprites = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.enemy_projectile_group = pygame.sprite.Group()
        self.tilemap = Tilemap(self, 'data/map/map2.txt')
        self.spawn_point = self.tilemap.enemy_spawn_point 
        print(self.door) 
        self.blocks = pygame.sprite.Group()
        self.inventory = Inventory(self)    
        self.camera = Camera(self.tilemap.width * TILESIZE, self.tilemap.height * TILESIZE)
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.movement = [False, False, False, False]
        self.shotgun = ShotGun(self, self.player)
        self.playing = True
        self.text_font = pygame.font.SysFont(None, 120, bold=True )
        self.text_font2 = pygame.font.SysFont(None, 35, bold=True )
   
   


        

        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 10)

        self.enemy_spawn_limit = 10
        
    def spawn_enemy_at(self, pos):
        enemytype = random.choice(['close', 'long', 'dash'])
        if enemytype == 'close':
            enemy = CloseRangeEnemy(self, pos)
        elif enemytype == 'long':
            enemy = LongRangeEnemy(self, pos)
        elif enemytype == 'dash':
            enemy = DashEnemy(self, pos)
        self.enemy_group.add(enemy)

    
    def lose_screen(self):
        self.screen.fill(BLACK)
    
        


        

    def run(self):

        
        

        self.sfx['background'].play(-1)
        
        self.playing = True
        while self.playing:

            

            
            self.event()
            self.update()
            self.render()
            self.clock.tick(FPS)
            


    def update(self):

        self.player.update(self.movement)
        self.camera.update(self.player)
        self.projectiles.update()
        self.enemy_group.update()
        self.enemy_projectile_group.update()
        

    
        
        
        
        pygame.display.update()

#render everything base on camera
    def render(self):

        self.screen.fill(BLACK)

        



        for tile in self.tilemap.tiles:
            tile_pos = self.camera.apply(tile.rect.topleft)
            self.screen.blit(tile.image, tile_pos)

        #draw_grid(self.screen)

        

        for entity in self.all_sprites:
            entity_pos = self.camera.apply(entity.rect.topleft)
            self.screen.blit(entity.image, entity_pos)

        for item in self.items:

            item_pos = self.camera.apply(item.rect.topleft)
            self.screen.blit(item.image, item_pos)


        for enemy in self.enemy_group:
            self.screen.blit(enemy.image, self.camera.apply(enemy.rect.topleft))
            

            
        
        



        
        

        self.player.render(self.screen)
        
        draw_health(self.screen, WIDTH - 400, 20, self.player.health / 100)

        for bullet in self.projectiles:
            bullet_pos = self.camera.apply(bullet.rect.topleft)  # Apply camera transformation
            self.screen.blit(bullet.image, bullet_pos)

        for bullet in self.enemy_projectile_group:
            bullet_pos = self.camera.apply(bullet.rect.topleft)  # Apply camera transformation
            self.screen.blit(bullet.image, bullet_pos)
        

        self.player.inventory.render(self.screen)

        draw_text(self.screen, "press e to pick up items", self.text_font2, WHITE, 160, HEIGHT - 40)
        draw_text(self.screen, "press space to attack,shoot", self.text_font2, WHITE, 160, HEIGHT - 20)

        
        
      
        
        pygame.display.flip()





 #handle input   
    def event(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    


                if event.type == self.enemy_event:
                    if len(self.enemy_group) < self.enemy_spawn_limit:
                        player_center = pygame.Vector2(self.player.rect.center)
                        for pos in self.spawn_point:
                            spawn_pos = pygame.Vector2(pos)
                            distance = player_center.distance_to(spawn_pos)

                            if distance > MIN_SPAWNING_DISTANCE:
                                self.spawn_enemy_at(pos)


                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame. K_w:
                        print("up work")
                      
                        self.movement[2] = True
                        
                    if event.key == pygame.K_DOWN or event.key == pygame. K_s:
                        
                        self.movement[3] = True
                        
                    if event.key == pygame.K_RIGHT or event.key == pygame. K_d:
                     
                        self.movement[1] = True
                    if event.key == pygame.K_LEFT or event.key == pygame. K_a:
                    
                        self.movement[0] = True
                    # the event key on keyboard only work when a space is add after .
                    if event.key == pygame. K_e:
                        self.player.pick_up_items()
                  
                    
                    #python start count from 0 than 1 

                    if event.key == pygame. K_1:
                        self.player.inventory.update(0)
                        self.inventory.equip_weapon()

                    if event.key == pygame. K_2:
                        self.player.inventory.update(1)
                        self.inventory.equip_weapon()

                    if event.key == pygame. K_3:
                        self.player.inventory.update(2)
                        self.inventory.equip_weapon()

                    if event.key == pygame. K_4:
                        self.player.inventory.update(3)
                        self.inventory.equip_weapon()

                    if event.key == pygame. K_5:
                        self.player.inventory.update(4)
                        self.inventory.equip_weapon()

                    if event.key == pygame. K_6:
                        self.player.inventory.update(5)
                        self.inventory.equip_weapon()

                    if event.key == pygame. K_7:
                        self.player.inventory.update(6)
                        self.inventory.equip_weapon()

                    if event.key == pygame. K_8:
                        self.player.inventory.update(7)
                        self.inventory.equip_weapon()

                    if event.key == pygame. K_9:
                        self.player.inventory.update(8)
                        self.inventory.equip_weapon()


                    #somehow space keys , esc, enter and arrows keys don't need to add a space
                    if event.key == pygame.K_SPACE:
                        self.player.use_item()
                        if self.player.equipped_weapon is not None:
                          
                            self.player.equipped_weapon.attack()
                        else:
                            print("player didn;t equip weapon")
                    
                    
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        

                        
                        
                        
                if event.type == pygame.KEYUP:
                    
                    if event.key == pygame.K_UP or event.key == pygame. K_w:
                     
                        self.movement[2] = False
                        
                    if event.key == pygame.K_DOWN or event.key == pygame. K_s:
                  
                        self.movement[3] = False
                        
                    if event.key == pygame.K_RIGHT or event.key == pygame. K_d:
                    
                        self.movement[1] = False
                    if event.key == pygame.K_LEFT or event.key == pygame. K_a:
                   
                        self.movement[0] = False


    def win(self):

        self.sfx['background'].stop()

        
        self.sfx['win'].play()
        self.playing = False


        self.screen.fill(BLACK)
        draw_text(self.screen, "You Win", self.text_font, YELLOW, WIDTH / 2, HEIGHT / 2 )

        draw_text(self.screen, "Press any_key to restart", self.text_font, WHITE, WIDTH / 2, HEIGHT / 2 + 100)


        pygame.display.flip()

        self.wait()

     

    



    def loss(self):
        self.sfx['background'].stop()
        self.sfx['die'].play()
        self.playing = False


        self.screen.fill(BLACK)
        draw_text(self.screen, "You Loss", self.text_font, RED, WIDTH / 2, HEIGHT / 2 )

        draw_text(self.screen, "Press any_key to restart", self.text_font, WHITE, WIDTH / 2, HEIGHT / 2 + 100)


        pygame.display.flip()

        self.wait()
    
    def wait(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    pygame.quit()
                    
                
                if event.type == pygame.KEYDOWN:
                    waiting = False


       
   
      

     

       
                    
                
               

async def main():
        while True:
            Game().run()
            Game().lose_screen()
            await asyncio.sleep(0)  
asyncio.run(main())

