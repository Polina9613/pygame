import pygame
import os


BASE_IMG_PATH = 'images/'

def load_image(path):
    if 'large_decor' in path:
        img = pygame.image.load(BASE_IMG_PATH + path)
    else:
        img = pygame.image.load(BASE_IMG_PATH + path).convert()
        img.set_colorkey((0, 0, 0))
    if 'flag' in path:
        img = pygame.image.load(BASE_IMG_PATH + path).convert()
        img.set_colorkey((255, 255, 255))
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        if img_name != '.DS_Store':
            images.append(load_image(path + '/' + img_name))
    return images

class Animation:
    def __init__(self, images, img_dur=5):
        self.images = images
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration)


    def update(self):
        self.frame = (self.frame + 1) % (self.img_duration * len(self.images))

    def img(self):
        return self.images[int(self.frame / self.img_duration)]