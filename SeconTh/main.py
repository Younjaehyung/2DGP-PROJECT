import math
from turtledemo.penrose import start

from pico2d import *

import gameworld
from gameworld import GameWorld
from Title import *

def initialize():
    global game
    global mapH
    global mapW
    global gametitle
    global start
    global gameend
    global end
    end = False
    start = True


    gametitle = Title()
    gameend = End()

def gameobject_update():

    game.update()


def gameobject_draw():


    clear_canvas()
    game.render()
    update_canvas()

def handle_input():
        global running
        global start
        global game
        events = get_events()

        for event in events:
         if event.type == SDL_QUIT:
              running = False
         elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
              running = False
         elif start ==True and event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
              start = False
         elif start == False:
              game.handle_event(event)

def title_draw():
    clear_canvas()
    gametitle.draw()
    update_canvas()

def end_draw():
    clear_canvas()
    gameend.draw()
    update_canvas()

def end_draw2():
    clear_canvas()
    gameend.draw2()
    update_canvas()


mapH=800
mapW=1200
endstate=0

open_canvas(mapW,mapH)
initialize()

while start:
    handle_input()
    gametitle.update()
    title_draw()

game = GameWorld()
game.reset_mapsize(mapW,mapH)
game.init()
while True:
    handle_input()
    gameobject_update()
    gameobject_draw()
    if game.stage==11 and game.playerLife <=0:
        endstate=1
        break
    elif game.stage==11:
        endstate=2
        break
    delay(0.02)
while True:
    handle_input()
    if endstate==1:
        end_draw()
    elif endstate==2:
        end_draw2()
close_canvas()