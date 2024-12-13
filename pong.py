import pygame
import random

# Inicialización de Pygame
pygame.init()

# Añadimos una fuente para el mensaje de salida
exit_font = pygame.font.Font(None, 24)

# Configuración de la pantalla
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong by Patricia 💫")

# Colores
white = (255, 255, 255)
black = (0, 0, 0)

# Velocidad del juego
clock = pygame.time.Clock()
fps = 60

# Paletas y pelota
paddle_width, paddle_height = 10, 100
ball_radius = 10

# Jugador 1 y Jugador 2
paddle1 = pygame.Rect(50, height // 2 - paddle_height // 2, paddle_width, paddle_height)
paddle2 = pygame.Rect(width - 50 - paddle_width, height // 2 - paddle_height // 2, paddle_width, paddle_height)

# Pelota
ball = pygame.Rect(width // 2 - ball_radius // 2, height // 2 - ball_radius // 2, ball_radius, ball_radius)
ball_speed_x = 5 * random.choice((1, -1))
ball_speed_y = 5 * random.choice((1, -1))

# Marcadores
score1, score2 = 0, 0
font = pygame.font.Font(None, 36)

def draw():
    screen.fill(black)
    pygame.draw.rect(screen, white, paddle1)
    pygame.draw.rect(screen, white, paddle2)
    pygame.draw.ellipse(screen, white, ball)
    score_text = font.render(f"{score1} - {score2}", True, white)
    screen.blit(score_text, (width // 2 - score_text.get_width() // 2, 20))
    
    # Añadimos el mensaje de salida
    exit_text = exit_font.render("Press ESC to exit", True, white)
    screen.blit(exit_text, (10, height - 30))  # Posición en la esquina inferior izquierda
    
    pygame.display.flip()

def move_ball():
    global ball_speed_x, ball_speed_y, score1, score2
    
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Colisión con la parte superior o inferior de la pantalla
    if ball.top <= 0 or ball.bottom >= height:
        ball_speed_y *= -1
    
    # Colisión con paletas
    if ball.colliderect(paddle1) or ball.colliderect(paddle2):
        ball_speed_x *= -1

    # Puntos
    if ball.left <= 0:
        score2 += 1
        ball.center = (width // 2, height // 2)
        ball_speed_x *= random.choice((1, -1))
        ball_speed_y *= random.choice((1, -1))
    elif ball.right >= width:
        score1 += 1
        ball.center = (width // 2, height // 2)
        ball_speed_x *= random.choice((1, -1))
        ball_speed_y *= random.choice((1, -1))

def move_paddles():
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_w] and paddle1.top > 0:
        paddle1.y -= 5
    if keys[pygame.K_s] and paddle1.bottom < height:
        paddle1.y += 5
    if keys[pygame.K_UP] and paddle2.top > 0:
        paddle2.y -= 5
    if keys[pygame.K_DOWN] and paddle2.bottom < height:
        paddle2.y += 5

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Salir del juego al presionar la tecla ESC
                running = False

    move_paddles()
    move_ball()
    draw()

    clock.tick(fps)

pygame.quit()