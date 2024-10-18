import math
from pico2d import *

import gameworld
from gameworld import GameWorld



def gameobject_update():
    global game
    game.update()


def gameobject_draw():
    global game

    clear_canvas()
    game.render()
    update_canvas()

def initialize():
    global game
    game = GameWorld()

open_canvas()
initialize()


while True:
    gameobject_update()
    gameobject_draw()

close_canvas()