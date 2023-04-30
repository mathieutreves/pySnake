import random

import pygame
import pygame_menu

grey = (40, 40, 40)
black = (0,0,0)
green = (0,140,0)
red = (140,0,0)
yellow = (255, 255, 102)

pygame.init()

screenWidth = 800
screenHeigth = 600
screen = pygame.display.set_mode([screenWidth, screenHeigth])

clock = pygame.time.Clock()
font_style = pygame.font.SysFont(pygame.font.get_default_font(), 25)
score_font = pygame.font.SysFont(pygame.font.get_default_font(), 35)
pygame.display.set_caption("Snakez")

screen.fill(black)

centerX = screenWidth / 2
centerY = screenHeigth / 2

snakePieceDim = 20

foodX = 0
foodY = 0

magicX = 0
magicY = 0

def displayScore(score):
    value = score_font.render("Score: " + str(score), True, yellow)
    screen.blit(value, [0, 0])
    
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [centerX - mesg.get_width()/2, centerY - mesg.get_height()/2])

def updateSnake(snake):
    for segment in snake:
        pygame.draw.rect(screen, green, [segment[0], segment[1], snakePieceDim, snakePieceDim])

def updateFood():
    global foodX
    global foodY

    foodX = random.randrange(0, screenWidth - snakePieceDim, snakePieceDim)
    foodY = random.randrange(0, screenHeigth - snakePieceDim, snakePieceDim)

def updateMagic():
    global magicX
    global magicY

    magicX = random.randrange(0, screenWidth - snakePieceDim, snakePieceDim)
    magicY = random.randrange(0, screenHeigth - snakePieceDim, snakePieceDim)

def gameLoop(withoutBorders):

    # Snake init
    updateX = 0
    updateY = 0

    snakeXpos = centerX
    snakeYpos = centerY
    
    snake = []
    snakeLen = 1

    # Food init
    updateFood()
    updateMagic()
    
    lastKey = 0
    fps = 10
    score = 0
    magicTime = 0
    magicDrawTime = random.randint(5, 20) * fps
    magicDraw = False

    gameOver = False
    gameClose = False
    while not gameOver:
        if gameClose:
            screen.fill(grey)
            displayScore(score)
            pygame.display.update()
            lostMenu.mainloop(screen)

        # Check events
        for event in pygame.event.get():
            # Check if we want to quit the game
            if event.type == pygame.QUIT:
                gameOver = True

            # Check if the user press a key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not(lastKey == pygame.K_DOWN):
                    lastKey = event.key
                    updateX = 0
                    updateY = - snakePieceDim
                elif event.key == pygame.K_DOWN and not(lastKey == pygame.K_UP):
                    lastKey = event.key
                    updateX = 0
                    updateY = snakePieceDim
                elif event.key == pygame.K_RIGHT and not(lastKey == pygame.K_LEFT):
                    lastKey = event.key
                    updateX = snakePieceDim
                    updateY = 0
                elif event.key == pygame.K_LEFT and not(lastKey == pygame.K_RIGHT):
                    lastKey = event.key
                    updateX = - snakePieceDim
                    updateY = 0

        # Update snake position on the screen
        snakeXpos += updateX
        snakeYpos += updateY

        # Boundaries teleport the snake to the other side
        if withoutBorders:
            if snakeXpos < 0: snakeXpos = screenWidth - snakePieceDim
            elif snakeXpos > screenWidth: snakeXpos = 0
            
            if snakeYpos < 0: snakeYpos = screenHeigth - snakePieceDim
            elif snakeYpos > screenHeigth: snakeYpos = 0
        else:
            if snakeXpos < 0 or snakeXpos > screenWidth or snakeYpos < 0 or snakeYpos > screenHeigth:
                gameClose = True

        # Redraw
        screen.fill(grey)

        # Update position and draw food
        if snakeXpos == foodX and snakeYpos == foodY:
            updateFood()
            snakeLen += 1
            score += 1
            # increment fps
            if snakeLen < 50 and snakeLen % 5 == 0:
                fps += 1
        pygame.draw.rect(screen, red, [foodX, foodY, snakePieceDim, snakePieceDim])

        if snakeXpos == magicX and snakeYpos == magicY:
            updateMagic()
            snakeLen += 1
            score += 10
            magicTime = 0
            magicDraw = False
        else:
            magicTime += 1

        if magicTime > magicDrawTime:
            magicDraw = True
        
        if magicTime > magicDrawTime + (5 * fps):
            magicDrawTime = random.randint(5, 20) * fps
            magicTime = 0
            magicDraw = False

        if magicDraw:
            pygame.draw.rect(screen, yellow, [magicX, magicY, snakePieceDim, snakePieceDim])

        # Add new head to snake, with updated position
        snakeHead = []
        snakeHead.append(snakeXpos)
        snakeHead.append(snakeYpos)
        snake.append(snakeHead)

        # Snake can be only of max lengh
        if len(snake) > snakeLen:
            del snake[0]

        # Check if gameOver
        for x in snake[:-1]:
            if x == snakeHead:
                gameClose = True

        # Draw snake
        updateSnake(snake)

        # Draw score
        displayScore(score)
        
        # Update screen
        pygame.display.update()

        # Click at incremental fps
        clock.tick(fps)
            
    pygame.quit()

menu = pygame_menu.Menu("Welcome", 400, 300, theme=pygame_menu.themes.THEME_DARK)
menu.add.button("Play", gameLoop, False)
menu.add.button("Without Borders", gameLoop, True)
menu.add.button("Quit", pygame_menu.events.EXIT)

lostMenu = pygame_menu.Menu("You lost", 400, 300, theme=pygame_menu.themes.THEME_DARK)
lostMenu.add.button("Play", gameLoop, False)
lostMenu.add.button("Without Borders", gameLoop, True)
lostMenu.add.button("Quit", pygame_menu.events.EXIT)

menu.mainloop(screen)