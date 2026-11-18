# AVALANCHE SURVIVOR
import pygame
import random
import os
pygame.init()

# Create the game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Avalanche Survivor")

# Player starting position
player_x = 375
player_y = 525

# Player movement speed
player_speed = 5

# Snowball settings
snowballs = [
    {"x": random.randint(20, 780), "y": -50},
    {"x": random.randint(20, 780), "y": -250},
    {"x": random.randint(20, 780), "y": -450}
]

snowball_radius = 20
base_snowball_speed = 4
snowball_speed = base_snowball_speed
current_snowball_speed = snowball_speed

# Power-up settings
powerup_types = ["time_slow", "body_heat"]

powerup_active = False
powerup_type = None

powerup_x = 0
powerup_y = -30
powerup_speed = 3
powerup_radius = 12

next_powerup_time = 10000
# Create 75 decorative snowflakes
snowflakes = []

for i in range(75):
    snowflake = {
        "x": random.randint(0, 800),
        "y": random.randint(0, 600),
        "speed": random.randint(1, 3),
        "size": random.randint(1, 3)
    }

    snowflakes.append(snowflake)

# Control how fast the game runs
clock = pygame.time.Clock()
# Score settings
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 72)
game_over_font = pygame.font.Font(None, 72)
start_time = pygame.time.get_ticks()
survival_time = 0

# High score settings
# Each Windows user gets their own save folder
save_folder = os.path.join(
    os.environ.get(
        "LOCALAPPDATA",
        os.path.expanduser("~")
    ),
    "AvalancheSurvivor"
)

# Create the folder if it doesn't exist
os.makedirs(save_folder, exist_ok=True)

high_score_file = os.path.join(
    save_folder,
    "highscore.txt"
)

high_score = 0

# Load the previous high score
if os.path.exists(high_score_file):
    with open(high_score_file, "r") as file:
        saved_score = file.read().strip()

        if saved_score.isdigit():
            high_score = int(saved_score)

running = True
game_over = False
game_started = False
active_ability = None
powerup_duration = 12000
powerup_warning_time = 5000
ability_end_time = 0
body_heat_radius = 70

while running:

    # Check if the player closes the window
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not game_started and event.key == pygame.K_SPACE:
                game_started = True
                start_time = pygame.time.get_ticks()
            # Press R to restart after losing
            if game_over and event.key == pygame.K_r:
                game_over = False
                player_x = 375
                player_y = 525
                start_time = pygame.time.get_ticks()
                survival_time = 0
                snowball_speed = base_snowball_speed
                current_snowball_speed = snowball_speed
                snowballs = [
                    {"x": random.randint(20, 780), "y": -50},
                    {"x": random.randint(20, 780), "y": -250},
                    {"x": random.randint(20, 780), "y": -450}
                ]
                # Reset collectible power-ups
                powerup_active = False
                powerup_type = None
                powerup_y = -30
                next_powerup_time = 10000

                #Reset active abilities
                active_ability = None
                ability_end_time = 0

            # Press Escape to quit
            if event.key == pygame.K_ESCAPE:
                running = False


    # Check which keys are being pressed
    if game_started and not game_over:
        keys = pygame.key.get_pressed()
        # Track gameplay time
        game_time = pygame.time.get_ticks() - start_time

        # Spawn a random power-up after 10 seconds
        if game_time >= next_powerup_time and not powerup_active:
            powerup_active = True
            powerup_type = random.choice(powerup_types)
            powerup_x = random.randint(20, 780)
            powerup_y = -30

        # Move the collectible downward
        if powerup_active:
            powerup_y += powerup_speed

            # Remove it when it leaves the screen
            if powerup_y > 600 + powerup_radius:
                powerup_active = False
                next_powerup_time = game_time + 15000

        if keys[pygame.K_LEFT]:
            player_x -= player_speed

        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        # Keep the player inside the window
        player_x = max(0, min(player_x, 750))
        player_y = max(0, min(player_y, 550))
        # Create a collision box around the player
        player_rect = pygame.Rect(player_x, player_y, 50, 50)
        
        # Check if the player collects a power-up
        if powerup_active:
            powerup_rect = pygame.Rect(
                powerup_x - powerup_radius,
                powerup_y - powerup_radius,
                powerup_radius * 2,
                powerup_radius * 2
            )

            if player_rect.colliderect(powerup_rect):
                active_ability = powerup_type
                ability_end_time = game_time + powerup_duration

                powerup_active = False
                next_powerup_time = game_time + 15000
        # End the ability when its timer expires
        if active_ability is not None:
            if game_time >= ability_end_time:
                active_ability = None
                ability_end_time = 0

        # Calculate survival time in seconds
        survival_time = (pygame.time.get_ticks() - start_time) // 1000
        # Increase snowball speed every 10 seconds
        snowball_speed = base_snowball_speed + (survival_time // 10)
       
        # Determine snowball speed
        if active_ability == "time_slow":
            current_snowball_speed = snowball_speed * 0.5
        else:
            current_snowball_speed = snowball_speed

        # Move and check each snowball
        for snowball in snowballs:

            # Move snowball downward
            snowball["y"] += current_snowball_speed

            # Reset snowball when it leaves the screen
            if snowball["y"] > 600 + snowball_radius:
                snowball["y"] = -snowball_radius
                snowball["x"] = random.randint(20, 780)
            
            # Body Heat Shield melts nearby snowballs
            if active_ability == "body_heat":

                # Find the center of the player
                player_center_x = player_x + 25
                player_center_y = player_y + 25

                # Calculate distance from player to snowball
                distance_x = snowball["x"] - player_center_x
                distance_y = snowball["y"] - player_center_y

                distance_squared = distance_x ** 2 + distance_y ** 2

                # Melt snowballs inside the shield radius
                if distance_squared <= body_heat_radius ** 2:
                    snowball["x"] = random.randint(20, 780)
                    snowball["y"] = -snowball_radius
                    continue

            # Create snowball collision box
            snowball_rect = pygame.Rect(
                snowball["x"] - snowball_radius,
                snowball["y"] - snowball_radius,
                snowball_radius * 2,
                snowball_radius * 2
            )

            
            # Check for collision with player
            if player_rect.colliderect(snowball_rect):
                game_over = True

                # Save a new high score
                if survival_time > high_score:
                    high_score = survival_time

                    with open(high_score_file, "w") as file:
                        file.write(str(high_score))

                break

    # Move decorative snowflakes
    if game_started and not game_over:
        for snowflake in snowflakes:
            snowflake["y"] += snowflake["speed"]

            # Return snowflakes to the top
            if snowflake["y"] > 600:
                snowflake["y"] = 0
                snowflake["x"] = random.randint(0, 800)
    # Draw the background
    screen.fill((200, 220, 255))

    # Draw distant snowy mountains
    pygame.draw.polygon(
        screen,
        (160, 190, 215),
        [(0, 450), (180, 170), (360, 450)]
    )

    pygame.draw.polygon(
        screen,
        (140, 175, 205),
        [(220, 450), (480, 130), (740, 450)]
    )

    pygame.draw.polygon(
        screen,
        (170, 200, 225),
        [(540, 450), (700, 220), (800, 450)]
    )

    # Draw snowy ground
    pygame.draw.rect(
        screen,
        (245, 250, 255),
        (0, 575, 800, 25)
    )

    # Draw decorative snowflakes
    for snowflake in snowflakes:
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (snowflake["x"], snowflake["y"]),
            snowflake["size"]
        )
   
    # Draw falling power-ups
    if powerup_active:

        if powerup_type == "time_slow":
            # Green clock
            pygame.draw.circle(
                screen, (20, 90, 45),
                (powerup_x, powerup_y), 14
            )
            pygame.draw.circle(
                screen, (50, 220, 100),
                (powerup_x, powerup_y), 11
            )

            # Clock hands
            pygame.draw.line(
                screen, (255, 255, 255),
                (powerup_x, powerup_y),
                (powerup_x, powerup_y - 7), 2
            )
            pygame.draw.line(
                screen, (255, 255, 255),
                (powerup_x, powerup_y),
                (powerup_x + 6, powerup_y + 3), 2
            )

            # Center dot
            pygame.draw.circle(
                screen, (255, 255, 255),
                (powerup_x, powerup_y), 2
            )

        elif powerup_type == "body_heat":
            # Animated flickering flame
            flicker = random.randint(-3, 3)

            # Outer red flame
            pygame.draw.polygon(
                screen, (230, 45, 20),
                [
                    (powerup_x - 12, powerup_y + 12),
                    (powerup_x - 8, powerup_y - 5),
                    (powerup_x - 3, powerup_y),
                    (powerup_x, powerup_y - 17 + flicker),
                    (powerup_x + 6, powerup_y - 3),
                    (powerup_x + 11, powerup_y + 12)
                ]
            )

            # Inner yellow flame
            pygame.draw.polygon(
                screen, (255, 210, 40),
                [
                    (powerup_x - 6, powerup_y + 10),
                    (powerup_x - 3, powerup_y + 1),
                    (powerup_x, powerup_y - 8 + flicker),
                    (powerup_x + 5, powerup_y + 10)
                ]
            )
    # Draw Body Heat Shield around the player
    if active_ability == "body_heat":

        shield_surface = pygame.Surface(
            (body_heat_radius * 2, body_heat_radius * 2),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            shield_surface,
            (255, 130, 30, 65),
            (body_heat_radius, body_heat_radius),
            body_heat_radius
        )

        pygame.draw.circle(
            shield_surface,
            (255, 160, 50, 200),
            (body_heat_radius, body_heat_radius),
            body_heat_radius,
            3
        )

        screen.blit(
            shield_surface,
            (
                player_x + 25 - body_heat_radius,
                player_y + 25 - body_heat_radius
            )
        )
    # Draw the player's legs
    pygame.draw.rect(
        screen,
        (40, 40, 60),
        (player_x + 10, player_y + 35, 12, 15)
    )

    pygame.draw.rect(
        screen,
        (40, 40, 60),
        (player_x + 28, player_y + 35, 12, 15)
    )

    # Draw the winter jacket
    pygame.draw.rect(
        screen,
        (220, 40, 40),
        (player_x + 5, player_y + 15, 40, 25)
    )

    # Draw the character's face
    pygame.draw.circle(
        screen,
        (245, 195, 150),
        (player_x + 25, player_y + 12),
        11
    )

    # Draw the winter hat
    pygame.draw.rect(
        screen,
        (30, 90, 180),
        (player_x + 13, player_y, 24, 8)
    )

    # Draw the hat's pom-pom
    pygame.draw.circle(
        screen,
        (255, 255, 255),
        (player_x + 25, player_y),
        5
    )


    # Draw every snowball
    for snowball in snowballs:
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (snowball["x"], snowball["y"]),
            snowball_radius
        )
    # Display survival score
    score_text = font.render(
        f"Survival Time: {survival_time}",
        True,
        (0, 0, 0)
        )

    screen.blit(score_text, (10, 10))
    # Display current snowball speed
    speed_text = font.render(
        f"Snowball Speed: {current_snowball_speed}",
        True,
        (0, 0, 0)
    )
    screen.blit(speed_text, (10, 45))

    # Display high score
    high_score_text = font.render(
        f"High Score: {high_score}s",
        True,
        (0, 0, 0)
    )

    screen.blit(high_score_text, (10, 80))

    
    # Display active power-up countdown
    if active_ability is not None:

        # Calculate remaining time
        remaining_ms = max(0, ability_end_time - game_time)
        remaining_seconds = (remaining_ms + 999) // 1000

        # Identify the active ability
        if active_ability == "time_slow":
            ability_name = "TIME SLOW"
        else:
            ability_name = "BODY HEAT SHIELD"

        # Default text color is white
        timer_color = (255, 255, 255)

        # Flash red during the final 5 seconds
        if remaining_ms <= powerup_warning_time:
            if (pygame.time.get_ticks() // 300) % 2 == 0:
                timer_color = (255, 60, 60)

        # Create countdown text
        ability_text = font.render(
            f"{ability_name}: {remaining_seconds}s",
            True,
            timer_color
        )

        # Display countdown in upper-right corner
        screen.blit(
            ability_text,
            ability_text.get_rect(topright=(780, 10))
        )

    # Display Game Over screen
    if game_over:

        # Create a dark transparent overlay
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Create Game Over message
        game_over_text = game_over_font.render(
            "GAME OVER",
            True,
            (255, 255, 255)
        )

        final_score_text = font.render(
            f"You survived {survival_time} seconds!",
            True,
            (255, 255, 255)
        )

        screen.blit(game_over_text, (230, 200))
        screen.blit(final_score_text, (250, 290))
        
        # Display personal best on Game Over screen
        personal_best_text = font.render(
            f"Personal Best: {high_score} seconds",
            True,
            (255, 215, 0)
        )

        screen.blit(
            personal_best_text,
            personal_best_text.get_rect(center=(400, 330))
        )

        restart_text = font.render(
            "Press R to Restart | ESC to Quit",
            True,
            (255, 255, 255)
        )

        screen.blit(restart_text, (175, 390))

    
    
    # Display main menu before the game starts
    if not game_started:

        # Cover the gameplay screen
        screen.fill((30, 60, 90))

        title_text = title_font.render(
            "AVALANCHE SURVIVOR",
            True,
            (255, 255, 255)
        )

        start_text = font.render(
            "Press SPACE to Start",
            True,
            (255, 255, 255)
        )

        controls_text = font.render(
            "LEFT / RIGHT to Move",
            True,
            (200, 220, 255)
        )

        screen.blit(
            title_text,
            title_text.get_rect(center=(400, 220))
        )

        screen.blit(
            start_text,
            start_text.get_rect(center=(400, 320))
        )

        screen.blit(
            controls_text,
            controls_text.get_rect(center=(400, 370))
        )


    # Update the display
    pygame.display.flip()

    # Limit game to 60 frames per second
    clock.tick(60)

pygame.quit()

