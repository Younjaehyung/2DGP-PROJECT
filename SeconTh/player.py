import random

from pico2d import *

class Player:
    def __init__(self):
        self.x ,self.y=400,300
        self.attack_stat = random.randint(10,30)
        self.hp=random.randint(40,100)
        self.speed=random.randint(10,30)

        self.handle_x = 0
        self.handle_y = 0

        self.status = 0

        self.normal_frame = 0
        self.action_frame=7
        self.image = load_image("resource/Knight/Knight/Knight.png")
    def update(self):
        self.attack()
        self.move()
        pass
    def render(self):
        flip_x ='H'
        flip_y =0
        if self.handle_x<0:
            flip_x ='h'
        if self.handle_y < 0:
            flip_y = 0





        self.normal_frame = (self.normal_frame +1)%6

        self.image.clip_composite_draw(
            self.normal_frame * 100,  # 이미지의 왼쪽 상단 x좌표
            self.action_frame * 100,  # 이미지의 왼쪽 상단 y좌표
            100,
            100,
            flip_y,
            flip_x,
            self.x,
            self.y,
            250,
            250)
        pass

    def attack(self):
        pass

    def move(self):
        if self.status != 0:
            return
        events = get_events()
        for event in events:
            if self.status==0:
                if event.type == SDL_KEYDOWN:
                    if event.key == SDLK_UP:
                        self.handle_y =self.handle_y+ 1

                    if event.key == SDLK_LEFT:
                        self.handle_x -= 1
                    if event.key == SDLK_RIGHT:
                        self.handle_x += 1

                    if event.key == SDLK_DOWN:
                        self.handle_y -= 1
                elif event.type == SDL_KEYUP:
                    if event.key == SDLK_UP:
                        self.handle_y -= 1
                    if event.key == SDLK_DOWN:
                        self.handle_y += 1
                    if event.key == SDLK_RIGHT:
                        self.handle_x -= 1
                    if event.key == SDLK_LEFT:
                        self.handle_x += 1



        self.x += (self.speed/50) * self.handle_x
        self.y += (self.speed/50) * self.handle_y

    def reset(self):
        self.hp=0