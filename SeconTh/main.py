import math
from pico2d import *

import gameworld
from gameworld import GameWorld



def gameobject_update():
    global game
    game.update()


def gameobject_draw():
    global game
    game.render()


def initialize():
    global game
    game = GameWorld()


initialize()


while True:
    gameobject_update()
    gameobject_draw()