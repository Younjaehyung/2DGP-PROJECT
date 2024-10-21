from monster import*
from player import*
import time


class GameWorld:
    def __init__(self):
       # self.worldL = load_image()
       # self.worldR =
       # self.worldT =
       # self.worldB =
        self.mapSize_W=800
        self.mapSize_H=600
        self.worldmain = load_image("resource/map.png")
        self.font = load_font('resource/DungeonFont.ttf', 70)  # 24는 폰트 크기

        self.text = "0"
        self.Check=0

        self.enemies =[]
        self.enemiesL=[]
        self.enemiesR = []
        self.enemiesT = []
        self.enemiesB = []

        self.penalty=1
        self.stage=1
        self.EndStage = 0

        self.start_time = time.perf_counter()
        self.playerTime = 30
        self.playerTotalTime = 30

        self.playerWhere = 0
        self.player = Player()
        self.playerLife=10
        self.playerWhere=0

    def update(self):
        self.checkstage()   #1 검사
        self.checkplayer()
        self.player.update()

                            #2 player update
                            #3 monster update
                            #4 gamelogic update
        pass

    def render(self):
        self.worldrender()
        self.player.render()
        for _enemy in self.enemies:
            if self.player.y > _enemy:
                self.player.render()
                #_enemy.render()
            else:
                #_enemy.render()
                self.player.render()
        self.playertimer()

        pass


    def playertimer(self):
        current_time = time.perf_counter()  # 현재 시간
        self.playerTime =  self.playerTotalTime- (current_time - self.start_time)
        if self.playerTime<10:
            self.font.draw(400, 500, f'{self.playerTime:.2f}', (255, 0, 0))
        else:
            self.font.draw(400, 500, f'{self.playerTime:.2f}', (185, 240, 100))

    def worldrender(self):
        if self.playerWhere == 0:
            self.worldmain.draw(400,300)
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
    def resetmapsize(self,w,h):
        self.mapSize_W=w
        self.mapSize_H=h

    def resetplayer(self):
        self.player=Player()
        self.player.handle_y=0
        self.player.handle_x=0
        self.playerWhere = 0
        self.start_time = time.perf_counter()
        self.playerLife-=1
        self.stage += 1
        self.playerTime=30

        events = get_events()
        for event in events:
            pass

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
        self.player.hp=0
        pass


    def checkplayer(self):
        if self.playerTime <= 0 or self.player.hp <= 0:
            self.resetplayer()

            #2
        #1  #0  #3
            #4
        if self.player.x < 0:
            self.player.x += (self.player.speed / 50)
        if self.player.x >= self.mapSize_W:
            self.player.x -=(self.player.speed / 50)
        if self.player.y < 0:
            self.player.y += (self.player.speed / 50)
        if self.player.y > self.mapSize_H:
            self.player.y -= (self.player.speed / 50)


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





