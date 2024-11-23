from pico2d import load_image, get_time

from state_machine import *


class Idle:

    @staticmethod
    def enter(player,e):
        print('idle')

        if z_down(e):
            player.attack_status = 1
            player.action_frame = 5

        else:
            player.attack_status = 0
            player.action_frame=7


        player.handle_x = 0
        player.handle_y = 0
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

        player.normal_frame = (player.normal_frame + 1) % 6
        if player.action_frame== 5 and player.normal_frame == 0:
            player.state_machine.add_event(('TIME_OUT', 0))
            return

        pass



class Run:
    @staticmethod
    def enter(player,e):

        if z_down(e):
            player.attack_status = 1
            player.action_frame=3

        else:
            player.attack_status = 0
            player.action_frame = 6



        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            player.handle_x += 1
            if right_down(e):
                print("right_down")
            else : print ("left_up")

        if left_down(e) or right_up(e) :  # 왼쪽으로 RUN
            player.handle_x -= 1
            if left_down(e):
                print("left_down")
            else:
                print("right_up")

        if up_down(e) or down_up(e):  # 위으로 RUN
            player.handle_y += 1
            if up_down(e):
                print("up_down")
            else:
                print("down_up")

        if down_down(e) or up_up(e):  # 아래로 RUN
            player.handle_y -= 1
            if down_down(e):
                print("down_down")
            else : print ("up_up")

        if down_down(e):
            player.keydown[3] = 1
        elif down_up(e):
            player.keydown[3] = 0

        if right_down(e):
            player.keydown[2] = 1
        elif right_up(e):
            player.keydown[2] = 0

        if up_down(e):
            player.keydown[1] = 1
        elif up_up(e):
            player.keydown[1] = 0

        if left_down(e):
            player.keydown[0] = 1
        elif left_up(e):
            player.keydown[0] = 0

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
        speed=1



        if player.action_frame == 3:
            player.normal_frame = (player.normal_frame + 1) % 8
            if player.job ==3:
                speed = 3
            if player.normal_frame == 0:
                player.state_machine.add_event(('TIME_OUT', 0))
                return
        else :
            player.normal_frame = (player.normal_frame + 1) % 8
        player2_x = player.x
        player2_y = player.y
        player2_x += (player.speed/5) * (get_time()-player.run_time) * player.handle_x*speed
        player2_y += (player.speed/5) * (get_time()-player.run_time) * player.handle_y*speed

        if player2_x >800 or player2_x <0:
            pass
        else:

            player.x += (player.speed) * (get_time()-player.run_time) * player.handle_x*speed
            player.y += (player.speed) * (get_time()-player.run_time) * player.handle_y*speed

        player.run_time = get_time()

        if not player.keydown[0] and not player.keydown[1] and not player.keydown[2] and not player.keydown[3]  :
            player.state_machine.add_event(('Idle', 0))


        pass


class Hit:

    @staticmethod
    def enter(player, e):
        player.normal_frame = 0

        player.action_frame = 2

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


        if player.normal_frame ==0:
            player.state_machine.add_event(('TIME_OUT', 0))

        pass


class Spawn:

    @staticmethod
    def enter(player, e):
        player.normal_frame = 0
        player.shnormal_frame = 0
        player.lsnormal_frame = 0
        player.action_frame = player.image_action[player.job]
        player.spawn_time = get_time()
        pass

    @staticmethod
    def exit(player, e):

        pass

    @staticmethod
    def draw(player):
        player.laser_image.clip_composite_draw(
            player.shnormal_frame * 100,  # 이미지의 왼쪽 상단 x좌표
            0,  # 이미지의 왼쪽 상단 y좌표
            100,
            100,
            player.flip_y,
            player.flip_x,
            player.x,
            player.y,
            500,
            500)

        player.image.clip_draw(
            player.normal_frame * 100,  # 이미지의 왼쪽 상단 x좌표
            player.action_frame * 100,  # 이미지의 왼쪽 상단 y좌표
            100,
            100,
            player.x,
            player.y,
            250,
            250)

        player.heal_image.clip_draw(
            player.lsnormal_frame,  # 이미지의 왼쪽 상단 x좌표
            0,  # 이미지의 왼쪽 상단 y좌표
            100,
            100,
            player.x,
            player.y,
            500,
            500)


        pass

    @staticmethod
    def do(player):
        player.normal_frame = (player.normal_frame + 1) % 6
        player.lhnormal_frame = (player.lhnormal_frame + 1) % 4
        player.shnormal_frame = (player.shnormal_frame + 1) % 4

        if get_time() - player.spawn_time > 1:
            player.state_machine.add_event(('TIME_OUT', 0))

        pass

class Dead:
    @staticmethod
    def enter(player, e):
        player.normal_frame = 0
        player.action_frame = 1
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