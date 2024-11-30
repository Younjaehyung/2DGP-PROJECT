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
        self.image=load_image('resource/Monster/Mon_Slime_2.png')
        self.image=load_image('resource/Monster/Mon_Slime_3.png')

        self.sfx_image=load_image('resource/NewResource/SFXattack.png')
        self.icon_image=load_image('resource/NewResource/Icon.png')

        self.normal_frame = 0
        self.action_frame =0
        self.current = 0
        self.nowdead =0
        self.flip_x='H'
        self.flip_y = 0
        self.monster_type = 1

        self.handle_x=0
        self.handle_y=0

        self.die_time = 0
        self.attack_time = 0
        self.idle_time = 0
        self.run_time = 0

        self.die_frame = 0
        self.attack_frame = 0
        self.idle_frame = 0
        self.run_frame= 0

        self.state_machine = StateMachine(self)  # 어떤 객체를 위한 상태 머신인지 알려줄 필요가 있다
        self.state_machine.start(Idle)  # 객체를 생성한게 아니고, 직접 idle 클래스를 사용

        self.state_machine.set_transitions({
            Idle: {Monster_Attack : Attack, Search_event : Run,time_out: Idle, Dead_event: Dead},
            Run: {Monster_Attack : Attack, Idle_event: Idle,time_out: Run, Dead_event: Dead},
            Attack : {time_out: Idle ,Dead_event: Dead},
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

        if self.health <= 0 and self.nowdead == 0:
            self.state_machine.add_event(('DEAD', 0))
            print("ATTACK!! MONSTER")
            self.nowdead = 1

        self.state_machine.update()



    def search_player(self,o):
        self.targetx, self.targety = o

    def handle_collision(self, group, other):
        if group == 'player:enemies' and self.monster_type is self.player_now:
            if other.state_machine.cur_state == 'Dead':
                pass


        if group == 'palayera:enemies' and self.monster_type is self.player_now:
            self.current = self.state_machine.cur_state
            self.state_machine.add_event(('Monster_Attack', 0))


        if group == 'enemies:palayera' and (self.monster_type is self.player_now )and other.attack_status == 1:
            if other.normal_frame == 3 or other.normal_frame == 2:
                self.health-= other.attack_stat #플레이어가 적을 공격


            print(f'{self.health} distance :')

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
        return self.x + (30 * self.dir) - 30, self.y + 5, self.x + (30 * self.dir) + 30, self.y - 25


class MonsterT(Monster):
    def __init__(self):
        super().__init__()
        self.monster_type = 2
        self.health=100
        self.damage =1
        self.image =load_image('resource/Monster/Mon_Slime_1.png')

        #self.image = load_image('run_animation.png')

class MonsterT2(Monster):
    def __init__(self):
        super().__init__()
        self.monster_type = 2
        self.health=100
        self.damage =1
        self.image =load_image('resource/Monster/Mon_Slime_2.png')

        #self.image = load_image('run_animation.png')


class MonsterT3(Monster):
    def __init__(self):
        super().__init__()
        self.monster_type = 2
        self.health=100
        self.damage =1
        self.image =load_image('resource/Monster/Mon_Slime_3.png')

        #self.image = load_image('run_animation.png')

class MonsterB(Monster):

    def __init__(self):
        super().__init__()
        self.monster_type = 4
        self.health = 100
        self.damage=2
        self.image =load_image('resource/Monster/Mon_Skeleton_1.png')
        #self.image = load_image('run_animation.png')

class MonsterB2(Monster):

    def __init__(self):
        super().__init__()
        self.monster_type = 4
        self.health = 100
        self.damage=2
        self.image =load_image('resource/Monster/Mon_Skeleton_2.png')
        #self.image = load_image('run_animation.png')

class MonsterB3(Monster):

    def __init__(self):
        super().__init__()
        self.monster_type = 4
        self.health = 100
        self.damage=2
        self.image =load_image('resource/Monster/Mon_Skeleton_3.png')
        #self.image = load_image('run_animation.png')

class MonsterL(Monster):
    def __init__(self):
        super().__init__()
        self.monster_type = 1
        self.health = 100
        self.damage=2
        self.image =load_image('resource/Monster/Mon_Beast_1.png')
        #self.image = load_image('run_animation.png')

class MonsterL2(Monster):
    def __init__(self):
        super().__init__()
        self.monster_type = 1
        self.health = 100
        self.damage=2
        self.image =load_image('resource/Monster/Mon_Beast_2.png')
        #self.image = load_image('run_animation.png')

class MonsterL3(Monster):
    def __init__(self):
        super().__init__()
        self.monster_type = 1
        self.health = 100
        self.damage=2
        self.image =load_image('resource/Monster/Mon_Beast_3.png')
        #self.image = load_image('run_animation.png')


class MonsterR(Monster):
    def __init__(self):
        super().__init__()
        self.monster_type = 3
        self.health = 100
        self.damage=3
        self.image =load_image('resource/Monster/Mon_Orc_1.png')
        #self.image = load_image('run_animation.png')


class MonsterR2(Monster):
    def __init__(self):
        super().__init__()
        self.monster_type = 3
        self.health = 100
        self.damage=3
        self.image =load_image('resource/Monster/Mon_Orc_2.png')
        #self.image = load_image('run_animation.png')


class MonsterR3(Monster):
    def __init__(self):
        super().__init__()
        self.monster_type = 3
        self.health = 100
        self.damage=3
        self.image =load_image('resource/Monster/Mon_Orc_3.png')
        #self.image = load_image('run_animation.png')


class MonsterBoss(Monster):
    def __init__(self):
        super().__init__()
        self.monster_type = 0
        self.health = 1000
        self.damage=2
        self.image =load_image('resource/Monster/Mon_Orc_4.png')
        #self.image = load_image('run_animation.png')