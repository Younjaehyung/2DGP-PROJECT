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
        global start
        events = get_events()

        for event in events:
         if event.type == SDL_QUIT:
              running = False
         elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
              running = False
         elif start ==False and event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
              start = True
         else :
              game.handle_event(event)


def initialize():
    global game
    global mapH
    global mapW

    game = GameWorld()
    game.reset_mapsize(mapW,mapH)
    game.init()


mapH=800
mapW=1200
#main_image =load_image('resource/BlackMap.png')
start = False
open_canvas(mapW,mapH)
initialize()


while True:
    if start:
        handle_input()
        gameobject_update()
        gameobject_draw()
        delay(0.02)
    else:
        handle_input()
        #main_image.clip_draw(0,0,1200,800)

close_canvas()