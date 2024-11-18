from pico2d import load_image, get_time
from state_machine import *
import math
from sdl2 import *


class Idle:
    @staticmethod
    def enter(player,e):

        player.handle_x = 0
        player.handle_y = 0
        player.normal_frame = 0
        player.action_frame = 5
        pass

    @staticmethod
    def exit(player,e):

        pass

    @staticmethod
    def draw(player):


        player.image.clip_composite_draw(
            player.normal_frame * 100,  # 이미지의 왼쪽 상단 x좌표
            player.action_frame * 100,  # 이미지의 왼쪽 상단 y좌표
            100,
            100,
            player.flip_y,
            player.flip_x,
            player.x,
            player.y,
            250,
            250)


        pass

    @staticmethod
    def do(player):


        player.normal_frame = (player.normal_frame + 1) % 6

        # if player.search_player():
        #     player.state_machine.add_event(('SEARCH', 0))

        pass



class Run:
    @staticmethod
    def enter(player,e):

        if Search_event(e):
            player.Attack_status = 1
            player.action_frame =2

        player.action_frame = 4
        player.normal_frame = 0

        pass

    @staticmethod
    def exit(player,e):

        pass

    @staticmethod
    def draw(player):
        player.image.clip_composite_draw(
            player.normal_frame * 100,  # 이미지의 왼쪽 상단 x좌표
            player.action_frame * 100,  # 이미지의 왼쪽 상단 y좌표
            100,
            100,
            player.flip_y,
            player.flip_x,
            player.x,
            player.y,
            250,
            250)
        pass

    @staticmethod
    def do(player):
        if player.Attack_status == 1:
            player.normal_frame = (player.normal_frame + 1) % 6
        else:
            player.normal_frame = (player.normal_frame + 1) % 8

            # 플레이어를 추적하는 로직 추가

        target_x, target_y = player.targetx, player.targety

        # 적과 플레이어 사이의 벡터 계산
        player.handle_x = target_x - player.x
        player.handle_y = target_y - player.y
        distance = math.sqrt(player.handle_x ** 2 + player.handle_y ** 2)

        # 거리 계산 후 방향 정규화 및 이동
        if distance != 0:
            player.handle_x /= distance
            player.handle_y /= distance

        if player.handle_x >0:
            player.flip_x = 'H'

        else:
            player.flip_x = 'h'

        player.x += (player.speed / 20) * player.handle_x
        player.y += (player.speed / 20) * player.handle_y

        pass

class Dead:
    @staticmethod
    def enter(player, e):
        player.normal_frame = 0
        player.action_frame = 0
        player.dead_time =get_time()
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def draw(player):
        player.image.clip_composite_draw(
            player.normal_frame * 100,  # 이미지의 왼쪽 상단 x좌표
            player.action_frame * 100,  # 이미지의 왼쪽 상단 y좌표
            100,
            100,
            player.flip_y,
            player.flip_x,
            player.x,
            player.y,
            250,
            250)
        pass

    @staticmethod
    def do(player):
        if get_time()-player.dead_time > 0.5:
            player.normal_frame = (player.normal_frame + 1) % 4
            player.dead_time =get_time()

        if player.normal_frame == 3:
            player.state_machine.add_event(('TIME_OUT', 0))

        pass


class Death:
    @staticmethod
    def enter(player, e):
        player.normal_frame = 0
        player.action_frame = 0
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def draw(player):
        player.image.clip_composite_draw(
            player.normal_frame * 100,  # 이미지의 왼쪽 상단 x좌표
            player.action_frame * 100,  # 이미지의 왼쪽 상단 y좌표
            100,
            100,
            player.flip_y,
            player.flip_x,
            player.x,
            player.y,
            250,
            250)
        pass

    @staticmethod
    def do(player):

        pass