import pygame
import random
import time
import datetime

# Initialize pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load the new font
font_size = 20  # Choose an appropriate font size
font_path = r"C:\Users\husse\Downloads\Space Invaders Prototype\Space Invaders\Font\Space.ttf"
new_font = pygame.font.Font(font_path, font_size)

heart_image = pygame.image.load("Images/Heart.png")  # Adjust the path as needed
heart_width, heart_height = 27, 17  # Adjust the size as needed
heart_image = pygame.transform.scale(heart_image, (heart_width, heart_height))

# Load the bullet images
bullet_width = 8
bullet_height = 16  # Decreased bullet size
bullet_images = {
    "RedBullet": pygame.transform.scale(pygame.image.load("Images/RedBullet.png"), (bullet_width, bullet_height)),
    "BlueBullet": pygame.transform.scale(pygame.image.load("Images/BlueBullet.png"), (bullet_width, bullet_height)),
    "PurpleBullet": pygame.transform.scale(pygame.image.load("Images/PurpleBullet.png"), (bullet_width, bullet_height)),
    "GreenBullet": pygame.transform.scale(pygame.image.load("Images/GreenBullet.png"), (bullet_width, bullet_height)),
    "YellowBullet": pygame.transform.scale(pygame.image.load("Images/YellowBullet.png"), (bullet_width, bullet_height)),
}

# Load the spaceship image
spaceship_width, spaceship_height = 80, 80
spaceship_image = pygame.image.load("Images/SpaceShip.png")
spaceship_image = pygame.transform.scale(spaceship_image, (spaceship_width, spaceship_height))

# Load the space invader image
invader_width, invader_height = 44, 33
invader_image = pygame.image.load("Images/SpaceInvader.png")
invader_image = pygame.transform.scale(invader_image, (invader_width, invader_height))

# Set up the player
player_width, player_height = 80, 80
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 6  # Slower player speed
player = pygame.Rect(player_x, player_y, player_width, player_height)

# Set up the enemies
enemy_speed = 1  # Slower enemy speed
enemy_drop = 10
enemies = []
for row in range(5):
    for col in range(10):
        enemy_x = 100 + col * (invader_width + 10)
        enemy_y = 100 + row * (invader_height + 10)

        if row == 1 and col == 0:
            enemy_x -= 1

        enemy = pygame.Rect(enemy_x, enemy_y, invader_width, invader_height)
        enemies.append(enemy)

# Set up the bullets
player_bullet_speed = 11 # Slower player bullet speed
enemy_bullet_speed = 6
player_bullet_cooldown = 500
last_player_bullet_time = 0
enemy_bullet_cooldown = 1800
last_enemy_bullet_time = 0

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.color = color
        self.image = bullet_images[self.color]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)

    def update(self):
        # Move the bullet upward for player bullets
        if self.color in ("RedBullet", "BlueBullet", "PurpleBullet", "GreenBullet", "YellowBullet"):
            self.rect.y -= player_bullet_speed
        # Move the bullet downward for enemy bullets
        else:
            self.rect.y += enemy_bullet_speed

player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

# Set up the score, lives, and time
score = 0
lives = 3
font = pygame.font.Font(None, 36)

# Set up game states
is_player_hit = False
player_respawn_time = 2000
last_player_hit_time = 0
enemy_reset_time = 2000
last_enemy_hit_time = 0

def draw_text(text, font, color, x, y, align="left"):
    text_surface = new_font.render(text, True, color)  # Use the new_font
    text_rect = text_surface.get_rect()

    if align == "left":
        text_rect.topleft = (x, y)
    elif align == "center":
        text_rect.center = (x, y)
    elif align == "right":
        text_rect.topright = (x, y)

    win.blit(text_surface, text_rect)

def reset_game():
    global player, player_speed, player_bullets, is_player_hit, last_player_hit_time, last_player_bullet_time
    global enemies, enemy_speed, enemy_bullets, last_enemy_bullet_time, last_enemy_hit_time

    player_speed = 0
    player.x = player_x
    player.y = player_y
    player_bullets = pygame.sprite.Group()
    is_player_hit = False
    last_player_hit_time = 0
    last_player_bullet_time = 0

    enemies = []
    for row in range(5):
        for col in range(10):
            enemy_x = 100 + col * (invader_width + 10)
            enemy_y = 100 + row * (invader_height + 10)

            if row == 1 and col == 0:
                enemy_x -= 1

            enemy = pygame.Rect(enemy_x, enemy_y, invader_width, invader_height)
            enemies.append(enemy)

    enemy_speed = 1
    enemy_bullets = pygame.sprite.Group()
    last_enemy_bullet_time = 0
    last_enemy_hit_time = 0

def show_game_over():
    win.fill((0, 0, 0))
    draw_text("GAME OVER", font, (255, 255, 255), WIDTH // 2, HEIGHT // 2, align="center")
    pygame.display.update()
    time.sleep(2)
    reset_game()

def draw_timer():
    current_time = datetime.datetime.now()
    time_elapsed = current_time - start_time
    time_text = f"Time {time_elapsed.seconds}"
    # Update the X and Y positions to change the time counter's position
    x_pos = 355
    y_pos = 11
    draw_text(time_text, font, (255, 255, 255), x_pos, y_pos, align="left")

# Load and display the background image
background_image = pygame.image.load("Images/Background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Set the size and position of the hearts
heart_spacing = 3  # Adjust the spacing between hearts
heart_start_x = 707
heart_y = 10  # Y position

# Define the reset_game_positions function
def reset_game_positions():
    player.x = player_x
    player.y = player_y
    for row in range(5):
        for col in range(10):
            enemy_x = 100 + col * (invader_width + 10)
            enemy_y = 100 + row * (invader_height + 10)
            
            if row == 1 and col == 0:
                enemy_x -= 1

            enemies[row * 10 + col].x = enemy_x
            enemies[row * 10 + col].y = enemy_y

# Game loop
running = True
clock = pygame.time.Clock()
start_time = datetime.datetime.now()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen with the background image
    win.blit(background_image, (0, 0))

    # Draw the score, lives, and time using the updated draw_text function
    draw_text(f"Score {score}", new_font, (255, 255, 255), WIDTH // 2 - 200, 20, align="center")  # Offset to the left
    draw_text("Lives", new_font, (255, 255, 255), WIDTH // 2 + 200, 20, align="center")  # Offset to the right
    draw_timer()

    # Draw the hearts for lives
    for i in range(lives):
        heart_x = heart_start_x - i * (heart_width + heart_spacing)
        win.blit(heart_image, (heart_x, heart_y))

    # Player shooting
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
        current_time = pygame.time.get_ticks()
        if current_time - last_player_bullet_time > player_bullet_cooldown:
            bullet_x = player.x + player_width // 2 - bullet_width // 2
            bullet_y = player.y

            # Replace the bullet color with the corresponding color for each bullet type
            bullet_color_name = random.choice(list(bullet_images.keys()))

            bullet = Bullet(bullet_x, bullet_y, bullet_color_name)
            player_bullets.add(bullet)
            last_player_bullet_time = current_time

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x -= player_speed
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x += player_speed

    # Ensure the player stays within the screen boundaries
    if player.left < 0:
        player.left = 0
    elif player.right > WIDTH:
        player.right = WIDTH

    # Move the enemies
    for enemy in enemies:
        enemy.x += enemy_speed

        # Reverse the enemy's direction and move down when hitting the edges
        if enemy.x <= 0 or enemy.x >= WIDTH - invader_width:
            enemy_speed *= -1
            for e in enemies:
                e.y += enemy_drop

    # Draw the player bullets using the sprite group
    player_bullets.draw(win)

    # Draw the enemy bullets using the sprite group
    enemy_bullets.draw(win)

    # Enemy shooting (inside the "Move the enemies" loop)
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_bullet_time > enemy_bullet_cooldown:
        enemy_shooting = random.choice(enemies)  # Choose a random enemy to shoot
        bullet_x = enemy_shooting.x + invader_width // 2 - bullet_width // 2
        bullet_y = enemy_shooting.y + invader_height

        # Randomly select a bullet color name
        bullet_color_name = random.choice(list(bullet_images.keys()))

        # Use the color name as the key to create the enemy bullet
        enemy_bullet = Bullet(bullet_x, bullet_y, bullet_color_name)
        enemy_bullets.add(enemy_bullet)
        last_enemy_bullet_time = current_time

    # Check for collision with player
    if is_player_hit:
        current_time = pygame.time.get_ticks()
        if current_time - last_player_hit_time > player_respawn_time:
            is_player_hit = False

    # Check for collision with player bullets
    for bullet in player_bullets:
        for enemy in enemies:
            if enemy.colliderect(bullet):
                player_bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1

    # Check for collision with enemy bullets
    for bullet in enemy_bullets:
        if bullet.rect.colliderect(player):
            if not is_player_hit:
                is_player_hit = True
                last_player_hit_time = pygame.time.get_ticks()
                lives -= 1
                enemy_bullets.remove(bullet)

    # Move the player bullets
    for bullet in player_bullets:
        bullet.rect.y -= player_bullet_speed
        if bullet.rect.y < 0:
            player_bullets.remove(bullet)

    # Move the enemy bullets and check for collision
    for bullet in enemy_bullets:
        bullet.rect.y += enemy_bullet_speed
        if bullet.rect.y > HEIGHT:
            enemy_bullets.remove(bullet)

    # Check if the player has lost all lives
    if lives <= 0:
        show_game_over()

    # Check if all enemies are defeated
    if len(enemies) == 0:
        reset_game()

    # Draw the player
    win.blit(spaceship_image, (player.x, player.y))

    # Draw the enemies
    for enemy in enemies:
        win.blit(invader_image, (enemy.x, enemy.y))

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
