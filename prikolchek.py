import pygame
pygame.init()
clock = pygame.time.Clock()
screenSize = (768, 512)
scene = pygame.display.set_mode(screenSize)
pygame.display.set_caption('Game')
playerSprite = pygame.image.load('img/raketa.png').convert_alpha()
groundSprite = pygame.image.load('img/backgr.jpg').convert()
groundSprite = pygame.transform.scale(groundSprite, screenSize)
playerRect = playerSprite.get_rect()
playerX, playerY = 123, 234
speed = 5
moving_left = False
moving_right = False
moving_up = False
moving_down = False

facing_right = True #true право
flipped_sprite = pygame.transform.flip(playerSprite, True, False)
def draw_player(x, y):
    if facing_right:
        current_sprite = playerSprite
    else:
        current_sprite = flipped_sprite

    scene.blit(current_sprite, (x, y))
    playerRect.x = x
    playerRect.y = y

def draw_background():
    scene.blit(groundSprite, (0, 0))

def update_player_position():
    global playerX, playerY, facing_right
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
    playerRect.width = playerSprite.get_width()
    playerRect.height = playerSprite.get_height()
    newX = max(0, min(newX, screenSize[0] - playerRect.width))
    newY = max(0, min(newY, screenSize[1] - playerRect.height))
    playerX, playerY = newX, newY

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
    pygame.display.flip()
    clock.tick(60)


pygame.quit()
