import pygame

# Pygame 초기화
pygame.init()
screen = pygame.display.set_mode((800, 600))

# 이미지 로드 및 설정
sprite1_img = pygame.image.load('resource/Werewolf/Werewolf with shadows/Werewolf.png').convert_alpha()
sprite2_img = pygame.image.load('resource/Werewolf/Werewolf with shadows/Werewolf.png').convert_alpha()

# 이미지 위치
sprite1_pos = pygame.Vector2(100, 100)
sprite2_pos = pygame.Vector2(200, 150)

# Mask 객체 생성
sprite1_mask = pygame.mask.from_surface(sprite1_img)
sprite2_mask = pygame.mask.from_surface(sprite2_img)

# 충돌 감지 함수
def check_collision(pos1, pos2):
    offset_x = int(pos2.x - pos1.x)
    offset_y = int(pos2.y - pos1.y)
    overlap = sprite1_mask.overlap(sprite2_mask, (offset_x, offset_y))
    return overlap

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 예시: sprite2를 마우스 위치로 이동
    sprite2_pos = pygame.Vector2(pygame.mouse.get_pos())

    # 충돌 체크
    if check_collision(sprite1_pos, sprite2_pos):
        print("Collision Detected!")

    # 화면 갱신
    screen.fill((255, 255, 255))
    screen.blit(sprite1_img, sprite1_pos)
    screen.blit(sprite2_img, sprite2_pos)
    pygame.display.flip()

# Pygame 종료
pygame.quit()
