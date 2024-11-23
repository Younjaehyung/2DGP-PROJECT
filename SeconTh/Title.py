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
       self.image3 = load_image("resource/title/title3.png")
       self.image4 = load_image("resource/title/title4.png")

    def update(self):
        pass

    def draw(self):
        self.image1.clip_draw(0, 0, 1200, 800, 400, 400, 800, 800)
        self.image2.clip_draw(0,0,1200,800,400,400,800,800)
        self.image3.clip_draw(0, 0, 1200, 800, 400, 400, 800, 800)
        self.image4.clip_draw(0, 0, 1200, 800, 400, 400, 800, 800)
        pass

