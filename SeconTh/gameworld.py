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
        self.Boss = MonsterBoss()
        self.screenSize_W=1200
        self.screenSize_H=800

        self.mapSize_W=576
        self.mapSize_H=576

        self.font = load_font('resource/DungeonFont.ttf', 70)  # 24는 폰트 크기

        self.text = "0"

        self.Gameobjects =[[] for _ in range(5)]
        self.enemies =[]
        self.enemiesL=[]
        self.enemiesR = []
        self.enemiesT = []
        self.enemiesB = []

        self.penalty=1
        self.stage=0
        self.EndStage = 0

        self.start_time = time.perf_counter()
        self.playerTime = 30
        self.playerTotalTime = 30

        self.playerWhere = 0
        self.player = Player()
        self.playerLife=10
        self.playerWhere=0


    def init(self):

        self.reset_player()
        self.reset_enemy()
        print(len(self.Gameobjects[1]))
        print(len(self.Gameobjects[0]))

    def handle_event(self,event):

        self.player.handle_event(event)

    def reset_mapsize(self,w,h):
        self.mapSize_W=w
        self.mapSize_H=h

    def add_object(self,o, depth=0):
        self.Gameobjects[depth].append(o)

    def add_objects(self,ol, depth=0):
        self.Gameobjects[depth] += ol


    def update(self):

        self.check_game()

        for layer in self.Gameobjects:
            for obj in layer:

                obj.update(self.playerWhere)

        CollisionManager().handle_collisions()
        CollisionManager().handle_collisions_a()
        CollisionManager().handle_collisions_s()
                            #2 player update
                            #3 monster update
                            #4 gamelogic update
        pass

    def render(self):

        self.world_render()

        for layer in self.Gameobjects:
            for obj in layer:
                obj.render()

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
        self.remove_object(self.player)
        self.player = Player()
        self.add_object(self.player,0)



    def remove_object(self,o):
        for layer in self.Gameobjects:
            if o in layer:
                layer.remove(o)
                CollisionManager().remove_collision_object(o)
                del o
                return
        #raise ValueError('Cannot delete non existing object')

    def reset_enemy(self):
        for i in range(4):
            self.Gameobjects[i + 1].clear()

        if self.stage==10:

            self.add_object(self.Boss, 1)
            CollisionManager().collision_pairs.clear()
            CollisionManager().collision_pairs_A.clear()
            CollisionManager().collision_pairs_S.clear()
            CollisionManager().add_collision_pair('player:search', self.player, None)
            CollisionManager().add_collision_pair('player:enemies', self.player, None)
            CollisionManager().add_collision_pair_a('palayera:enemies', self.player, None)
            CollisionManager().add_collision_pair_a('enemies:palayera', None, self.player)
            CollisionManager().add_collision_pair_s('palayera:search', self.player, None)

            CollisionManager().add_collision_pair('player:enemies', None, self.Boss)
            CollisionManager().add_collision_pair('player:search', None, self.Boss)
            CollisionManager().add_collision_pair_a('palayera:enemies', None, self.Boss)
            CollisionManager().add_collision_pair_a('enemies:palayera', self.Boss, None)
            CollisionManager().add_collision_pair_s('palayera:search', None, self.Boss)
        else:


            self.enemiesL = [MonsterL() for i in range(self.stage + 2 * self.penalty)]
            self.enemiesR = [MonsterR() for i in range(self.stage + 2 * self.penalty)]
            self.enemiesT = [MonsterT() for i in range(self.stage + 2 * self.penalty)]
            self.enemiesB = [MonsterB() for i in range(self.stage + 2 * self.penalty)]
            self.add_objects(self.enemiesL, 1)
            self.add_objects(self.enemiesT, 2)
            self.add_objects(self.enemiesR, 3)
            self.add_objects(self.enemiesB, 4)

    def check_game(self):

        for layer in self.Gameobjects:
            for _enemey in layer:

                if  _enemey.type =="monster" and _enemey.action_frame ==0 :
                    self.remove_object(_enemey)
                    print("DELETE A")
                    CollisionManager().remove_collision_object_A(_enemey)
                    pass


        if  (self.player.state_machine.cur_state != Dead and self.player.state_machine.cur_state != Death)and (self.playerTime <= 0 or self.player.hp <= 0):
            self.player.state_machine.add_event(('DEAD',0))

        elif self.player.state_machine.cur_state == Death :

            self.reset_player()
            self.reset_enemy()

            return

        elif self.stage!=10 :
            # ////////맵 이동 좌표/////////

            #     2
            # 1  #0  #3
            #     4

            if self.playerWhere==0:
                if self.player.x <= 20 and 350 <= self.player.y <= 450:
                    self.playerWhere = 1
                    self.player.x = 770
                    CollisionManager().collision_pairs.clear()
                    CollisionManager().collision_pairs_A.clear()
                    CollisionManager().collision_pairs_S.clear()
                    CollisionManager().add_collision_pair('player:search', self.player, None)
                    CollisionManager().add_collision_pair('player:enemies', self.player, None)
                    CollisionManager().add_collision_pair_a('palayera:enemies', self.player, None)
                    CollisionManager().add_collision_pair_a('enemies:palayera', None, self.player)
                    CollisionManager().add_collision_pair_s('palayera:search', self.player, None)
                    for enemies in self.enemiesL:
                        CollisionManager().add_collision_pair('player:enemies', None, enemies)
                        CollisionManager().add_collision_pair('player:search', None, enemies)
                        CollisionManager().add_collision_pair_a('palayera:enemies',  None, enemies)
                        CollisionManager().add_collision_pair_a('enemies:palayera', enemies, None)
                        CollisionManager().add_collision_pair_s('palayera:search', None, enemies)

                if self.player.x >= 780 and 350 <= self.player.y <= 450:
                    self.playerWhere = 3
                    self.player.x = 30
                    CollisionManager().collision_pairs.clear()
                    CollisionManager().collision_pairs_A.clear()
                    CollisionManager().collision_pairs_S.clear()
                    CollisionManager().add_collision_pair('player:search', self.player, None)
                    CollisionManager().add_collision_pair('player:enemies', self.player, None)
                    CollisionManager().add_collision_pair_a('palayera:enemies', self.player, None)
                    CollisionManager().add_collision_pair_a('enemies:palayera', None, self.player)
                    CollisionManager().add_collision_pair_s('palayera:search', self.player, None)
                    for enemies in self.enemiesR:
                        CollisionManager().add_collision_pair('player:enemies', None, enemies)
                        CollisionManager().add_collision_pair('player:search', None, enemies)
                        CollisionManager().add_collision_pair_a('palayera:enemies',  None, enemies)
                        CollisionManager().add_collision_pair_a('enemies:palayera', enemies, None)
                        CollisionManager().add_collision_pair_s('palayera:search', None, enemies)

                if self.player.y >= 780 and 350 <= self.player.x <= 450:
                    self.playerWhere = 2
                    self.player.y = 30
                    CollisionManager().collision_pairs.clear()
                    CollisionManager().collision_pairs_A.clear()
                    CollisionManager().collision_pairs_S.clear()
                    CollisionManager().add_collision_pair('player:search', self.player, None)
                    CollisionManager().add_collision_pair('player:enemies', self.player, None)
                    CollisionManager().add_collision_pair_a('palayera:enemies', self.player, None)
                    CollisionManager().add_collision_pair_a('enemies:palayera', None, self.player)
                    CollisionManager().add_collision_pair_s('palayera:search', self.player, None)
                    for enemies in self.enemiesT:
                        CollisionManager().add_collision_pair('player:enemies', None, enemies)
                        CollisionManager().add_collision_pair('player:search', None, enemies)
                        CollisionManager().add_collision_pair_a('palayera:enemies',  None, enemies)
                        CollisionManager().add_collision_pair_a('enemies:palayera', enemies, None)
                        CollisionManager().add_collision_pair_s('palayera:search', None, enemies)

                if self.player.y <= 20 and 350 <= self.player.x <= 450:
                    self.playerWhere = 4
                    self.player.y = 770
                    CollisionManager().collision_pairs.clear()
                    CollisionManager().collision_pairs_A.clear()
                    CollisionManager().collision_pairs_S.clear()
                    CollisionManager().add_collision_pair('player:search', self.player, None)
                    CollisionManager().add_collision_pair('player:enemies', self.player, None)
                    CollisionManager().add_collision_pair_a('palayera:enemies',self.player, None)
                    CollisionManager().add_collision_pair_a('enemies:palayera', None, self.player)
                    CollisionManager().add_collision_pair_s('palayera:search', self.player, None)
                    for enemies in self.enemiesB:
                        CollisionManager().add_collision_pair('player:enemies', None, enemies)
                        CollisionManager().add_collision_pair('player:search', None, enemies)
                        CollisionManager().add_collision_pair_a('palayera:enemies', None, enemies)
                        CollisionManager().add_collision_pair_a('enemies:palayera', enemies, None)
                        CollisionManager().add_collision_pair_s('palayera:search', None, enemies)

            elif self.playerWhere==1:
                if self.player.x >= 780 and 350 <= self.player.y <= 450:
                    self.playerWhere = 0
                    self.player.x = 30
                    CollisionManager().collision_pairs.clear()
            elif self.playerWhere==2:
                if self.player.y <= 20 and 350 <= self.player.x <= 450:
                    self.playerWhere = 0
                    self.player.y = 770
                    CollisionManager().collision_pairs.clear()
            elif self.playerWhere==3:
                if self.player.x <= 20 and 350 <= self.player.y <= 450:
                    self.playerWhere = 0
                    self.player.x = 770
                    CollisionManager().collision_pairs.clear()
            elif self.playerWhere==4:
                if self.player.y >= 780 and 350 <= self.player.x <= 450:
                    self.playerWhere = 0
                    self.player.y = 30
                    CollisionManager().collision_pairs.clear()



