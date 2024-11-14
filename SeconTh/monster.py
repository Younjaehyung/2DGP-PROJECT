import random

import pygame
from state_machine import *
from monster_state import*

class Monster:
    image = None

    def __init__(self):
        self.x, self.y = random.randrange(100, 600), random.randrange(100, 600)
        self.frame=0
        self.dir=0
        self.damage=0
        self.speed=0
        self.health=0
        self.time=0
        self.Attack_status=0 #0 : 기본 상태

        self.state_machine = StateMachine(self)  # 어떤 객체를 위한 상태 머신인지 알려줄 필요가 있다
        self.state_machine.start(Idle)  # 객체를 생성한게 아니고, 직접 idle 클래스를 사용

        self.state_machine.set_transitions({
            Idle: {time_out: Idle, Dead_event: Dead},
            Run: {Idle_event: Idle,time_out: Run, Dead_event: Dead},

            Attack: {time_out : Idle, Dead_event : Dead},

            Dead: {time_out: Death}, Death: {}

        })




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
        if image == None:
            Monster.image=load_image('resource/Monster/Mon_Slime_1.png')
        #self.image = load_image('run_animation.png')

class MonsterB(Monster):
    image = None
    def __init__(self):
        super().__init__()
        self.monster_type = 2
        self.health = 100
        if image == None:
            Monster.image=load_image('resource/Monster/Skeleton.png')
        #self.image = load_image('run_animation.png')

class MonsterL(Monster):
    image = None
    def __init__(self):
        super().__init__()
        self.monster_type = 3
        self.health = 100
        if image == None:
            Monster.image=load_image('resource/Monster/Werebear.png')
        #self.image = load_image('run_animation.png')

class MonsterR(Monster):
    image = None
    def __init__(self):
        super().__init__()
        self.monster_type = 4
        self.health = 100
        if image == None:
            Monster.image=load_image('resource/Monster/Mon_Orc_1.png')
        #self.image = load_image('run_animation.png')
