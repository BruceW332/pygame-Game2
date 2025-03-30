#colour
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "KUNKUN"
BGCOLOR = DARKGREY

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

#player propeties
PLAYER_SPEED = 5


#enemy propeties
ENEMY_SPEED = 2


AVOID_RADIUSS = 50

MIN_SPAWNING_DISTANCE = 500

REMOVING_DISTANCE = 600

CHASE_DISTANCE = 400

PROJECTILE_DAMAGE = 10

DASH_DAMAGE = 10

CLOSE_DAMAGE = 20




#Inventory system
WEAPON = ['shotgun', 'staff', 'sword']


ITEM = ['key', 'health_book']

# Weapon system, more convince
WEAPONS = {
    'staff': {
        'bullet_speed': 20,
        'bullet_lifetime': 500,
        'spread': 9,
        'damage': 25,
        'bullet_size': 10,
        'bullet_count': 3
    },
    'shotgun': {
        'bullet_speed': 20,
        'bullet_lifetime': 360,
        'spread': 21,
        'damage': 25,
        'bullet_size': 15,
        'bullet_count': 12
    },
    'sword':{
        'bullet_speed': 20,
        'bullet_lifetime': 1000,
        'spread': 15,
        'damage': 25,
        'bullet_size': 10,
        'bullet_count': 3

    }
}
