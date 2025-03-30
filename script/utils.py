import pygame


BASE_IMAGE_PATH = 'data/image/'




#open the map and save the width , length and every mumber in to a list
def load_map(filename):
    map_data = []
    with open(filename, 'rt') as file:
        for line in file:
            map_data.append(line)


            map_width = len(map_data[0])
            map_height = len(map_data)

    print("Loaded Map from file:", map_data)
    return map_data, map_width, map_height


# load image
def load_image(path):
    image = pygame.image.load(BASE_IMAGE_PATH + path).convert_alpha()

    return image


#too complicate
class Animation:
    def __init__(self, folder, image_duration=5, loop=True):
        pass







