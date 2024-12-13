import pygame
import time
import random

pygame.init()

# Colores
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Dimensiones de la pantalla
dis_width = 800
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by Patricia 💫')

clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def enemy_ai(snake_list, enemy):
    if len(snake_list) > 0:
        target = snake_list[0]  # La cabeza de la serpiente es el objetivo
        if enemy[0] < target[0]:
            enemy[0] += snake_block
        elif enemy[0] > target[0]:
            enemy[0] -= snake_block
        if enemy[1] < target[1]:
            enemy[1] += snake_block
        elif enemy[1] > target[1]:
            enemy[1] -= snake_block
        
        # Asegurarse de que el enemigo no salga de la pantalla
        enemy[0] = max(0, min(enemy[0], dis_width - snake_block))
        enemy[1] = max(0, min(enemy[1], dis_height - snake_block))

    return enemy

def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    # Inicialización del enemigo
    enemy = [random.randrange(0, dis_width - snake_block), random.randrange(0, dis_height - snake_block)]

    while not game_over:
        while game_close == True:
            dis.fill(blue)
            message("Perdiste! Presiona Q-Quit o C-Play Again", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # Actualizar posición de la serpiente
        x1 += x1_change
        y1 += y1_change

        # Comprobar colisión con los bordes
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        # Actualizar lista de la serpiente
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Comprobar auto-colisión y colisión con el enemigo
        for segment in snake_List[:-1]:
            if segment == snake_Head or segment == enemy:
                game_close = True
                break

        # Mover al enemigo
        enemy = enemy_ai(snake_List, enemy)

        # Dibujar juego
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        pygame.draw.rect(dis, red, [enemy[0], enemy[1], snake_block, snake_block])
        our_snake(snake_block, snake_List)

        pygame.display.update()

        # Colisión con comida y crecimiento de la serpiente
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        # Actualización de la puntuación y otros gráficos
        score = score_font.render("Score: " + str(Length_of_snake - 1), True, white)
        dis.blit(score, [0, 0])

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()