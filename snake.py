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

def distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) 

def enemy_ai(snake_list, enemy, move_counter):
    if len(snake_list) > 0:
        target = snake_list[0]  # La cabeza de la serpiente es el objetivo
        
        # Solo mover al enemigo cada 2 frames para una velocidad intermedia
        if move_counter % 2 == 0:
            if enemy[0] < target[0]:
                enemy[0] = min(enemy[0] + snake_block, dis_width - snake_block)
            elif enemy[0] > target[0]:
                enemy[0] = max(enemy[0] - snake_block, 0)
            if enemy[1] < target[1]:
                enemy[1] = min(enemy[1] + snake_block, dis_height - snake_block)
            elif enemy[1] > target[1]:
                enemy[1] = max(enemy[1] - snake_block, 0)

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
    while True:
        enemy = [round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0, 
                 round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0]
        if distance([x1, y1], enemy) > 100:  # Aseguramos que el enemigo inicie lejos de la serpiente
            break

    move_counter = 0  # Contador para el movimiento del enemigo

    while not game_over:
        while game_close == True:
            dis.fill(blue)
            message("Perdiste! Presiona Q para salir o C para jugar otra vez", red)
            your_score = score_font.render("Tu Puntuación: " + str(Length_of_snake - 1), True, yellow)
            dis.blit(your_score, [dis_width / 6, dis_height / 3 + 50])  # Mostrar puntaje en la pantalla de fin de juego
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

        # Comprobar colisión con el enemigo y auto-colisión
        if snake_Head == enemy or snake_Head in snake_List[:-1]:
            game_close = True

        # Mover al enemigo
        move_counter += 1
        enemy = enemy_ai(snake_List, enemy, move_counter)

        # Dibujar juego
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        pygame.draw.rect(dis, red, [enemy[0], enemy[1], snake_block, snake_block])
        our_snake(snake_block, snake_List)

        # Mostrar el score
        score = score_font.render("Puntuación: " + str(Length_of_snake - 1), True, white)
        dis.blit(score, [0, 0])  # Aseguramos que el score se dibuje en cada frame

        pygame.display.update()

        # Colisión con comida y crecimiento de la serpiente
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()