import pygame
pygame.init()
clock = pygame.time.Clock()
SCREEN_WIDTH, SCREEN_HEIGHT = 768, 512
scene = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Game')
WORLD_WIDTH, WORLD_HEIGHT = 2048, 1024
camera_offset_x, camera_offset_y = 0, 0

playerSprite = pygame.image.load('img/raketa.png').convert_alpha()
groundSprite = pygame.image.load('img/backgr.jpg').convert()
groundSprite = pygame.transform.scale(groundSprite, (WORLD_WIDTH, WORLD_HEIGHT))
mercurySprite = pygame.image.load('img/mercury.jpg').convert_alpha()  # Спрайт Меркурия
MINIMAP_SIZE = 100
MINIMAP_POS = (10, 10)
minimap = pygame.Surface((MINIMAP_SIZE, MINIMAP_SIZE))
minimap.fill((0, 0, 0))
mercury_positions = [ (600, 100)]
playerRect = playerSprite.get_rect()
playerX, playerY = 100,800
speed = 5
moving_left = False
moving_right = False
moving_up = False
moving_down = False
facing_right = True  # True — направо
flipped_sprite = pygame.transform.flip(playerSprite, True, False)

def draw_player(x, y):
    if facing_right:
        current_sprite = playerSprite
    else:
        current_sprite = flipped_sprite
    scene.blit(current_sprite, (x - camera_offset_x, y - camera_offset_y))
    playerRect.x = x
    playerRect.y = y
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

def draw_minimap():
    minimap.fill((0, 0, 0))
    pygame.draw.rect(minimap, (255, 255, 255), (0, 0, MINIMAP_SIZE-1, MINIMAP_SIZE-1), 1)
    scale_x = MINIMAP_SIZE / WORLD_WIDTH
    scale_y = MINIMAP_SIZE / WORLD_HEIGHT
    player_minimap_x = int(playerX * scale_x)
    player_minimap_y = int(playerY * scale_y)
    pygame.draw.circle(minimap, (0, 120, 255), (player_minimap_x, player_minimap_y), 4)
    for mercury_x, mercury_y in mercury_positions:
        mercury_minimap_x = int(mercury_x * scale_x)
        mercury_minimap_y = int(mercury_y * scale_y)
        pygame.draw.circle(minimap, (255, 0, 0), (mercury_minimap_x, mercury_minimap_y), 3)
    scene.blit(minimap, MINIMAP_POS)
game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False

    update_player_position()
    draw_background()
    draw_player(playerX, playerY)
    draw_minimap()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()