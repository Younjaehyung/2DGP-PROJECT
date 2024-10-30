from state_machine import *


class Idle:
    @staticmethod
    def enter(player,e):

        player.handle_x = 0
        player.handle_y = 0
        player.normal_frame=0
        player.action_frame=7
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
        pass




class Attack:
    @staticmethod
    def enter(player,e):
        player.status = 2
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
        player.normal_frame = (player.normal_frame + 1) % 7
        if player.normal_frame == 0:
            player.status = 0

        player.long_press_action()

        pass




class Run:
    @staticmethod
    def enter(player,e):
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            player.handle_x = 1
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            player.handle_x = -1
        if up_down(e) or down_up(e):  # 위으로 RUN
            player.handle_y = 1
        elif down_down(e) or up_up(e):  # 아래로 RUN
            player.handle_y = -1

        player.normal_frame=0
        player.action_frame=6
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
        player.normal_frame = (player.normal_frame + 1) % 8

        player.x += (player.speed / 20) * player.handle_x
        player.y += (player.speed / 20) * player.handle_y
        pass


class Dead:
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
        player.normal_frame = (player.normal_frame + 1) % 4
        if player.normal_frame == 0:
            player.status = 0

        player.x += (player.speed / 20) * player.handle_x
        player.y += (player.speed / 20) * player.handle_y
        pass