import random
import time
import os

from pico2d import *
import pygame
import collider

class Title:
    def __init__(self):
        self.image1 = load_image("resource/title/title1.png")
        self.image2 = load_image("resource/title/title2.png")
        self.imagen2 = load_image("resource/title/title2.png")
        self.image3 = load_image("resource/title/title3.png")
        self.imagen3 = load_image("resource/title/title3.png")
        self.image4 = load_image("resource/title/title4.png")
        self.title2_x = 600
        self.title2_nx = -600
        self.title3_x = 600
        self.title3_nx = -600

    def update(self):
        self.title2_x += 3
        self.title2_nx += 3
        self.title3_x += 1
        self.title3_nx += 1

        if self.title2_x > 1800:
            self.title2_x = 600

        if self.title2_nx > 600:
            self.title2_nx = -600

        if self.title3_x > 1800:
            self.title3_x = 600

        if self.title3_nx > 600:
            self.title3_nx = -600


    def draw(self):
        self.image1.clip_draw(0, 0, 1200, 800, 600, 400)
        self.imagen2.clip_draw(0, 0, 1200, 800, self.title2_nx, 400)
        self.image2.clip_draw(0, 0, 1200, 800, self.title2_x, 400)
        self.image3.clip_draw(0, 0, 1200, 800, self.title3_nx, 400)
        self.image3.clip_draw(0, 0, 1200, 800, self.title3_x, 400)
        self.image4.clip_draw(0, 0, 1200, 800, 600, 400)
        pass


class End:
    def __init__(self):
       self.image = load_image("resource/BlackMap.png")

       self.image2 = load_image("resource/BlackMap.png")
       self.imagem = load_image("resource/BlackMap.png")

       self.imagep = load_image("resource/BlackMap.png")
    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 1200, 800, 600,400)
        # self.image.clip_draw(0, 0, 1200, 800, 600, 400)
        pass
    def draw2(self):
        self.image2.clip_draw(0, 0, 1200, 800, 600,400)
        #self.image.clip_draw(0, 0, 1200, 800, 600, 400)
        pass