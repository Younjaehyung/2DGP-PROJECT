import random
import time
import os
from player_state import *
from pico2d import *
import pygame
import collider
from state_machine import *


class Player:
    def __init__(self):
        self.x ,self.y=400,400
        self.attack_stat = random.randint(10,30)
        self.hp=random.randint(40,100)
        self.speed=random.randint(100,150)
        self.job = random.randint(1,4)


        self.keydown =[0,0,0,0]

        self.handle_x = 0
        self.handle_y = 0
        self.font = load_font('resource/DungeonFont.ttf', 70)
        self.flip_x='H'
        self.flip_y = 0

        self.status = 0 #0 idle 1 move 2 attack 3 spec attack 4 death 5 none

        self.normal_frame = 0
        self.action_frame = 8

        self.shnormal_frame = 0
        self.lhnormal_frame = 0
        self.spawn_time =0
        self.dead_time = 0
        self.attack_time = 0


        self.heal_image = load_image("resource/Heal_Effect.png")
        self.laser_image = load_image("resource/LASER_Effect.png")
        self.wait_time = get_time()
        # base_path = "resource"

        self.image_action = {1: 7, 2: 8, 3: 7, 4: 6}


        self.state_machine = StateMachine(self)  # 어떤 객체를 위한 상태 머신인지 알려줄 필요가 있다
        self.state_machine.start(Spawn)  # 객체를 생성한게 아니고, 직접 idle 클래스를 사용



        self.state_machine.set_transitions({
            Idle: {right_down: Run, left_down: Run, down_down: Run, up_down: Run,z_down: Attack, Dead_event : Dead},
            Run: {right_down: Run, left_down: Run, down_down: Run, up_down: Run,right_up: Run, left_up: Run, down_up: Run, up_up: Run,Idle_event : Idle,z_down: Attack,Dead_event : Dead},
            Attack: { Dead_event : Dead},
            Spawn:{time_out : Idle},
            Dead: {time_out : Death }, Death: {}

        })





        base_path = os.path.dirname(os.path.abspath(__file__))
        job_paths = {
            1: "Knight/Knight with shadows/Knight.png",
            2: "Knight Templar/Knight Templar with shadows/Knight Templar.png",
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
        if self.hp<=0:
            self.state_machine.add_event(('DEAD', 0))

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
        self.state_machine.draw()
        self.font.draw(self.x, self.y, f'{self.x:.2f},{self.y:.2f}', (255, 0, 0))
        self.font.draw(self.x, self.y + 50, f'{self.attack_stat}', (255, 0, 0))
        self.font.draw(self.x, self.y + 100, f'{self.hp}', (255, 0, 0))
        self.font.draw(self.x, self.y + 150, f'{self.speed}', (255, 0, 0))

        if get_time() - self.wait_time > 0.1:
            self.wait_time = get_time()


        pass

    def handle_event(self,event):
        self.state_machine.add_event(('INPUT', event))



    def take_damage(self, damage):
        self.hp -= damage/30

    def short_press_action(self):
        collider_instance = collider.Collider()
        collider_instance.enemey_take_damage(30)
