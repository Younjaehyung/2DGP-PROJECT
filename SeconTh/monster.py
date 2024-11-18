import random

from pico2d import *
import pygame
from monster_state import*
from state_machine import *


class Monster:

    def __init__(self):
        self.x, self.y = random.randrange(100, 600), random.randrange(100, 600)
        self.frame=0
        self.dir=0
        self.damage=0
        self.speed=20
        self.dead_time = 0
        self.health = 200
        self.width = 32
        self.height = 48
        self.type = "monster"
        self.targetx =0
        self.targety =0

        self.health=0
        self.time=0
        self.player_now=0
        self.Attack_status=0 #0 : 기본 상태
        self.image=load_image('resource/Monster/Mon_Slime_1.png')
        self.normal_frame = 0
        self.action_frame =0
        self.flip_x='H'
        self.flip_y = 0
        self.monster_type = 1

        self.handle_x=0
        self.handle_y=0

        self.state_machine = StateMachine(self)  # 어떤 객체를 위한 상태 머신인지 알려줄 필요가 있다
        self.state_machine.start(Idle)  # 객체를 생성한게 아니고, 직접 idle 클래스를 사용

        self.state_machine.set_transitions({
            Idle: {Search_event : Run,time_out: Idle, Dead_event: Dead},
            Run: {Idle_event: Idle,time_out: Run, Dead_event: Dead},
            Dead: {time_out: Death}, Death: {}

        })


    def render(self):
        if self.monster_type is not self.player_now:
            return
        self.state_machine.draw()
        draw_rectangle(*self.return_body_box())
        draw_rectangle(*self.return_weapon_box())

    def update(self,playerwhere):
        self.player_now = playerwhere

        if self.monster_type is not self.player_now:
            return

        self.state_machine.update()



    def attack(self):
        pass

    def search_player(self,o):
        self.targetx, self.targety = o

    def handle_collision(self, group, other):
        if group == 'player:enemies' and self.monster_type is self.player_now:
            if other.state_machine.cur_state == 'Dead':
                pass

        if group == 'player:search'and self.monster_type is self.player_now:
            self.search_player((other.x,other.y))

        if group == 'palayera:enemies' and self.monster_type is self.player_now:
            print("ATTACK PEOPLE")
            pass

        if group == 'enemies:palayera' and (self.monster_type is self.player_now )and other.attack_status == 1:
            self.health-= 10  #플레이어가 적을 공격

            print(f'{self.health} distance :')
            print("ATTACK MONSTER")
            pass
        if group == 'palayera:search' and self.monster_type is self.player_now:
            self.search_player((other.x, other.y))

            #if self.state_machine.cur_state == 'Idle':
            self.state_machine.add_event(('SEARCH', 0))
        else:
            self.state_machine.add_event(('Idle', 0))


    def search_box(self):
        return self.x, self.y,150

    def return_body_box(self):
        return self.x - (self.width/2), self.y - self.height,self.x + (self.width/2),  self.y+self.height

    def return_weapon_box(self):
        return self.x - 15+(self.dir *  15),self.y + 5, self.x - 15+(self.dir *  15)+30,self.y -25


class MonsterT(Monster):
    def __init__(self):
        super().__init__()
        self.monster_type = 2
        self.health=100
        self.image =load_image('resource/Monster/Mon_Slime_1.png')

        #self.image = load_image('run_animation.png')

class MonsterB(Monster):

    def __init__(self):
        super().__init__()
        self.monster_type = 4
        self.health = 100
        self.image =load_image('resource/Monster/Mon_Skeleton_1.png')
        #self.image = load_image('run_animation.png')

class MonsterL(Monster):
    def __init__(self):
        super().__init__()
        self.monster_type = 1
        self.health = 100
        self.image =load_image('resource/Monster/Mon_Beast_1.png')
        #self.image = load_image('run_animation.png')

class MonsterR(Monster):
    def __init__(self):
        super().__init__()
        self.monster_type = 3
        self.health = 100
        self.image =load_image('resource/Monster/Mon_Orc_1.png')
        #self.image = load_image('run_animation.png')
