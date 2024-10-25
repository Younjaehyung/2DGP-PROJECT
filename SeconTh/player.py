import random
import time
from pico2d import *

class Player:
    def __init__(self):
        self.x ,self.y=400,300
        self.attack_stat = random.randint(10,30)
        self.hp=random.randint(40,100)
        self.speed=random.randint(100,150)

        self.cooltime = 2
        self.is_key_down = False
        self.key_pressed_time = None

        self.handle_x = 0
        self.handle_y = 0
        self.font = load_font('resource/DungeonFont.ttf', 70)
        self.flip_x='H'
        self.flip_y = 0

        self.status = 0 #0 idle 1 move 2 attack 3 spec attack 4 death 5 none
        self.prevstatus=0
        self.normal_frame = 0
        self.action_frame=7
        #self.image = load_image("resource/Knight/Knight with shadows/Knight.png")
        #self.image = load_image("resource/Soldier/Soldier with shadows/Soldier.png")
        #self.image = load_image("resource/Lancer/Lancer with shadows/Lancer.png")
        self.image = load_image("resource/Armored Axeman/Armored Axeman with shadows/Armored Axeman.png")
        #self.image = load_image("resource/plalyer_move.png")

    def update(self):



        #self.attack()

        if self.prevstatus != self.status:
            self.normal_frame = 0

            self.prevstatus = self.status

        self.move()
        pass
    def render(self):
        if self.handle_x<0:
            self.flip_x ='h'
        elif self.handle_x>0:
            self.flip_x = 'H'
        if self.handle_y < 0:
            self.flip_y = 0
        elif self.handle_y > 0:
            self.flip_y = 0



        if self.status==0:
            self.action_frame=6
            self.normal_frame = (self.normal_frame + 1) % 6
        elif self.status==1:
            self.action_frame=5
            self.normal_frame = (self.normal_frame + 1) % 8

        elif self.status == 2:
            self.action_frame = 5
            self.normal_frame = (self.normal_frame + 1) % 7
            if self.normal_frame==0:
                self.status = 0
        elif self.status == 3:
            self.action_frame = 3
            self.normal_frame = (self.normal_frame + 1) % 10
            if self.normal_frame==0:
                self.status = 0



        self.image.clip_composite_draw(
            self.normal_frame * 100,  # 이미지의 왼쪽 상단 x좌표
            self.action_frame * 100,  # 이미지의 왼쪽 상단 y좌표
            100,
            100,
            self.flip_y,
            self.flip_x,
            self.x,
            self.y,
            250,
            250)

        self.font.draw(self.x, self.y, f'{self.x:.2f},{self.y:.2f}', (255, 0, 0))
        pass

    def handle_event(self,event):
            if event.type == SDL_KEYDOWN and event.key == SDLK_x:
                self.long_press_action()

          #  if event.type == SDL_KEYDOWN and event.key == SDLK_z:
           #   if not self.is_key_down:  # 키가 처음 눌렸을 때만 시간 기록
             #       self.key_pressed_time = time.time()  # 키가 눌린 시간을 기록
               #     self.is_key_down = True


            #elif event.type == SDL_KEYUP and event.key == SDLK_z:
              #  if self.is_key_down:
                 #   key_released_time = time.time()  # 키가 떼어진 시간을 기록
                 #   pressed_duration = key_released_time - self.key_pressed_time  # 눌린 시간 계산

                 #   if pressed_duration < 0.5:
                 #       self.short_press_action()  # 짧게 누른 액션
                #    else:
                 #       self.long_press_action()  # 길게 누른 액션

                 #   self.is_key_down = False  # 키가 떼어졌으므로 초기화


            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_UP:
                        self.handle_y += 1
                        self.status = 1
                if event.key == SDLK_LEFT:
                        self.handle_x -= 1
                        self.status = 1
                if event.key == SDLK_RIGHT:
                        self.handle_x += 1
                        self.status = 1
                if event.key == SDLK_DOWN:
                        self.handle_y -= 1
                        self.status = 1
            elif event.type == SDL_KEYUP:
                if event.key == SDLK_UP:
                        self.handle_y -= 1
                        self.status = 0
                if event.key == SDLK_DOWN:
                        self.handle_y += 1
                        self.status = 0
                if event.key == SDLK_RIGHT:
                        self.handle_x -= 1
                        self.status = 0
                if event.key == SDLK_LEFT:
                        self.handle_x += 1
                        self.status = 0




    def short_press_action(self):
        self.status = 2

    def long_press_action(self):
        self.status = 3

    def move(self):







        self.x += (self.speed/50) * self.handle_x
        self.y += (self.speed/50) * self.handle_y


    def reset(self):
        self.hp=0