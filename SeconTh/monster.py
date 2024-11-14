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
        self.speed=0
        self.dead_time = 0

        self.Rect =None
        self.Weapon_Rect =None

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

    def update(self,playerwhere):
        self.player_now = playerwhere

        if self.monster_type is not self.player_now:
            return

        self.state_machine.update()
        self.readjust_box(32,48)

    def attack(self):
        pass

    def search_player(self,o):
        self.targetx, self.targety = o

    def handle_collision(self, group, other):
        if group == 'player:enemies' and self.monster_type is self.player_now:
            if other.state_machine.cur_state == 'Dead':
                pass
            elif other.attack_status == 1:
                self.take_damage(other.attack_stat)
        if group == 'player:search'and self.monster_type is self.player_now:
            self.search_player((other.x,other.y))
            print("CCCCC")



    def readjust_box(self,width,height):
        self.Rect=pygame.Rect(self.x - (width/2), self.y + height, width/2, height)


        self.Weapon_Rect = pygame.Rect(self.x - 15+(self.dir *  15),
                                       self.y + 5, 30, 30)


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
