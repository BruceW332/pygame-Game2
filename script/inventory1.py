import pygame
from script.setting import*
from script.weapon import ShotGun, Staff, Sword


class ItemSlot:
    def __init__(self, item_type = None, amount = 0):

      

        self.item_type = item_type
        self.amount = amount
        

        


class Inventory:
    def __init__(self, game):
        self.game = game
        self.slots = [ItemSlot() for i in range(9)]
        self.selected_slot, self.equipped_weapon = 0, None
        self.slot_size, self.slot_gap = 40, 20
        self.x, self.y = 15, 15 
        self.font = pygame.font.SysFont(None, 20, bold=True)


    def add(self, item_type, amount):
        for slots in self.slots:
            if slots.item_type == item_type:
                slots.amount += amount

                return True
        for slots in self.slots:
            if slots.item_type is None:
                slots.item_type = item_type
                slots.amount = amount
                return True
            
    
    
    def equip_weapon(self):

        selected_item = self.slots[self.selected_slot]
        if selected_item.item_type is not None:
            
            
            if selected_item.item_type in WEAPON:
                
                print("shotgun is select")
                if selected_item.item_type == 'shotgun':
                    self.weapon = ShotGun(self.game, self.game.player)
                    self.game.enemy_spawn_limit = 30
                    print(self.game.enemy_spawn_limit)
                    print("shotgun equip")

                    self.game.player.equipped_weapon = self.weapon

                elif selected_item.item_type == 'staff':
                    self.weapon = Staff(self.game, self.game.player)
                    print("staff equip")

                    self.game.player.equipped_weapon = self.weapon
                
                elif selected_item.item_type == 'sword':
                    self.weapon = Sword(self.game, self.game.player)
                    print("sword equip")

                    self.game.player.equipped_weapon = self.weapon
            else:
                print("unequip")
                
                self.game.player.equipped_weapon = None

    def update(self, index):
        self.selected_slot = index

        self.equip_weapon()
    
    def draw_item_name_number(self, surface, slot, slot_position):
        text_surface = self.font.render(str(slot.amount), True, WHITE)
        shadow_surface = self.font.render(str(slot.amount), True, BLACK)
        surface.blit(shadow_surface, (slot_position.x + 28, slot_position.y +28))
        surface.blit(text_surface, (slot_position.x + 25, slot_position.y +25))

        
        
      
        name_surface = self.font.render(slot.item_type, True, WHITE)
        name_shadow_surface = self.font.render(slot.item_type, True, BLACK)

        name_rect = name_surface.get_rect(midtop= (slot_position.centerx, slot_position.y - 15))
        name_shadow_rect = name_shadow_surface.get_rect(midtop=(slot_position.centerx + 3, slot_position.y - 12))
        surface.blit(name_shadow_surface, name_shadow_rect)
        surface.blit(name_surface, name_rect)

    
    def render(self, surface):
        for index, slot in enumerate(self.slots):
            slot_pos = pygame.Rect(self.x + index * (self.slot_size + self.slot_gap), self.y , self.slot_size, self.slot_size)
            pygame.draw.rect(surface, DARKGREY, slot_pos)
            pygame.draw.rect(surface, WHITE, slot_pos, 2)


            if index == self.selected_slot:
                pygame.draw.rect(surface, YELLOW, slot_pos, 2)
            
            if slot.item_type is not None:
                item_image = self.game.assets.get(slot.item_type)
                image = pygame.transform.scale(item_image, (self.slot_size, self.slot_size))
                surface.blit(image, slot_pos.topleft)
                self.draw_item_name_number(surface, slot, slot_pos)





