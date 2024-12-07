from pico2d import load_image, get_time
from state_machine import *
import math
from sdl2 import *


class Idle:
    @staticmethod
    def enter(player, e):
        player.handle_x = 0
        player.handle_y = 0
        player.normal_frame = 0
        player.action_frame = 5
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
            300,
            300)

        pass

    @staticmethod
    def do(player):
        if get_time() - player.idle_time > 0.15:
            player.normal_frame = (player.normal_frame + 1) % 6
            player.idle_time = get_time()

        # if player.search_player():
        #     player.state_machine.add_event(('SEARCH', 0))

        pass


class Run:
    @staticmethod
    def enter(player, e):

        if Search_event(e):
            player.Attack_status = 0
            player.action_frame = 2

        player.action_frame = 4
        player.normal_frame = 0

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
            300,
            300)
        pass

    @staticmethod
    def do(player):
        if get_time() - player.run_time > 0.2:
            player.normal_frame = (player.normal_frame + 1) % 8
            player.run_time = get_time()

            # 플레이어를 추적하는 로직 추가

        target_x, target_y = player.targetx, player.targety

        # 적과 플레이어 사이의 벡터 계산
        player.handle_x = target_x - player.x
        player.handle_y = target_y - player.y
        distance = math.sqrt((player.handle_x ** 2) + (player.handle_y ** 2))

        # 거리 계산 후 방향 정규화 및 이동

        if distance <= 20:
            return

        elif distance != 0:
            player.handle_x /= distance
            player.handle_y /= distance

        if player.handle_x > 0:
            player.flip_x = 'H'
            player.dir = 1

        else:
            player.flip_x = 'h'
            player.dir = -1

        player.x += (player.speed / 20) * player.handle_x
        player.y += (player.speed / 20) * player.handle_y

        pass


class Attack:
    @staticmethod
    def enter(player, e):

        player.Attack_status = 1
        player.action_frame = 3

        player.normal_frame = 0

        pass

    @staticmethod
    def exit(player, e):
        player.Attack_status = 0

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
            300,
            300)
        pass

    @staticmethod
    def do(player):
        if get_time() - player.attack_time > 0.2:
            player.normal_frame = (player.normal_frame + 1) % 6
            player.attack_time = get_time()


            # 플레이어를 추적하는 로직 추가
        if player.normal_frame == 0:
            player.state_machine.add_event(('TIME_OUT', 0))

        pass


class Dead:
    @staticmethod
    def enter(player, e):
        player.normal_frame = 0
        player.action_frame = 1
        player.dead_time = get_time()
        player.fly_back_distance = 100  # 뒤로 날아가는 최대 거리
        player.fly_back_speed = 5  # 뒤로 날아가는 속도
        player.sfx_frame = 0  # SFX 이미지의 초기 프레임
        player.sfx_time = get_time()  # SFX 애니메이션 시간 초기화
        player.ATK_sound.play()
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
            300,
            300)

        player.icon_image.clip_draw(
            128, 0, 32, 32,  # 아이콘 크기
            player.x, player.y + 50,  # 몬스터 위쪽에 렌더링
            50, 50  # 출력 크기
        )

        player.sfx_image.clip_draw(
            player.sfx_frame * 100, 0,  # SFX 프레임의 x 좌표
            100, 100,  # SFX 이미지의 너비와 높이
            player.x, player.y,  # 몬스터 위쪽에 렌더링
            100, 100  # 출력 크기
        )

    @staticmethod
    def do(player):

        if get_time() - player.dead_time > 0.1:
            player.normal_frame = player.normal_frame + 1
            player.dead_time = get_time()

        if player.normal_frame == 5:
            player.state_machine.add_event(('TIME_OUT', 0))

        if get_time() - player.sfx_time > 0.1 and player.sfx_frame < 6:  # 마지막 프레임까지만 업데이트
            player.sfx_frame += 1
            player.sfx_time = get_time()

        if player.fly_back_distance > 0:

            fly_x = player.dir * -1 * player.fly_back_speed  # 반대 방향으로 이동
            player.x += fly_x
            player.fly_back_distance -= abs(fly_x)

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
            300,
            300)
        pass

    @staticmethod
    def do(player):
        pass
