import pygame
import player
import monster


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.Rect
    left_b, bottom_b, right_b, top_b = b.Rect
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True


class CollisionManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CollisionManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # 초기화 코드 (필요한 경우만 실행)
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.collision_pairs = {}

    def add_collision_pair(self,group, a, b):
        if group not in self.collision_pairs:
            print(f'Added new group {group}')
        self.collision_pairs[group] = [[], []]
        if a:
            self.collision_pairs[group][0].append(a)
        if b:
            self.collision_pairs[group][1].append(b)

    def remove_collision_object(self,o):
        for pairs in self.collision_pairs.values():
            if o in pairs[0]:
                pairs[0].remove(o)
            if o in pairs[1]:
                pairs[1].remove(o)



    def handle_collisions(self):
        for group, pairs in self.collision_pairs.items():
            for a in pairs[0]:
                for b in pairs[1]:
                    if collide(a, b):
                        a.handle_collision(group, b)
                        b.handle_collision(group, a)

