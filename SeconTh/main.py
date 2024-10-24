import math
from pico2d import *

import gameworld
from gameworld import GameWorld



def gameobject_update():

    game.update()


def gameobject_draw():


    clear_canvas()
    game.render()
    update_canvas()

def handle_input():

        global running
        events = get_events()
        if game.resetflag==2:
            for event in events:
                print('pass')
                pass
            return
        else:
            for event in events:
             if event.type == SDL_QUIT:
                  running = False
             elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                  running = False
             else :
                  game.handle_event(event)


def initialize():
    global game
    global mapH
    global mapW

    game = GameWorld()
    game.resetmapsize(mapW,mapH)



mapH=800
mapW=1200

open_canvas(mapW,mapH)
initialize()


while True:
    handle_input()
    gameobject_update()
    gameobject_draw()
    delay(0.01)

close_canvas()