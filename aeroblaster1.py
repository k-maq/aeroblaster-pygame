import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aeroblaster")

# Load background music
pygame.mixer.music.load("bgm.mp3")  # Replace "bgm.mp3" with the path to your background music file

# Play background music
pygame.mixer.music.play(-1)  # -1 will play the music loop indefinitely

# Load game over sound effect
game_over_sound = pygame.mixer.Sound("roblox.mp3")  # Replace "game_over.wav" with the path to your game over sound effect file

# Load images
background_img = pygame.image.load("bg3.png").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
player_img = pygame.image.load("player1.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (80, 80))
asteroid_img = pygame.image.load("asteroid1.png").convert_alpha()
asteroid_img = pygame.transform.scale(asteroid_img, (50, 50))

# Define game variables
player_size = 60
player_speed = 15
projectile_speed = 15
projectile_cooldown = 30
projectile_timer = 0
player_x, player_y = WIDTH // 2, HEIGHT // 2
asteroid_size = 50
cores = [(random.randint(WIDTH, WIDTH * 2), random.randint(0, HEIGHT - 50)) for _ in range(3)]
projectiles = []
game_over = False
game_running = False  # Add this variable to track if the game is running

# Define menu variables
menu_font = pygame.font.SysFont(None, 36)
menu_color = (255, 255, 255)
menu_text_start = menu_font.render("Start", True, menu_color)
menu_text_stop = menu_font.render("Stop", True, menu_color)
menu_rect = menu_text_start.get_rect()
menu_rect.topleft = (10, 10)

game_over_font = pygame.font.SysFont(None, 72)
game_over_color = (255, 0, 0)
game_over_text = game_over_font.render("GAME OVER", True, game_over_color)
game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Define score variables
score_font = pygame.font.SysFont(None, 36)
score_color = (255, 255, 255)
score = 0

# Main game loop
clock = pygame.time.Clock()  # Create a clock object to track time
start_time = 0  # Initialize start time
timer_update_interval = 1000  # Update the timer every 1000 milliseconds (1 second)
timer_last_update = 0  # Variable to keep track of the last timer update
while True:
    win.blit(background_img, (0, 0))  # Draw background

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if menu_rect.collidepoint(mouse_pos):
                game_running = not game_running
                if not game_running:
                    pygame.quit()
                    sys.exit()

    # Draw menu
    if game_running:
        win.blit(menu_text_stop, menu_rect)
    else:
        win.blit(menu_text_start, menu_rect)

    if not game_running:
        pygame.display.flip()
        continue

    # Start the timer when the game starts
    if start_time == 0:
        start_time = pygame.time.get_ticks()

    # Move player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - player_size:
        player_y += player_speed
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed
    if keys[pygame.K_SPACE] and projectile_timer <= 0:
        projectiles.append((player_x + player_size, player_y + player_size // 2))
        projectile_timer = projectile_cooldown

    # Loop player horizontally
    if player_x > WIDTH:
        player_x = 0
    elif player_x < 0:
        player_x = WIDTH

    # Loop projectiles horizontally
    for i in range(len(projectiles)):
        projectiles[i] = (projectiles[i][0] + projectile_speed, projectiles[i][1])
        if projectiles[i][0] > WIDTH:
            del projectiles[i]
            break

    # Loop cores horizontally
    for i in range(len(cores)):
        cores[i] = (cores[i][0] - player_speed, cores[i][1])
        if cores[i][0] < 0:
            cores[i] = (random.randint(WIDTH, WIDTH * 2), random.randint(0, HEIGHT - 50))

    # Check collision with cores
    for core in cores:
        core_rect = pygame.Rect(core[0], core[1], asteroid_size, asteroid_size)
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        if core_rect.colliderect(player_rect):
            game_over = True
            break

    if game_over:
        # Stop the timer when the game ends
        start_time = 0

        # Play game over sound effect
        game_over_sound.play()

        # Calculate score based on time elapsed
        end_time = pygame.time.get_ticks()  # Get the time when the game ends
        elapsed_seconds = (end_time - start_time) // 1000  # Convert milliseconds to seconds
        score = elapsed_seconds

        win.blit(game_over_text, game_over_rect)
        # Display score
        score_text = score_font.render("YOUR SCORE: {}".format(score), True, score_color)
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        win.blit(score_text, score_rect)

        pygame.display.flip()
        continue

    # Calculate score based on time elapsed
    current_time = pygame.time.get_ticks()  # Get the current time
    if current_time - timer_last_update >= timer_update_interval:
        elapsed_seconds = (current_time - start_time) // 1000  # Convert milliseconds to seconds
        timer_last_update = current_time  # Update the last timer update time

    # Draw player
    win.blit(player_img, (player_x, player_y))

    # Draw projectiles
    for projectile in projectiles:
        pygame.draw.circle(win, (0, 0, 255), projectile, 5)

    # Draw cores
    for core in cores:
        win.blit(asteroid_img, core)

    # Update display
    pygame.display.flip()

    # Decrease projectile cooldown timer
    if projectile_timer > 0:
        projectile_timer -= 1

    clock.tick(60)  # Cap the frame rate at 60 frames per second
