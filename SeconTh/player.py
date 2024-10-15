import random

class Player:
    def __init__(self):
        self.x ,self.y=400,300
        self.attack_stat = random.randint(10,30)
        self.hp=random.randint(40,100)
        self.speed=random.randint(10,30)

    def update(self):

    def render(self):


    def attack(self):

    def move(self):



    def reset(self):
        self.hp=0