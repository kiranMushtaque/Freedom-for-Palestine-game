import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game window setup
WIDTH, HEIGHT = 480, 640
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Freedom Shooter Game")

# Load and scale images
try:
    man_img = pygame.image.load("images/woman-7080689_1280.jpg")
    flag_img = pygame.image.load("images/flag.png")
    fire_img = pygame.image.load("images/preview_fire.gif")
    palestine_flag_img = pygame.image.load("images/palestine_flag.png")  # Palestine flag image
except:
    print("⚠️ Image file not found! Check the path or filename.")
    pygame.quit()
    sys.exit()

# Resize images
man_img = pygame.transform.scale(man_img, (60, 80))
flag_img = pygame.transform.scale(flag_img, (50, 60))
fire_img = pygame.transform.scale(fire_img, (10, 20))
palestine_flag_img = pygame.transform.scale(palestine_flag_img, (300, 200))

# Player settings
man_x = WIDTH // 2 - 30
man_y = HEIGHT - 90
man_speed = 5

# Lists for bullets and enemies
fires = []
enemies = []

# Score system
score = 0
font = pygame.font.SysFont(None, 36)

# Clock
clock = pygame.time.Clock()

# Enemy spawn timer
SPAWNENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNENEMY, 1000)  # every second

# Winning condition
WIN_SCORE = 10  # The score required to win

# Game loop
running = True
last_fire_time = 0
fire_delay = 300  # milliseconds between shots

while running:
    clock.tick(60)
    win.fill((30, 30, 30))  # Dark background

    # Check if the player has won
    if score >= WIN_SCORE:
        # Display the Palestine flag on the screen
        win.fill((30, 30, 30))  # Clear the screen
        win.blit(palestine_flag_img, (WIDTH // 2 - 150, HEIGHT // 2 - 100))  
        win_text = font.render("You Win!", True, (255, 255, 255))  # Winning text
        win.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 + 120))  # Center the text
        pygame.display.update()
        pygame.time.wait(3000)  # Wait for 3 seconds before closing the game
        break

    # Draw player
    win.blit(man_img, (man_x, man_y))

    # Draw fire
    for fx, fy in fires:
        win.blit(fire_img, (fx, fy))

    # Draw enemies
    for ex, ey in enemies:
        win.blit(flag_img, (ex, ey))

    # Draw score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    win.blit(score_text, (10, 10))
    pygame.display.update()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SPAWNENEMY:
            ex = random.randint(0, WIDTH - 50)
            enemies.append([ex, -60])

    # Key presses
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()

    # Player movement
    if keys[pygame.K_LEFT] and man_x > 0:
        man_x -= man_speed
    if keys[pygame.K_RIGHT] and man_x < WIDTH - 60:
        man_x += man_speed

  
    if keys[pygame.K_SPACE] and current_time - last_fire_time > fire_delay:
        if len(fires) < 5:
            fires.append([man_x + 25, man_y])
            last_fire_time = current_time

    # Move fires
    for fire in fires[:]:
        fire[1] -= 10
        if fire[1] < 0:
            fires.remove(fire)

    # Move enemies
    for enemy in enemies[:]:
        enemy[1] += 2
        if enemy[1] > HEIGHT:
            enemies.remove(enemy)

    # Collision detection for fire and enemy
    for fire in fires[:]:
        for enemy in enemies[:]:
            fire_rect = pygame.Rect(fire[0], fire[1], 10, 20)
            enemy_rect = pygame.Rect(enemy[0], enemy[1], 50, 60)
            if fire_rect.colliderect(enemy_rect):
                fires.remove(fire)
                enemies.remove(enemy)
                score += 1
                break

pygame.quit()
sys.exit()
