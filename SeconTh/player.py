import random
import time
import os

from pico2d import *
import pygame
import collider
from player_state import *
from state_machine import *


class Player:
    def __init__(self, hpLv=0, atkLv=0, spdLv=0, skillLv=0):
        self.x, self.y = 400, 400

        # 플레이어 레벨 초기화
        self.hpLv = hpLv
        self.spdLv = spdLv
        self.skillLv = skillLv
        self.atkLv = atkLv

        self.attack_stat = random.randint(10 + self.atkLv * 5, 20 + self.atkLv * 5)
        self.hp = random.randint(75 + self.hpLv * 60, 125 + self.hpLv * 60)
        self.speed = random.randint(200 + self.spdLv * 20, 250 + self.spdLv * 20)
        self.job = random.randint(1, 4)

        self.attack_width = None
        self.attack_height = None
        self.dir = 1
        if self.job == 1:  # 칼
            self.attack_width = 45
            self.attack_height = 45
            self.Portrait_Num = random.randint(6, 7)
        elif self.job == 2:  # 스피어
            self.attack_width = 80
            self.attack_height = 20
            self.Portrait_Num = random.randint(4, 5)
        elif self.job == 3:  # 렌서
            self.attack_width = 70
            self.attack_height = 20
            self.Portrait_Num = random.randint(2, 3)
        elif self.job == 4:  # 도
            self.attack_width = 45
            self.attack_height = 50
            self.Portrait_Num = random.randint(0, 1)

        self.keydown = [0, 0, 0, 0]

        self.type = "player"

        self.current = 0
        self.upgrade_image=load_image('resource/NewResource/Icon.png')
        self.upgrade_start_time = None  # 업그레이드 이미지 표시 시작 시간 추가
        self.show_upgrade = False  # 업그레이드 이미지 표시 여부
        self.upgrade_type = 0 #0: 없음 1: 공격 2: 속도 3: 체력 4: 스킬

        self.handle_x = 0
        self.handle_y = 0
        self.font = load_font('resource/DungeonFont.ttf', 70)
        self.flip_x = 'H'
        self.flip_y = 0
        self.normal_frame = 0
        self.action_frame = 8
        self.player_now = 0
        self.status = 0  # 0 idle 1 move 2 attack 3 spec attack 4 death 5 none
        self.attack_status = 0

        self.coin = 0
        # Idle
        self.Rect = None  # 좌측 상단 xy 가로 세로 길이
        # Attack(weapon)
        self.Weapon_Rect = None
        self.level = 0

        self.shnormal_frame = 0
        self.lhnormal_frame = 0
        self.spawn_time = 0
        self.dead_time = 0
        self.attack_time = 0

        self.width = 32
        self.height = 48

        self.heal_image = load_image("resource/Heal_Effect.png")
        self.LevelUp_image = load_image("resource/NewResource/LevelUp_effect.png")
        self.lvUp_frame = 0
        self.laser_image = load_image("resource/LASER_Effect.png")

        self.wait_time = get_time()
        self.run_time = get_time()
        # base_path = "resource"
        self.LVup_sound = load_wav('resource/NewResource/Seconth_LevelUp.wav')
        self.LVup_sound.set_volume(100)

        self.image_action = {1: 7, 2: 8, 3: 7, 4: 6}

        self.state_machine = StateMachine(self)  # 어떤 객체를 위한 상태 머신인지 알려줄 필요가 있다
        self.state_machine.start(Spawn)  # 객체를 생성한게 아니고, 직접 idle 클래스를 사용

        self.state_machine.set_transitions({
            Idle: {right_down: Run, left_down: Run, down_down: Run, up_down: Run, z_down: Idle, time_out: Idle,
                   Dead_event: Dead, hit: Hit},
            Run: {right_down: Run, left_down: Run, down_down: Run, up_down: Run, right_up: Run, left_up: Run,
                  down_up: Run, up_up: Run,
                  Idle_event: Idle, z_down: Run, time_out: Run, Dead_event: Dead},
            Hit: {time_out: Idle},
            # Attack: {right_down: Attack, left_down: Attack, right_up: Attack, left_up: Attack ,time_out : Idle, Dead_event : Dead},
            Spawn: {time_out: Idle},
            Dead: {time_out: Death}, Death: {}

        })

        base_path = os.path.dirname(os.path.abspath(__file__))
        job_paths = {
            # 1: "Knight/Knight with shadows/Knight.png",
            # 2: "Knight Templar/Knight Templar with shadows/Knight Templar.png",
            # 3: "Lancer/Lancer with shadows/Lancer.png",
            # 4: "Armored Axeman/Armored Axeman with shadows/Armored Axeman.png"
            1: "Hero_Sword.png",
            2: "Hero_Spear.png",
            3: "Hero_Lancer.png",
            4: "Hero_Axe.png"

        }
        self.image = 0
        if self.job ==1:
            self.image = load_image('resource/Hero_Sword.png')
        if self.job ==2:
            self.image = load_image('resource/Hero_Spear.png')
        if self.job ==3:
            self.image = load_image('resource/Hero_Lancer.png')
        if self.job ==4:
            self.image = load_image('resource/Hero_Axe.png')

        # Pygame 이미지 경로
        #image_path = os.path.join(base_path, "resource", job_paths.get(self.job, ''))
        #print(f"Image path: {image_path}")  # 경로 확인용
        #image_path2 = os.path.join(base_path, "resource")
        # 경로 및 파일 존재 여부 확인

        #self.image = load_image(image_path)

        # Pygame에서 이미지 로드


    def update(self, player_now):

        self.state_machine.update()
        self.run_time = get_time()
        print(self.x - 32 / 2, self.y + 48, 32, 48)
        self.player_now = player_now

        if self.hp <= 0:
            self.state_machine.add_event(('DEAD', 0))

        pass

    def render(self):

        if self.handle_x < 0:
            self.flip_x = 'h'
            self.dir = -1
        elif self.handle_x > 0:
            self.flip_x = 'H'
            self.dir = 1
        if self.handle_y < 0:
            self.flip_y = 0
        elif self.handle_y > 0:
            self.flip_y = 0
        self.state_machine.draw()
        #self.font.draw(self.x, self.y + 50, f'{self.x:.2f},{self.y:.2f}', (255, 0, 0))
        #self.font.draw(self.x, self.y + 100, f'{self.attack_stat}', (255, 0, 0))
        #self.font.draw(self.x, self.y + 150, f'{self.hp}', (255, 0, 0))
        #self.font.draw(self.x, self.y + 200, f'{self.speed}', (255, 0, 0))
        # ┌┐└┘

        #draw_rectangle(*self.return_body_box())
        #draw_rectangle(*self.return_weapon_box())
        #draw_rectangle(100, 100, 200, 200)

        if self.show_upgrade:

            self.upgrade_image.clip_draw((self.upgrade_type-1)*32, 0, 32, 32, self.x, self.y + 75, 50, 50)
            self.LevelUp_image.clip_draw(self.lvUp_frame*100, 0, 100, 100, self.x, self.y, 350, 350)
            if get_time() - self.upgrade_start_time > 0.7:
                self.show_upgrade = False

        if get_time() - self.wait_time > 0.1:
            self.lvUp_frame = (self.lvUp_frame + 1) % 4
            self.wait_time = get_time()

        pass

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))

        if self.player_now == 5 and 350 <= self.y <= 450 and 350 <= self.x <= 450:
            if event.type == SDL_KEYDOWN and event.key == SDLK_f:
                self.coin += random.randint(-1,3)
                self.show_upgrade = True  # 업그레이드 이미지 표시 활성화
                self.upgrade_type = 5
                self.upgrade_start_time = get_time()  # 현재 시간을 기록
                self.LVup_sound.play()

        if self.player_now == 6 and 350 <= self.y <= 450 and 350 <= self.x <= 450:
            if event.type == SDL_KEYDOWN and event.key == SDLK_f and self.coin >= 30:
                self.spdLv += 1
                self.coin -= 30
                self.show_upgrade = True  # 업그레이드 이미지 표시 활성화
                self.upgrade_type = 2
                self.upgrade_start_time = get_time()  # 현재 시간을 기록
                self.LVup_sound.play()

        if self.player_now == 7 and 350 <= self.y <= 450 and 350 <= self.x <= 450:
            if event.type == SDL_KEYDOWN and event.key == SDLK_f and self.coin >= 30:
                self.atkLv += 1
                self.coin -= 30
                self.show_upgrade = True  # 업그레이드 이미지 표시 활성화
                self.upgrade_type = 1
                self.upgrade_start_time = get_time()  # 현재 시간을 기록
                self.LVup_sound.play()

        if self.player_now == 8 and 350 <= self.y <= 450 and 350 <= self.x <= 450:
            if event.type == SDL_KEYDOWN and event.key == SDLK_f and self.coin >= 30:
                self.hpLv += 1
                self.coin -= 30
                self.show_upgrade = True  # 업그레이드 이미지 표시 활성화
                self.upgrade_type = 3
                self.upgrade_start_time = get_time()  # 현재 시간을 기록
                self.LVup_sound.play()

        # if  350 <= self.y <= 450 and 350 <= self.x <= 450:     #업그레이드
        #     if self.player_now==5:
        #         if event.type == SDL_KEYDOWN and event.key == SDLK_f and self.coin >= 50:
        #             self.hpLv += 1
        #             self.coin -= 50
        #     elif self.player_now==6:
        #         if event.type == SDL_KEYDOWN and event.key == SDLK_f and self.coin >= 50:
        #             self.spdLv += 1
        #             self.coin -= 50
        #     elif self.player_now == 7:
        #         if event.type == SDL_KEYDOWN and event.key == SDLK_f and self.coin >= 50:
        #             self.atkLv += 1
        #             self.coin -= 50
        #     elif self.player_now == 8:
        #         if event.type == SDL_KEYDOWN and event.key == SDLK_f and self.coin >= 50:
        #             self.skillLv += 1
        #             self.coin -= 50

    def take_damage(self, damage):
        self.hp -= damage

    def handle_collision(self, group, other):
        if group == 'player:enemies' and other.normal_frame == 3:
            if other.normal_frame == 1:
                self.hp -= 0.5
            pass

        if group == 'palayera:enemies' and other.Attack_status == 1:  # 적이 플레이어 공격
            if other.normal_frame == 1:
                self.hp -= other.damage
                self.state_machine.add_event(('hit', 0))
            # self.state_machine.add_event(('TIME_OUT', 0))
            print("-HEL")
            pass
        if group == 'enemies:palayera':
            pass
            # print("")

    def return_body_box(self):
        return self.x - (self.width / 2), self.y - self.height, self.x, self.y + self.height

    def return_weapon_box(self):
        if self.job == 1:
            return self.x + (30 * self.dir) - 55, self.y + 15, self.x + (30 * self.dir) + 30, self.y - 25
        if self.job == 2:
            return self.x + (30 * self.dir) - 55, self.y + 15, self.x + (30 * self.dir) + 30, self.y - 25
        if self.job == 3:
            return self.x + (30 * self.dir) - 55, self.y + 15, self.x + (30 * self.dir) + 30, self.y - 25
        if self.job == 4:
            return self.x + (30 * self.dir) - 55, self.y + 15, self.x + (30 * self.dir) + 30, self.y - 25
