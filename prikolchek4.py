import pygame
import subprocess

pygame.init()
clock = pygame.time.Clock()
WINDOWED_WIDTH, WINDOWED_HEIGHT = 1280, 720
SCREEN_WIDTH, SCREEN_HEIGHT = WINDOWED_WIDTH, WINDOWED_HEIGHT
fullscreen = False
scene = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Game')
WORLD_WIDTH, WORLD_HEIGHT = 3072, 1536
camera_offset_x, camera_offset_y = 0, 0

playerSprite = pygame.image.load('img/raketa.png').convert_alpha()
PLAYER_WIDTH = 230
PLAYER_HEIGHT = 104
playerSprite = pygame.transform.scale(playerSprite, (PLAYER_WIDTH, PLAYER_HEIGHT))

groundSprite = pygame.image.load('img/backgrver2.jpg').convert()
groundSprite = pygame.transform.scale(groundSprite, (WORLD_WIDTH, WORLD_HEIGHT))

mercurySprite = pygame.image.load('img/merc.png').convert_alpha()
MERCURY_WIDTH = 400
MERCURY_HEIGHT = 300
mercurySprite = pygame.transform.scale(mercurySprite, (MERCURY_WIDTH, MERCURY_HEIGHT))

MINIMAP_SIZE = 150
MINIMAP_POS = (20, 20)
minimap = pygame.Surface((MINIMAP_SIZE, MINIMAP_SIZE))
minimap.fill((0, 0, 0))

mercury_positions = [(2000, 800)]
mercuryX, mercuryY = mercury_positions[0]

playerRect = playerSprite.get_rect()
playerX, playerY = WORLD_WIDTH // 4, WORLD_HEIGHT // 4
speed = 7
moving_left = False
moving_right = False
moving_up = False
moving_down = False
facing_right = True
flipped_sprite = pygame.transform.flip(playerSprite, True, False)

mercuryRect = pygame.Rect(mercuryX, mercuryY, MERCURY_WIDTH, MERCURY_HEIGHT)

def draw_player(x, y):
    if facing_right:
        current_sprite = playerSprite
    else:
        current_sprite = flipped_sprite
    scene.blit(current_sprite, (x - camera_offset_x, y - camera_offset_y))
    playerRect.x = x
    playerRect.y = y

def draw_mercury(x, y):
    scene.blit(mercurySprite, (x - camera_offset_x, y - camera_offset_y))
    mercury_center_x = x - camera_offset_x + MERCURY_WIDTH // 2
    mercury_center_y = y - camera_offset_y + MERCURY_HEIGHT // 2
    pygame.draw.circle(scene, (255, 0, 0), (mercury_center_x, mercury_center_y), 8)

def draw_background():
    scene.blit(groundSprite, (-camera_offset_x, -camera_offset_y))

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
    newX = max(0, min(newX, WORLD_WIDTH - playerRect.width))
    newY = max(0, min(newY, WORLD_HEIGHT - playerRect.height))
    playerX, playerY = newX, newY
    camera_offset_x = playerX - SCREEN_WIDTH // 2
    camera_offset_y = playerY - SCREEN_HEIGHT // 2
    camera_offset_x = max(0, min(camera_offset_x, WORLD_WIDTH - SCREEN_WIDTH))
    camera_offset_y = max(0, min(camera_offset_y, WORLD_HEIGHT - SCREEN_HEIGHT))

def check_collision():
    if playerRect.colliderect(mercuryRect):
        pygame.quit()
        subprocess.run(['python', 'main.py'])
        return True
    return False

def draw_minimap():
    minimap.fill((0, 0, 0))
    pygame.draw.rect(minimap, (255, 255, 255), (0, 0, MINIMAP_SIZE-1, MINIMAP_SIZE-1), 1)
    scale_x = MINIMAP_SIZE / WORLD_WIDTH
    scale_y = MINIMAP_SIZE / WORLD_HEIGHT
    player_minimap_x = int(playerX * scale_x)
    player_minimap_y = int(playerY * scale_y)
    pygame.draw.circle(minimap, (0, 120, 255), (player_minimap_x, player_minimap_y), 5)
    for mercury_x, mercury_y in mercury_positions:
        mercury_minimap_x = int(mercury_x * scale_x)
        mercury_minimap_y = int(mercury_y * scale_y)
        pygame.draw.circle(minimap, (255, 0, 0), (mercury_minimap_x, mercury_minimap_y), 6)
    scene.blit(minimap, MINIMAP_POS)

game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    info = pygame.display.Info()
                    SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
                    scene = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT),
                pygame.FULLSCREEN
            )
                else:
                    SCREEN_WIDTH, SCREEN_HEIGHT = WINDOWED_WIDTH, WINDOWED_HEIGHT
            scene = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
    mercuryRect.x = mercuryX
    mercuryRect.y = mercuryY

    if check_collision():
        game = False
    else:
        draw_background()
        draw_player(playerX, playerY)
        draw_mercury(mercuryX, mercuryY)
        draw_minimap()
        pygame.display.flip()
        clock.tick(60)

pygame.quit()






