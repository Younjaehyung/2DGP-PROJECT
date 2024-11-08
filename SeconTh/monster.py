import random

import pygame
from state_machine import *

class Monster:


    def __init__(self):
        self.x, self.y = random.randrange(100, 600), random.randrange(100, 600)
        self.frame=0
        self.dir=0
        self.damage=0
        self.speed=0
        self.health=0
        self.time=0
        self.status=0 #0 : 기본 상태

        self.state_machine = StateMachine(self)  # 어떤 객체를 위한 상태 머신인지 알려줄 필요가 있다
        self.state_machine.start(Spawn)  # 객체를 생성한게 아니고, 직접 idle 클래스를 사용

        self.state_machine.set_transitions({
            Idle: {right_down: Run, left_down: Run, down_down: Run, up_down: Run, z_down: Idle, time_out: Idle,
                   Dead_event: Dead},
            Run: {right_down: Run, left_down: Run, down_down: Run, up_down: Run, right_up: Run, left_up: Run,
                  down_up: Run, up_up: Run,
                  Idle_event: Idle, z_down: Run, time_out: Run, Dead_event: Dead},

            # Attack: {right_down: Attack, left_down: Attack, right_up: Attack, left_up: Attack ,time_out : Idle, Dead_event : Dead},
            Spawn: {time_out: Idle},
            Dead: {time_out: Death}, Death: {}

        })


       # self.image = load_image('run_animation.png')
    def render(self):
        if self.status==0 : #기본
            pass
            #self.image.clip_draw(self.frame*100,0,100,100,self.x,self.y)
        elif self.status==1 :   #이동
            pass
            #self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)
        elif self.status == 2:  #공격
            pass
            #self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

        self.frame += 1

    def search_player(self):
        pass

    def attack(self):
        pass

class MonsterT(Monster):
    image = None
    def __init__(self):
        super().__init__()
        self.monster_type = 1
        self.health=100
        # if image == None:
        # Monster.image=load_image('run_animation.png')
        #self.image = load_image('run_animation.png')
class MonsterB(Monster):
    image = None
    def __init__(self):
        super().__init__()
        self.monster_type = 2
        self.health = 100
        # if image == None:
        # Monster.image=load_image('run_animation.png')
        #self.image = load_image('run_animation.png')
class MonsterL(Monster):
    image = None
    def __init__(self):
        super().__init__()
        self.monster_type = 3
        self.health = 100
        # if image == None:
        # Monster.image=load_image('run_animation.png')
        #self.image = load_image('run_animation.png')
class MonsterR(Monster):
    image = None
    def __init__(self):
        super().__init__()
        self.monster_type = 4
        self.health = 100
        # if image == None:
        # Monster.image=load_image('run_animation.png')
        #self.image = load_image('run_animation.png')
