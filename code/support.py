from setteing import *

def import_image(*path, format = 'png', alpha = True):
    full_path = join(*path) + f'.{format}'
    return pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()

def import_folder(*path):
    frames = []
    for folder_path,_,file_names in walk(join(*path)):
        for file_name in sorted(file_names, key= lambda name: int(name.split('.')[0])):
                full_path = join(folder_path,file_name)               
                frames.append(pygame.image.load(full_path).convert_alpha())
    return frames

def import_sound(*path, format = 'wav'):
    return pygame.mixer.Sound(join(*path) + f'.{format}')