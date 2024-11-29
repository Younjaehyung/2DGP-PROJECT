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

        self.worldRB = load_image("resource/Right_bottom.png")
        self.worldRT = load_image("resource/LEFT_bottom.png")
        self.worldLB = load_image("resource/Right_top.png")     #무친사람아 오른쪽 왼쪽 구별못해!!!

        self.UI = load_image("resource/post.png")
        self.Portrait = load_image("resource/FACE.png")

        self.Obelisk = load_image("resource/Stone.png")


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

        self.Portrait_Num=0
        self.Portrait_frame = 0
        self.Portait_time = 0

        self.enemyLNum = 1
        self.enemyRNum = 1
        self.enemyTNum = 1
        self.enemyBNum = 1

        self.PlayerCoin = 0

        self.LClear = False
        self.RClear = False
        self.TClear = False
        self.BClear = False


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
        self.object_render()
        self.UI_render()
        self.Portrait_render()
        for layer in self.Gameobjects:
            for obj in layer:
                obj.render()

        self.player_timer()
        self.player_coin()

        pass


    #UI그리기
    def UI_render(self):
        self.UI.clip_draw(0, 0, 224, 576, 1000, 400, 224*1.3, 576*1.3)
        pass

    #포트레잇 그리기
    def Portrait_render(self):
        if get_time()-self.Portait_time > 0.2:
            self.Portrait_frame = (self.Portrait_frame + 1) % 2
            self.Portait_time =get_time()


        frame_height = 114  # 각 프레임의 높이
        frame_width = 114  # 각 프레임의 높이
        start_y = self.Portrait_Num * frame_height  # 클립할 영역의 시작 Y 좌표
        self.Portrait.clip_draw(
            0 + self.Portrait_frame * 114, start_y,  # 클립 시작 X, Y 좌표
            114 + self.Portrait_frame * 114, frame_height,  # 클립할 영역의 너비와 높이
            1000, 700,  # 그려질 중심 좌표 (X, Y)
            114 * 1.25, 114 * 1.25  # 출력될 이미지 크기 (스케일링)
        )


    def player_timer(self):
        current_time = time.perf_counter()  # 현재 시간
        self.playerTime =  self.playerTotalTime- (current_time - self.start_time)
        if self.playerTime<10:
            self.font.draw(950, 600, f'{self.playerTime:.2f}', (255, 0, 0))
        else:
            self.font.draw(950, 600, f'{self.playerTime:.2f}', (185, 240, 100))

    def player_coin(self):
        self.font.draw(950, 200, f'{self.PlayerCoin}', (247, 230, 0))

    def object_render(self):
        if self.playerWhere == 0:
            self.Obelisk.clip_draw(0 + ((self.stage-1)*128), 0, 128, 128, 400,410, 128*1.75, 128*1.75)

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
        elif self.playerWhere == 5:
            self.worldmap=self.worldB
            pass
        elif self.playerWhere == 6:
            self.worldmap=self.worldRT
            pass
        elif self.playerWhere == 7:
            self.worldmap=self.worldLB
            pass
        elif self.playerWhere == 8:
            self.worldmap=self.worldRB
            pass
        self.BackGround.clip_draw(0,0,1200,800,600,400)
        self.worldmap.clip_draw(0, 0, 576, 576, 400,400,800,800)

        pass

            # 5   2   6
            # 1   0   3
            # 7   4   8



    def reset_player(self):
       # self.player = None
        self.playerWhere = 0
        self.start_time = time.perf_counter()
        self.playerLife-=1
        self.stage += 1
        self.remove_object(self.player)
        self.player = Player()
        self.Portrait_Num = self.player.Portrait_Num
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
        self.enemyLNum += 2
        self.enemyRNum += 2
        self.enemyTNum += 2
        self.enemyBNum += 2
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

                # L
                if self.enemyLNum > 4:
                    self.enemiesL = [MonsterL2() for _ in range(self.enemyLNum)]
                elif self.enemyLNum > 7:
                    self.enemiesL = [MonsterL3() for _ in range(self.enemyLNum)]
                else:
                    self.enemiesL = [MonsterL() for _ in range(self.enemyLNum)]

                # R
                if self.enemyRNum > 4:
                    self.enemiesR = [MonsterR2() for _ in range(self.enemyRNum)]
                elif self.enemyRNum > 7:
                    self.enemiesR = [MonsterR3() for _ in range(self.enemyRNum)]
                else:
                    self.enemiesR = [MonsterR() for _ in range(self.enemyRNum)]

                # T
                if self.enemyTNum > 4:
                    self.enemiesT = [MonsterT2() for _ in range(self.enemyTNum)]
                elif self.enemyTNum > 7:
                    self.enemiesT = [MonsterT3() for _ in range(self.enemyTNum)]
                else:
                    self.enemiesT = [MonsterT() for _ in range(self.enemyTNum)]

                # B
                if self.enemyBNum > 4:
                    self.enemiesB = [MonsterB2() for _ in range(self.enemyBNum)]
                elif self.enemyBNum > 7:
                    self.enemiesB = [MonsterB3() for _ in range(self.enemyBNum)]
                else:
                    self.enemiesB = [MonsterB() for _ in range(self.enemyBNum)]

                for monster in self.enemiesL:
                    monster.monster_type = 1  # 좌측 맵
                for monster in self.enemiesR:
                    monster.monster_type = 3  # 우측 맵
                for monster in self.enemiesT:
                    monster.monster_type = 2  # 상단 맵
                for monster in self.enemiesB:
                    monster.monster_type = 4  # 하단 맵

                self.add_objects(self.enemiesL, 1)
                self.add_objects(self.enemiesT, 2)
                self.add_objects(self.enemiesR, 3)
                self.add_objects(self.enemiesB, 4)

    def check_game(self):

        for layer in self.Gameobjects:
            for _enemey in layer:
                if _enemey.type == "monster" and _enemey.action_frame == 0:
                    # 방향별 적 수 감소
                    if _enemey in self.enemiesL:
                        self.enemyLNum -= 1
                        self.PlayerCoin += 10
                    elif _enemey in self.enemiesR:
                        self.enemyRNum -= 1
                        self.PlayerCoin += 10
                    elif _enemey in self.enemiesT:
                        self.enemyTNum -= 1
                        self.PlayerCoin += 10
                    elif _enemey in self.enemiesB:
                        self.enemyBNum -= 1
                        self.PlayerCoin += 10

                    # 적 제거 및 충돌 제거
                    self.remove_object(_enemey)
                    CollisionManager().remove_collision_object_A(_enemey)
                    print("DELETE A")

        if  (self.player.state_machine.cur_state != Dead and self.player.state_machine.cur_state != Death)and (self.playerTime <= 0 or self.player.hp <= 0):
            self.player.state_machine.add_event(('DEAD',0))

        elif self.player.state_machine.cur_state == Death :

            self.reset_player()
            self.reset_enemy()

            return


        elif self.stage!=10 :
            # ////////맵 이동 좌표/////////

            # 5   2   6
            # 1   0   3
            # 7   4   8

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

            elif self.playerWhere==1:   #좌
                if self.player.x >= 780 and 350 <= self.player.y <= 450:    #메인(우)로 이동
                    self.playerWhere = 0
                    self.player.x = 30
                    CollisionManager().collision_pairs.clear()
                if self.player.y >= 780 and 350 <= self.player.x <= 450:
                    self.playerWhere = 5
                    self.player.y = 30
                    CollisionManager().collision_pairs.clear()
                if self.player.y <= 20 and 350 <= self.player.x <= 450:
                    self.playerWhere = 7
                    self.player.y = 770
                    CollisionManager().collision_pairs.clear()

            elif self.playerWhere==2:   #상
                if self.player.y <= 20 and 350 <= self.player.x <= 450:     #메인(하)로 이동
                    self.playerWhere = 0
                    self.player.y = 770
                    CollisionManager().collision_pairs.clear()
                if self.player.x >= 780 and 350 <= self.player.y <= 450:    #상우로 이동
                    self.playerWhere = 6
                    self.player.x = 30
                    CollisionManager().collision_pairs.clear()
                if self.player.x <= 20 and 350 <= self.player.y <= 450:     #상좌로 이동
                    self.playerWhere = 5
                    self.player.x = 770
                    CollisionManager().collision_pairs.clear()

            elif self.playerWhere==3:   #우
                if self.player.x <= 20 and 350 <= self.player.y <= 450:     #메인(좌)으로 이동
                    self.playerWhere = 0
                    self.player.x = 770
                    CollisionManager().collision_pairs.clear()
                if self.player.y >= 780 and 350 <= self.player.x <= 450:    #우상으로 이동
                    self.playerWhere = 6
                    self.player.y = 30
                    CollisionManager().collision_pairs.clear()
                if self.player.y <= 20 and 350 <= self.player.x <= 450:     #우하로 이동
                    self.playerWhere = 8
                    self.player.y = 770
                    CollisionManager().collision_pairs.clear()

            elif self.playerWhere==4:   #하
                if self.player.y >= 780 and 350 <= self.player.x <= 450:    #메인(상)으로 이동
                    self.playerWhere = 0
                    self.player.y = 30
                    CollisionManager().collision_pairs.clear()
                if self.player.x >= 780 and 350 <= self.player.y <= 450:    #우하로 이동
                    self.playerWhere = 8
                    self.player.x = 30
                    CollisionManager().collision_pairs.clear()
                if self.player.x <= 20 and 350 <= self.player.y <= 450:     #좌하로 이동
                    self.playerWhere = 7
                    self.player.x = 770
                    CollisionManager().collision_pairs.clear()

            elif self.playerWhere==5: #좌상
                if self.player.x >= 780 and 350 <= self.player.y <= 450:    #메인(우)로 이동
                    self.playerWhere = 2
                    self.player.x = 30
                    CollisionManager().collision_pairs.clear()
                if self.player.y <= 20 and 350 <= self.player.x <= 450:     #메인(하)로 이동
                    self.playerWhere = 1
                    self.player.y = 770
                    CollisionManager().collision_pairs.clear()


            elif self.playerWhere==6:   #우상
                if self.player.x <= 20 and 350 <= self.player.y <= 450:     #상으로 이동
                    self.playerWhere = 2
                    self.player.x = 770
                    CollisionManager().collision_pairs.clear()
                if self.player.y <= 20 and 350 <= self.player.x <= 450:     #메인(하)로 이동
                    self.playerWhere = 3
                    self.player.y = 770
                    CollisionManager().collision_pairs.clear()



            elif self.playerWhere==7:   #좌하
                if self.player.y >= 780 and 350 <= self.player.x <= 450:    #(상)으로 이동
                    self.playerWhere = 1
                    self.player.y = 30
                    CollisionManager().collision_pairs.clear()
                if self.player.x >= 780 and 350 <= self.player.y <= 450:    #(우)로 이동
                    self.playerWhere = 4
                    self.player.x = 30
                    CollisionManager().collision_pairs.clear()

            elif self.playerWhere==8:   #우하
                if self.player.x <= 20 and 350 <= self.player.y <= 450:     #메인(좌)으로 이동
                    self.playerWhere = 4
                    self.player.x = 770
                    CollisionManager().collision_pairs.clear()
                if self.player.y >= 780 and 350 <= self.player.x <= 450:    #메인(상)으로 이동
                    self.playerWhere = 3
                    self.player.y = 30
                    CollisionManager().collision_pairs.clear()
