import pygame
import random
import heapq

pygame.init()

# Configuración de la pantalla
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Laberinto por Patricia 💫")

# Colores
black, white, red, green, blue = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)

# Dimensiones del laberinto
cell_size = 30
cols, rows = width // cell_size, height // cell_size

# Inicializar laberinto
grid = [[0 for _ in range(cols)] for _ in range(rows)]

# Generar laberinto usando Prim's algorithm
def generate_maze():
    walls = []
    start_x, start_y = random.randint(0, cols-1), random.randint(0, rows-1)
    grid[start_y][start_x] = 1  # 1 representa un camino
    for y in (start_y-1, start_y+1):
        if 0 <= y < rows:
            walls.append((start_x, y))
    for x in (start_x-1, start_x+1):
        if 0 <= x < cols:
            walls.append((x, start_y))
    
    while walls:
        wall = random.choice(walls)
        walls.remove(wall)
        x, y = wall
        neighbors = 0
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows:
                if grid[ny][nx] == 1:
                    neighbors += 1
        if neighbors == 1:
            grid[y][x] = 1
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] == 0:
                    walls.append((nx, ny))

generate_maze()

# Jugador
player = pygame.Rect(cell_size, cell_size, cell_size, cell_size)

# Meta
goal_x, goal_y = random.randint(0, cols-1), random.randint(0, rows-1)
while grid[goal_y][goal_x] != 1:
    goal_x, goal_y = random.randint(0, cols-1), random.randint(0, rows-1)

# Enemigos
enemies = []
num_enemies = 5
enemy_move_interval = 30  # Enemigos se mueven cada 30 frames
enemy_move_counter = 0
for _ in range(num_enemies):
    enemy_x, enemy_y = random.randint(0, cols-1), random.randint(0, rows-1)
    while grid[enemy_y][enemy_x] != 1 or (enemy_x, enemy_y) == (goal_x, goal_y):
        enemy_x, enemy_y = random.randint(0, cols-1), random.randint(0, rows-1)
    enemies.append(pygame.Rect(enemy_x * cell_size, enemy_y * cell_size, cell_size, cell_size))

# Movimiento de enemigos
def move_enemy(enemy):
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    random.shuffle(directions)
    for dx, dy in directions:
        new_x, new_y = (enemy.x + dx * cell_size) // cell_size, (enemy.y + dy * cell_size) // cell_size
        if 0 <= new_x < cols and 0 <= new_y < rows and grid[new_y][new_x] == 1:
            enemy.x = new_x * cell_size
            enemy.y = new_y * cell_size
            break

# Bucle principal del juego
running = True
win = False
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    new_x, new_y = player.x, player.y
    if keys[pygame.K_LEFT] and player.left > 0:   new_x = player.left - cell_size
    elif keys[pygame.K_RIGHT] and player.right < width: new_x = player.right
    elif keys[pygame.K_UP] and player.top > 0:   new_y = player.top - cell_size
    elif keys[pygame.K_DOWN] and player.bottom < height: new_y = player.bottom

    new_cell_x, new_cell_y = new_x // cell_size, new_y // cell_size
    if 0 <= new_cell_x < cols and 0 <= new_cell_y < rows and grid[new_cell_y][new_cell_x] == 1:
        player.x, player.y = new_cell_x * cell_size, new_cell_y * cell_size

    # Mover enemigos
    enemy_move_counter += 1
    if enemy_move_counter >= enemy_move_interval:
        for enemy in enemies:
            move_enemy(enemy)
        enemy_move_counter = 0

    # Colisiones
    if player.colliderect(pygame.Rect(goal_x * cell_size, goal_y * cell_size, cell_size, cell_size)):
        win = True
        running = False
    for enemy in enemies:
        if player.colliderect(enemy):
            running = False

    # Dibujar el laberinto, el jugador, la meta y enemigos
    screen.fill(black)
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == 0:
                pygame.draw.rect(screen, white, (x * cell_size, y * cell_size, cell_size, cell_size))
            else:
                pygame.draw.rect(screen, black, (x * cell_size, y * cell_size, cell_size, cell_size), 1)  # Borde para caminos
    pygame.draw.rect(screen, red, player)
    pygame.draw.rect(screen, green, pygame.Rect(goal_x * cell_size, goal_y * cell_size, cell_size, cell_size))
    for enemy in enemies:
        pygame.draw.rect(screen, blue, enemy)
    pygame.display.flip()

    clock.tick(30)  # Limitar a 30 FPS para controlar la velocidad del juego

if win:
    print("¡Has ganado!")
else:
    print("¡Perdiste!")

pygame.quit()