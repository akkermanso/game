import pygame
import os
import time

pygame.init()
clock = pygame.time.Clock()
WINDOWED_WIDTH, WINDOWED_HEIGHT = 1280, 720
SCREEN_WIDTH, SCREEN_HEIGHT = WINDOWED_WIDTH, WINDOWED_HEIGHT
fullscreen = False
scene = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Mercury Exploration')
MERCURY_WORLD_WIDTH, MERCURY_WORLD_HEIGHT = 3072, 1536
camera_offset_x, camera_offset_y = 0, 0

kosmonautSprite = pygame.image.load(os.path.join('img', 'kosmonaft1.png')).convert_alpha()
KOSMONAUT_WIDTH = 165
KOSMONAUT_HEIGHT = 200
kosmonautSprite = pygame.transform.scale(kosmonautSprite, (KOSMONAUT_WIDTH, KOSMONAUT_HEIGHT))

mercGroundSprite = pygame.image.load(os.path.join('img', 'mercBack.jpg')).convert()
mercGroundSprite = pygame.transform.scale(mercGroundSprite, (MERCURY_WORLD_WIDTH, MERCURY_WORLD_HEIGHT))

try:
    mercury_notification_sprite = pygame.image.load(os.path.join('img', 'mercWid.jpg')).convert_alpha()
    MERCURY_NOTIF_WIDTH = 200
    MERCURY_NOTIF_HEIGHT = 100
    mercury_notification_sprite = pygame.transform.scale(mercury_notification_sprite, (MERCURY_NOTIF_WIDTH, MERCURY_NOTIF_HEIGHT))
    mercury_image_loaded = True
except:
    mercury_image_loaded = False

MINIMAP_SIZE = 150
MINIMAP_POS = (20, 100)  # Сдвинуто вниз, чтобы не перекрывать уведомление
minimap = pygame.Surface((MINIMAP_SIZE, MINIMAP_SIZE))
minimap.fill((0, 0, 0))

playerRect = kosmonautSprite.get_rect()
playerX, playerY = MERCURY_WORLD_WIDTH // 4, MERCURY_WORLD_HEIGHT // 4
speed = 7
moving_left = False
moving_right = False
moving_up = False
moving_down = False
facing_right = True
flipped_sprite = pygame.transform.flip(kosmonautSprite, True, False)

show_notification = True
notification_duration = 15
notification_start_time = time.time()

def draw_notification():
    notification_height = 80
    notification_surface = pygame.Surface((SCREEN_WIDTH, notification_height), pygame.SRCALPHA)
    notification_surface.fill((0, 0, 0, 180))
    if mercury_image_loaded:
        notification_surface.blit(mercury_notification_sprite, (20, 10))
    font = pygame.font.SysFont('Arial', 16)
    text_lines = [
        "Добро пожаловать на поверхность Меркурия!",
        "Исследуйте эту загадочную планету, полную тайн и открытий."
    ]
    for i, line in enumerate(text_lines):
        text_surface = font.render(line, True, (255, 255, 255))
        notification_surface.blit(text_surface, (230, 10 + i * 20))
    scene.blit(notification_surface, (0, 0))  # Уведомление в самом верху экрана

def draw_kosmonaut(x, y):
    current_sprite = kosmonautSprite if facing_right else flipped_sprite
    scene.blit(current_sprite, (x - camera_offset_x, y - camera_offset_y))
    playerRect.x = x
    playerRect.y = y

def draw_background():
    scene.blit(mercGroundSprite, (-camera_offset_x, -camera_offset_y))

def update_player_position():
    global playerX, playerY, facing_right, camera_offset_x, camera_offset_y
    newX, newY = playerX, playerY
    if moving_left:
        newX -= speed
        facing_right = False
    if moving_right:
        newX += speed
        facing_right = True
    if moving_up:
        newY -= speed
    if moving_down:
        newY += speed
    newX = max(0, min(newX, MERCURY_WORLD_WIDTH - playerRect.width))
    newY = max(0, min(newY, MERCURY_WORLD_HEIGHT - playerRect.height))
    playerX, playerY = newX, newY
    camera_offset_x = playerX - SCREEN_WIDTH // 2
    camera_offset_y = playerY - SCREEN_HEIGHT // 2
    camera_offset_x = max(0, min(camera_offset_x, MERCURY_WORLD_WIDTH - SCREEN_WIDTH))
    camera_offset_y = max(0, min(camera_offset_y, MERCURY_WORLD_HEIGHT - SCREEN_HEIGHT))

def draw_minimap():
    minimap.fill((0, 0, 0))
    pygame.draw.rect(minimap, (255, 255, 255), (0, 0, MINIMAP_SIZE-1, MINIMAP_SIZE-1), 1)
    scale_x = MINIMAP_SIZE / MERCURY_WORLD_WIDTH
    scale_y = MINIMAP_SIZE / MERCURY_WORLD_HEIGHT
    player_minimap_x = int(playerX * scale_x)
    player_minimap_y = int(playerY * scale_y)
    pygame.draw.circle(minimap, (0, 120, 255), (player_minimap_x, player_minimap_y), 5)
    scene.blit(minimap, MINIMAP_POS)

game = True
while game:
    current_time = time.time()
    if show_notification and (current_time - notification_start_time >= notification_duration):
        show_notification = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    info = pygame.display.Info()
                    SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
                else:
                    SCREEN_WIDTH, SCREEN_HEIGHT = WINDOWED_WIDTH, WINDOWED_HEIGHT
                scene = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN if fullscreen else 0)
                minimap = pygame.Surface((MINIMAP_SIZE, MINIMAP_SIZE))
                minimap.fill((0, 0, 0))
            if event.key == pygame.K_a:
                moving_left = True
            elif event.key == pygame.K_d:
                moving_right = True
            elif event.key == pygame.K_w:
                moving_up = True
            elif event.key == pygame.K_s:
                moving_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            elif event.key == pygame.K_d:
                moving_right = False
            elif event.key == pygame.K_w:
                moving_up = False
            elif event.key == pygame.K_s:
                moving_down = False
    update_player_position()
    draw_background()
    if show_notification:
        draw_notification()
    draw_kosmonaut(playerX, playerY)
    draw_minimap()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()







