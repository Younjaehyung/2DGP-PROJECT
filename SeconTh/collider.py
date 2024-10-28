import pygame
import player
import monster

class Collider:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Collider, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # 초기화 코드 (필요한 경우만 실행)
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.enemies = []
            self.player = None


    # 충돌을 확인할 함수
    @staticmethod
    def check_collision(object1, object2):
        # 각 객체에 대한 마스크 생성
        mask1 = pygame.mask.from_surface(object1.colliderImage)
        mask2 = pygame.mask.from_surface(object2.colliderImage)

        # 두 객체의 위치 차이를 벡터로 계산
        offset = (object2.rect.x - object1.rect.x, object2.rect.y - object1.rect.y)

        # 마스크 충돌 검사
        if mask1.overlap(mask2, offset):
            return True
        return False



    def player_take_damage(self, damage):
        for enemy in self.enemies:
            if self.check_collision(self.player, enemy):
                self.player.take_damage(damage)


    def enemey_take_damage(self, damage):
        for enemy in self.enemies:
            if self.check_collision(self.player, enemy):
                enemy.take_damage(damage)

