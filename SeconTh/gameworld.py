from monster import*
from player import*



class GameWorld:
    def __init__(self):
       # self.worldL = load_image()
       # self.worldR =
       # self.worldT =
       # self.worldB =

        self.Check=0

        self.enemies =[]
        self.enemiesL=[]
        self.enemiesR = []
        self.enemiesT = []
        self.enemiesB = []

        self.penalty=1
        self.stage=1
        self.EndStage = 0

        self.playerTime = 30
        self.playerWhere = 0
        self.player = Player()
        self.playerLife=10
        self.playerWhere=0

    def update(self):
        self.checkstage()   #1 검사
        self.player.update()
                            #2 player update
                            #3 monster update
                            #4 gamelogic update
        pass

    def render(self):
        self.player.render()
        if self.playerWhere == 1:
            self

        for _enemy in self.enemies:
            if self.player.y > _enemy:
                self.player.render()
                _enemy.render()
            else:
                _enemy.render()
                self.player.render()


        pass
    def worldrender(self):
        if self.playerWhere == 0:
            pass
        elif self.playerWhere == 1:
            pass
        elif self.playerWhere == 2:
            pass
        elif self.playerWhere == 3:
            pass
        elif self.playerWhere == 4:
            pass

        pass
    def enterfield(self):
        pass


    def resetplayer(self):
        self.player=Player()
        self.playerWhere = 0
        self.playerlife-=1
        self.stage += 1
        self.playerTime=30

    def resetenemy(self):
        self.enemiesL = [MonsterL() for i in range(self.stage * 5 * self.penalty)]
        self.enemiesR = [MonsterR() for i in range(self.stage * 5 * self.penalty)]
        self.enemiesT = [MonsterT() for i in range(self.stage * 5 * self.penalty)]
        self.enemiesB = [MonsterB() for i in range(self.stage * 5 * self.penalty)]

        self.enemies = [self.enemiesL, self.enemiesR, self.enemiesT, self.enemiesB]

    def checkstage(self):

        if self.player.hp <= 0 <= self.playerTime:
            self.penalty +=1
        elif self.player.hp>=0 and self.checkmonster():
            pass

    def checkmonster(self):
        checking_empty=1
        for enemy in self.enemies:
            if enemy.health >= 0 :
                checking_empty=0

        if checking_empty==1:
            return 1    #아무도 없으면 1 반환
        else:
            return 0    #존재하면 0 반환


    def killplayer(self):
        pass


    def checkplayer(self):
        if self.playerTime <= 0 or self.player.hp <= 0:
            self.resetplayer()
            self.playerWhere=0
            #2
        #1  #0  #3
            #4

        if self.playerWhere==0:
            if self.player.x <= 0 and 250 <= self.player.y <= 350:
                self.playerWhere = 1
            if self.player.x >= 800 and 250 <= self.player.y <= 350:
                self.playerWhere = 3
            if self.player.y >= 600 and 350 <= self.player.x <= 450:
                self.playerWhere = 2
            if self.player.y <= 0 and 350 <= self.player.x <= 450:
                self.playerWhere = 4
        elif self.playerWhere==1:
            if self.player.x >= 800 and 250 <= self.player.y <= 350:
                self.playerWhere = 0
        elif self.playerWhere==2:
            if self.player.y <= 0 and 250 <= self.player.x <= 350:
                self.playerWhere = 0
        elif self.playerWhere==3:
            if self.player.x <= 0 and 350 <= self.player.y <= 450:
                self.playerWhere = 0
        elif self.playerWhere==4:
            if self.player.y >= 600 and 350 <= self.player.x <= 450:
                self.playerWhere = 0





