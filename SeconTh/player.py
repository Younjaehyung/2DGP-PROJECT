import random
import time
import os
from pico2d import *
import pygame
import collider
from state_machine import *

class Idle:
    @staticmethod
    def enter(boy,e):
        boy.start_time = get_time()     #현재 시간으 기록

        #움직이다가 멈춘 경우
        if left_up(e) or right_down(e):
            boy.action = 2
            boy.face_dir = -1
        elif right_up(e) or left_down(e) or start_event(e):
            boy.action = 3
            boy.face_dir = 1
        elif time_out(e):
            if boy.dir >0:
                boy.action = 3
                boy.face_dir = 1
            elif boy.dir < 0:
                boy.action = 2
                boy.face_dir = -1

        boy.frame = 0
        boy.dir = 0
        pass

    @staticmethod
    def exit(boy,e):
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 5:
            #이벤트를 발생
            boy.state_machine.add_event(('TIME_OUT',0))
        pass




class Player:
    def __init__(self):
        self.x ,self.y=400,300
        self.attack_stat = random.randint(10,30)
        self.hp=random.randint(40,100)
        self.speed=random.randint(100,150)
        self.job = random.randint(1,4)
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
        self.action_frame=8

        self.state_machine = StateMachine(self)  # 어떤 객체를 위한 상태 머신인지 알려줄 필요가 있다
        self.state_machine.start(Idle)  # 객체를 생성한게 아니고, 직접 idle 클래스를 사용

        self.state_machine.set_transitions({
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, a_down: AutoRun, time_out: Sleep},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
            Attack: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: Idle},
            Dead: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, time_out: Idle}

        })

        self.wait_time = get_time()
        #base_path = "resource"
        base_path = os.path.dirname(os.path.abspath(__file__))
        job_paths = {
            1: "Knight/Knight with shadows/Knight.png",
            2: "Soldier/Soldier with shadows/Soldier.png",
            3: "Lancer/Lancer with shadows/Lancer.png",
            4: "Armored Axeman/Armored Axeman with shadows/Armored Axeman.png"
        }

        # Pygame 이미지 경로
        image_path = os.path.join(base_path, "resource", job_paths.get(self.job, ''))
        print(f"Image path: {image_path}")  # 경로 확인용

        # 경로 및 파일 존재 여부 확인
        if not os.path.exists(image_path):
            print(f"Error: File does not exist at {image_path}")
            return

        # pico2d에서 이미지 로드
        self.image = load_image(image_path)

        # Pygame에서 이미지 로드
        try:
            self.colliderImage = pygame.image.load(image_path).convert_alpha()
            self.rect = self.colliderImage.get_rect(topleft=(self.x, self.y))
        except pygame.error as e:
            print(f"Error loading image with pygame: {e}")

    def update(self):
        self.state_machine.update()


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

        if get_time() - self.wait_time > 0.1:
            self.wait_time = get_time()

            if self.status==0:
                self.action_frame=7
                self.normal_frame = (self.normal_frame + 1) % 6
            elif self.status==1:
                self.action_frame=6
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

        # 좌표 test
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



    def take_damage(self, damage):
        self.hp -= damage/30

    def short_press_action(self):
        self.status = 2
        collider_instance = collider.Collider()
        collider_instance.enemey_take_damage(30)

    def long_press_action(self):
        self.status = 3


    def move(self):


        self.x += (self.speed/20) * self.handle_x
        self.y += (self.speed/20) * self.handle_y


    def reset(self):
        self.hp=0