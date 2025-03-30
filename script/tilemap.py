import pygame
from script.setting import*
from script.block import Wall, Decoration, Item, Door
from script.utils import load_map






class Tilemap:
    def __init__(self, game, mapfile):
        self.game = game
        self.tiles = pygame.sprite.Group()
        self.tile_dict = {}
        self.load_tiles(mapfile)

        self.widths = 0
        self.height = 0
        
        
# using the funtion in utils to read the data in mapfile but somehow it need to type the filename in here than in game.py
    def load_tiles(self, mapfile):
        self.enemy_spawn_point = []
        self.elites_enemy = []
        map_data, map_width, map_height = load_map('data/map/map2.txt')  

        self.width = map_width
        self.height = map_height
        

        for row_index, row in enumerate(map_data):
            for col_index, char in enumerate(row):

                tile_pos = (col_index, row_index)

                if tile_pos not in self.tile_dict:
                    self.tile_dict[tile_pos] = []

                tile_sprite_object = None
                

                
#place the sprite on its position base on the character it has , The value is the row index and col index (x, y ) 
                if char == '1':
                    tile_sprite_object = Wall(self.game, col_index, row_index, self.game.assets['block'])
                elif char == '.':
                    tile_sprite_object = Decoration(self.game, col_index, row_index, self.game.assets['floor'])
                elif char == 'P':
                    
                    self.player_start_pos = (col_index, row_index)
                    tile_sprite_object = Decoration(self.game, col_index, row_index, self.game.assets['floor'])
                elif char == 'K':
                    
                    Item(self.game, col_index, row_index, 'key', self.game.assets['key'])
                    tile_sprite_object = Decoration(self.game, col_index, row_index, self.game.assets['floor'])
                
                elif char == 'S':
                    Item(self.game, col_index, row_index, 'shotgun', self.game.assets['shotgun'])
                    tile_sprite_object = Decoration(self.game, col_index, row_index, self.game.assets['floor'])

                elif char == 'H':
                    Item(self.game, col_index, row_index, 'health_book', self.game.assets['health_book'])
                
                elif char == 'E':
                    pixel_pos = col_index * TILESIZE, row_index * TILESIZE
                    self.enemy_spawn_point.append(pixel_pos)
                    tile_sprite_object = Decoration(self.game, col_index, row_index, self.game.assets['water'])

                elif char == 'B':
                    pixel_pos = col_index * TILESIZE, row_index * TILESIZE
                    self.elites_enemy.append(pixel_pos)
                    tile_sprite_object = Decoration(self.game, col_index, row_index, self.game.assets['water'])
                
                elif char == 'D':
                    door = Door(self.game, col_index, row_index, self.game.assets['open_door'], self.game.assets['close_door'])
                    self.tiles.add(door)
                    self.tile_dict[tile_pos].append(door)
                    self.game.door = door

                elif char == 'T':
                    Item(self.game, col_index, row_index, 'staff', self.game.assets['staff'])
                    tile_sprite_object = Decoration(self.game, col_index, row_index, self.game.assets['floor'])
                
                elif char == 'O':
                    Item(self.game, col_index, row_index, 'sword', self.game.assets['sword'])
                    tile_sprite_object = Decoration(self.game, col_index, row_index, self.game.assets['floor'])
                
                    


                    
                    
                


                if tile_sprite_object is not None:
                    self.tiles.add(tile_sprite_object)

                #safe the placement of all the tile sprite into a dictionary
                if tile_sprite_object is not None:
                    self.tile_dict[tile_pos].append(tile_sprite_object) 

        

# for optimization , save the data of the tiles areound player 3*3 
    def tiles_around(self, rect):
        tiles_around_player = []
        

        #int and // both together, prevent game crash
        center_tile = (int(rect.centerx//TILESIZE),int(rect.centery//TILESIZE))
        for row in range(center_tile[1] -1, center_tile[1] + 2):
            for col in range(center_tile[0] -1, center_tile[0] + 2):
                tile_list = self.tile_dict.get((col, row), [])
                
                for tile in tile_list:         
                    tiles_around_player.append(tile)
       
       #safe the data in a list         
        return tiles_around_player


# not using now
    def draw(self, surface):
        self.tiles.draw(surface)

    
    