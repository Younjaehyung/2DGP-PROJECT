from monster import*
from player import*
import time
from collider import*

class GameWorld:
    def __init__(self):
        self.BackGround = load_image("resource/BlackMap.png")
        self.worldL = load_image("resource/leftmap.png")
        self.worldR =load_image("resource/rightmap.png")
        self.worldT = load_image("resource/topmap.png")
        self.worldB =load_image("resource/bottommap.png")
        self.worldmain = load_image("resource/mainmap.png")

        self.worldmap =None

        self.screenSize_W=1200
        self.screenSize_H=800

        self.mapSize_W=576
        self.mapSize_H=576

        self.font = load_font('resource/DungeonFont.ttf', 70)  # 24는 폰트 크기

        self.text = "0"

        self.Gameobjects = [[], []]
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

        CollisionManager().add_collision_pair('player:enemies', self.player, None)

    def handle_event(self,event):

        self.player.handle_event(event)

    def reset_mapsize(self,w,h):
        self.mapSize_W=w
        self.mapSize_H=h


    def update(self):

        self.check_game()
        self.player.update()
                            #2 player update
                            #3 monster update
                            #4 gamelogic update
        pass

    def render(self):

        self.world_render()

        for _enemy in self.enemies:
            if self.player.y < _enemy.y:
                _enemy.render()

        self.player.render()

        for _enemy in self.enemies:
            if self.player.y > _enemy.y:
                _enemy.render()
        self.player_timer()

        pass


    def player_timer(self):
        current_time = time.perf_counter()  # 현재 시간
        self.playerTime =  self.playerTotalTime- (current_time - self.start_time)
        if self.playerTime<10:
            self.font.draw(950, 600, f'{self.playerTime:.2f}', (255, 0, 0))
        else:
            self.font.draw(950, 600, f'{self.playerTime:.2f}', (185, 240, 100))

    def world_render(self):
        if self.playerWhere == 0:
            self.worldmap=self.worldmain
            pass
        elif self.playerWhere == 1:
            self.worldmap=self.worldL
            pass
        elif self.playerWhere == 2:
            self.worldmap=self.worldT
            pass
        elif self.playerWhere == 3:
            self.worldmap=self.worldR
            pass
        elif self.playerWhere == 4:
            self.worldmap=self.worldB
            pass
        self.BackGround.clip_draw(0,0,1200,800,600,400)
        self.worldmap.clip_draw(0, 0, 576, 576, 400,400,800,800)

        pass




    def reset_player(self):
       # self.player = None
        self.playerWhere = 0
        self.start_time = time.perf_counter()
        self.playerLife-=1
        self.stage += 1
        self.player = Player()

    def remove_object(self,o):
        for layer in self.Gameobjects:
            if o in layer:
                layer.remove(o)
                CollisionManager().remove_collision_object(o)
                del o
                return
        raise ValueError('Cannot delete non existing object')

    def reset_enemy(self):
        self.enemiesL = [MonsterL() for i in range(self.stage * 5 * self.penalty)]
        self.enemiesR = [MonsterR() for i in range(self.stage * 5 * self.penalty)]
        self.enemiesT = [MonsterT() for i in range(self.stage * 5 * self.penalty)]
        self.enemiesB = [MonsterB() for i in range(self.stage * 5 * self.penalty)]

        self.enemies = [self.enemiesL, self.enemiesR, self.enemiesT, self.enemiesB]
    def check_monster(self):

        checking_empty=1
        for enemy in self.enemies:
            if enemy.health >= 0 :
                checking_empty=0

        if checking_empty==1:
            return 1    #아무도 없으면 1 반환
        else:
            return 0    #존재하면 0 반환


    def check_game(self):

        if  (self.player.state_machine.cur_state != Dead and self.player.state_machine.cur_state != Death)and (self.playerTime <= 0 or self.player.hp <= 0):
            self.player.state_machine.add_event(('DEAD',0))
        elif self.player.state_machine.cur_state == Death :
            self.reset_player()

            CollisionManager().add_collision_pair('player:enemies', self.player, None)
            for enemies in self.enemies:
                CollisionManager().add_collision_pair('player:enemies', None, enemies)

            return



        else :
            # ////////맵 이동 좌표/////////

            #     2
            # 1  #0  #3
            #     4

            if self.playerWhere==0:
                if self.player.x <= 20 and 350 <= self.player.y <= 450:
                    self.playerWhere = 1
                    self.player.x = 770
                    CollisionManager().collision_pairs.clear()
                    CollisionManager().add_collision_pair('player:enemies', self.player, None)
                    for enemies in self.enemiesL:
                        CollisionManager().add_collision_pair('player:enemies', None, enemies)

                if self.player.x >= 780 and 350 <= self.player.y <= 450:
                    self.playerWhere = 3
                    self.player.x = 30
                    CollisionManager().collision_pairs.clear()
                    CollisionManager().add_collision_pair('player:enemies', self.player, None)
                    for enemies in self.enemiesR:
                        CollisionManager().add_collision_pair('player:enemies', None, enemies)

                if self.player.y >= 780 and 350 <= self.player.x <= 450:
                    self.playerWhere = 2
                    self.player.y = 30
                    CollisionManager().collision_pairs.clear()
                    CollisionManager().add_collision_pair('player:enemies', self.player, None)
                    for enemies in self.enemiesB:
                        CollisionManager().add_collision_pair('player:enemies', None, enemies)

                if self.player.y <= 20 and 350 <= self.player.x <= 450:
                    self.playerWhere = 4
                    self.player.y = 770
                    CollisionManager().collision_pairs.clear()
                    CollisionManager().add_collision_pair('player:enemies', self.player, None)
                    for enemies in self.enemiesT:
                        CollisionManager().add_collision_pair('player:enemies', None, enemies)

            elif self.playerWhere==1:
                if self.player.x >= 780 and 350 <= self.player.y <= 450:
                    self.playerWhere = 0
                    self.player.x = 30
            elif self.playerWhere==2:
                if self.player.y <= 20 and 350 <= self.player.x <= 450:
                    self.playerWhere = 0
                    self.player.y = 770
            elif self.playerWhere==3:
                if self.player.x <= 20 and 350 <= self.player.y <= 450:
                    self.playerWhere = 0
                    self.player.x = 770
            elif self.playerWhere==4:
                if self.player.y >= 780 and 350 <= self.player.x <= 450:
                    self.playerWhere = 0
                    self.player.y = 30



