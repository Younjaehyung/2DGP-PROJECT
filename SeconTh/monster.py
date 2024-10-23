import random

import pygame


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
