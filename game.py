import pygame
from pygame.locals import *
import levels
pygame.init()

window = pygame.display.set_mode((1000, 700))
fps = pygame.time.Clock()

scale = 3


# convert millimetres to pixels
def convertGridToPixels(r, offset):
    return Rect(r[0]*scale - offset[0], r[1]*scale - offset[1], r[2]*scale, r[3]*scale)


# Declare colors, fonts and variables
font = pygame.font.SysFont("Arial", 24)
fontLarge = pygame.font.SysFont("Arial", 64)
BACKGROUND = (45, 31, 40)
PLAYER = (77, 44, 36)
PFTOP = (69, 21, 54)
PLATFORM = (24, 8, 19)
WALL = (24, 8, 19)
COIN = (255, 200, 9)
LAVA = (131, 40, 41)
GOAL = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (200, 200, 0)
BACKGROUND2 = (90, 69, 38)
PFTOP2 = (170, 123, 59)
PLATFORM2 = (57, 37, 10)
WALL2 = (57, 37, 10)
BACKGROUND3 = (18, 61, 93)
PFTOP3 = (7, 117, 202)
PLATFORM3 = (3, 24, 40)
WALL3 = (3, 24, 40)

player = Rect([20, 200, 10, 20])

offset = [0, 25*scale]
centering = [455, 300]
movingLeft = False
movingRight = False
horizontalSpeed = 5
verticalSpeed = 8
jumpHeight = 50
jumpFor = -1
onGround = False
coins = 0
health = 10
run1 = True
run2 = True
run3 = True
victorious = False


# starting loop
intro = True
while intro:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            intro = False
            run1 = False
            run2 = False
            run3 = False

    cur = pygame.mouse.get_pos()  # because we have a button we need to get the cursor position
    click = pygame.mouse.get_pressed()  # which button we are clicking
    window.fill(BLACK)
    welcome = fontLarge.render("Welcome!", 1, GREEN)
    objective = font.render("The objective of the game is to collect all the coins and reach the end", 1, WHITE)
    lava = font.render("Touching lava will decrease your health", 1, WHITE)
    controls = font.render("Use arrows to move and space key to jump.", 1, WHITE)
    by = font.render("Made by: Eilaf Aljundi", 1, RED)
    window.blit(welcome, (380, 200))
    window.blit(objective, (200, 300))
    window.blit(lava, (320, 350))
    window.blit(controls, (300, 400))
    window.blit(by, (760, 50))

    pygame.draw.rect(window, GREEN, (450, 500, 100, 50))

    play = font.render("Play", 1, BLACK)
    window.blit(play, (482, 508))

    # to check if cursor over button
    if 450 + 100 > cur[0] > 450 and 500 + 50 > cur[1] > 500:
        if click[0] == 1:
            intro = False

    pygame.display.update()
    fps.tick(20)


# Game loop lvl1
while run1:

    # Process events
    for event in pygame.event.get():
        if event.type == QUIT:
            run1 = False
            run2 = False
            run3 = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                run1 = False
                run2 = False
                run3 = False
            # move left
            if event.key == K_LEFT:
                movingLeft = True
                movingRight = False
            # move right
            if event.key == K_RIGHT:
                movingRight = True
                movingLeft = False
            # jump
            if event.key == K_SPACE:
                if onGround:
                    jumpFor = jumpHeight
        elif event.type == KEYUP:
            if event.key == K_LEFT:
                movingLeft = False
            if event.key == K_RIGHT:
                movingRight = False

    # Reset screen
    window.fill(BACKGROUND)

    # Calculate player position
    if movingLeft:
        player.x -= horizontalSpeed
    elif movingRight:
        player.x += horizontalSpeed
    if jumpFor >= 0:  # We're jumping
        player.y -= verticalSpeed
        jumpFor -= verticalSpeed
    elif not onGround and jumpFor < 0:
        # We're not onGround and not jumping, so we must be falling
        player.y += verticalSpeed

    # Re-center the screen around our player
    offset[0] = -centering[0] + player.x*scale
    offset[1] = -centering[1] + player.y*scale

    # Draw platforms
    for platform in levels.platforms:
        pygame.draw.rect(window, PLATFORM, convertGridToPixels(platform, offset))

    # Draw platforms tops
    for pftop in levels.pftops:
        pygame.draw.rect(window, PFTOP, convertGridToPixels(pftop, offset))

    # Draw lava
    for lava in levels.firepits:
        pygame.draw.rect(window, LAVA, convertGridToPixels(lava, offset))

    # Draw walls
    for wall in levels.walls:
        pygame.draw.rect(window, WALL, convertGridToPixels(wall, offset))

    # Draw coins
    for coin in levels.coins:
        pygame.draw.ellipse(window, COIN, convertGridToPixels(coin, offset))

    # Draw endpoint
    for endpoint in levels.goal:
        pygame.draw.ellipse(window, GOAL, convertGridToPixels(endpoint, offset))

    # Draw the player
    draw = convertGridToPixels(player, offset)
    pygame.draw.rect(window, PLAYER, draw)

    # Are we touching a platform?
    if player.collidelist(levels.platforms) > -1:
        if not onGround and jumpFor < 0:
            onGround = True
            jumpFor = -1  # If we were jumping, we just landed
    else:
        onGround = False

    # Are we touching lava?
    if player.collidelist(levels.firepits) > - 1:
        onGround = True
        health = health - 1

    # Are we touching a wall?
    if player.collidelist(levels.walls) > -1:
        if movingLeft:
            movingLeft = False
            movingRight = True
        elif movingRight:
            movingRight = False
            movingLeft = True

    # Are we touching a coin?
    coinNumber = player.collidelist(levels.coins)
    if coinNumber >= 0:
        coins = coins + 1
        del levels.coins[coinNumber]

    # We reached the goal!
    if player.collidelist(levels.goal) > -1:
        if coins == 120:
            run1 = False
        else:
            notenough = fontLarge.render("Not enough coins :(", 1, RED)
            window.blit(notenough, (300, 300))

    # We're dead, game over
    if health <= 0:
        run1 = False
        run2 = False
        run3 = False

    # Display our stats on screen
    coinsText = font.render(str(coins), 1, GREEN)
    totalcoin = font.render(" /120 Coins", 1, GREEN)
    healthText = font.render(str(health), 1, RED)
    window.blit(coinsText, (20, 20))
    window.blit(totalcoin, (50, 20))
    window.blit(healthText, (20, 50))

    # Refresh the screen
    pygame.display.update()
    fps.tick(20)


# Game loop lvl2
while run2:

    # Process events
    for event in pygame.event.get():
        if event.type == QUIT:
            run2 = False
            run3 = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                run2 = False
                run3 = False
            # move left
            if event.key == K_LEFT:
                movingLeft = True
                movingRight = False
            # move right
            if event.key == K_RIGHT:
                movingRight = True
                movingLeft = False
            # jump
            if event.key == K_SPACE:
                if onGround:
                    jumpFor = jumpHeight
        elif event.type == KEYUP:
            if event.key == K_LEFT:
                movingLeft = False
            if event.key == K_RIGHT:
                movingRight = False

    # Reset screen
    window.fill(BACKGROUND2)

    # Calculate player position
    if movingLeft:
        player.x -= horizontalSpeed
    elif movingRight:
        player.x += horizontalSpeed
    if jumpFor >= 0:  # We're jumping
        player.y -= verticalSpeed
        jumpFor -= verticalSpeed
    elif not onGround and jumpFor < 0:
        # We're not onGround and not jumping, so we must be falling
        player.y += verticalSpeed

    # Re-center the screen around our player
    offset[0] = -centering[0] + player.x*scale
    offset[1] = -centering[1] + player.y*scale

    # Draw platforms
    for platform in levels.platforms:
        pygame.draw.rect(window, PLATFORM2, convertGridToPixels(platform, offset))

    # Draw platforms tops
    for pftop in levels.pftops:
        pygame.draw.rect(window, PFTOP2, convertGridToPixels(pftop, offset))

    # Draw lava
    for lava in levels.firepits:
        pygame.draw.rect(window, LAVA, convertGridToPixels(lava, offset))

    # Draw walls
    for wall in levels.walls:
        pygame.draw.rect(window, WALL2, convertGridToPixels(wall, offset))

    # Draw coins
    for coin in levels.coins2:
        pygame.draw.ellipse(window, COIN, convertGridToPixels(coin, offset))

    # Draw endpoint
    for endpoint in levels.goal2:
        pygame.draw.ellipse(window, GOAL, convertGridToPixels(endpoint, offset))

    # Draw the player
    draw = convertGridToPixels(player, offset)
    pygame.draw.rect(window, PLAYER, draw)

    # Are we touching a platform?
    if player.collidelist(levels.platforms) > -1:
        if not onGround and jumpFor < 0:
            onGround = True
            jumpFor = -1  # If we were jumping, we just landed
    else:
        onGround = False

    # Are we touching lava?
    if player.collidelist(levels.firepits) > - 1:
        onGround = True
        health = health - 1

    # Are we touching a wall?
    if player.collidelist(levels.walls) > -1:
        if movingLeft:
            movingLeft = False
            movingRight = True
        elif movingRight:
            movingRight = False
            movingLeft = True

    # Are we touching a coin?
    coinNumber = player.collidelist(levels.coins2)
    if coinNumber >= 0:
        coins = coins + 1
        del levels.coins2[coinNumber]

    # We reached the goal!
    if player.collidelist(levels.goal2) > -1:
        if coins == 240:
            run2 = False
        else:
            notenough = fontLarge.render("Not enough coins :(", 1, RED)
            window.blit(notenough, (300, 300))

    # We're dead, game over
    if health <= 0:
        run2 = False
        run3 = False

    # Display our stats on screen
    coinsText = font.render(str(coins), 1, GREEN)
    totalcoin = font.render(" /240 Coins", 1, GREEN)
    healthText = font.render(str(health), 1, RED)
    window.blit(coinsText, (20, 20))
    window.blit(totalcoin, (50, 20))
    window.blit(healthText, (20, 50))

    # Refresh the screen
    pygame.display.update()
    fps.tick(20)


# Game loop lvl3
while run3:

    # Process events
    for event in pygame.event.get():
        if event.type == QUIT:
            run3 = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                run3 = False
            # move left
            if event.key == K_LEFT:
                movingLeft = True
                movingRight = False
            # move right
            if event.key == K_RIGHT:
                movingRight = True
                movingLeft = False
            # jump
            if event.key == K_SPACE:
                if onGround:
                    jumpFor = jumpHeight
        elif event.type == KEYUP:
            if event.key == K_LEFT:
                movingLeft = False
            if event.key == K_RIGHT:
                movingRight = False

    # Reset screen
    window.fill(BACKGROUND3)

    # Calculate player position
    if movingLeft:
        player.x -= horizontalSpeed
    elif movingRight:
        player.x += horizontalSpeed
    if jumpFor >= 0:  # We're jumping
        player.y -= verticalSpeed
        jumpFor -= verticalSpeed
    elif not onGround and jumpFor < 0:
        # We're not onGround and not jumping, so we must be falling
        player.y += verticalSpeed

    # Re-center the screen around our player
    offset[0] = -centering[0] + player.x*scale
    offset[1] = -centering[1] + player.y*scale

    # Draw platforms
    for platform in levels.platforms:
        pygame.draw.rect(window, PLATFORM3, convertGridToPixels(platform, offset))

    # Draw platforms tops
    for pftop in levels.pftops:
        pygame.draw.rect(window, PFTOP3, convertGridToPixels(pftop, offset))

    # Draw lava
    for lava in levels.firepits:
        pygame.draw.rect(window, LAVA, convertGridToPixels(lava, offset))

    # Draw walls
    for wall in levels.walls:
        pygame.draw.rect(window, WALL3, convertGridToPixels(wall, offset))

    # Draw coins
    for coin in levels.coins3:
        pygame.draw.ellipse(window, COIN, convertGridToPixels(coin, offset))

    # Draw endpoint
    for endpoint in levels.goal3:
        pygame.draw.ellipse(window, GOAL, convertGridToPixels(endpoint, offset))

    # Draw the player
    draw = convertGridToPixels(player, offset)
    pygame.draw.rect(window, PLAYER, draw)

    # Are we touching a platform?
    if player.collidelist(levels.platforms) > -1:
        if not onGround and jumpFor < 0:
            onGround = True
            jumpFor = -1  # If we were jumping, we just landed
    else:
        onGround = False

    # Are we touching lava?
    if player.collidelist(levels.firepits) > - 1:
        onGround = True
        health = health - 1

    # Are we touching a wall?
    if player.collidelist(levels.walls) > -1:
        if movingLeft:
            movingLeft = False
            movingRight = True
        elif movingRight:
            movingRight = False
            movingLeft = True

    # Are we touching a coin?
    coinNumber = player.collidelist(levels.coins3)
    if coinNumber >= 0:
        coins = coins + 1
        del levels.coins3[coinNumber]

    # We reached the goal!
    if player.collidelist(levels.goal3) > -1:
        if coins == 360:
            victorious = True
            run3 = False
        else:
            notenough = fontLarge.render("Not enough coins :(", 1, RED)
            window.blit(notenough, (300, 300))

    # We're dead, game over
    if health <= 0:
        run3 = False

    # Display our stats on screen
    coinsText = font.render(str(coins), 1, GREEN)
    totalcoin = font.render(" /360 Coins", 1, GREEN)
    healthText = font.render(str(health), 1, RED)
    window.blit(coinsText, (20, 20))
    window.blit(totalcoin, (50, 20))
    window.blit(healthText, (20, 50))

    # Refresh the screen
    pygame.display.update()
    fps.tick(20)


# End of game message
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                waiting = False
    window.fill(BLACK)
    message = fontLarge.render("Thanks for playing :D", 1, GREEN)
    if health <= 0:
        message = fontLarge.render("Sorry, you died.", 1, RED)
    elif victorious:
        message = fontLarge.render("YOU WON! CONGRATULATIONS", 1, GREEN)
    window.blit(message, (20, 220))
    message = font.render("You collected " + str(coins) + "/" + "360" + " coins", 1, WHITE)
    window.blit(message, (20, 300))
    message = font.render("Press ESC to close.", 1, WHITE)
    window.blit(message, (20, 340))
    pygame.display.update()
    fps.tick(20)

# Exit
pygame.quit()
