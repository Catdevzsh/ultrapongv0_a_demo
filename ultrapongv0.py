import pygame
from array import array

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Retro Pong with AI")

# Define a function to generate beep sounds with varying frequencies
def generate_beep_sound(frequency=440, duration=0.1):
    sample_rate = pygame.mixer.get_init()[0]
    max_amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
    samples = int(sample_rate * duration)
    wave = [int(max_amplitude * ((i // (sample_rate // frequency)) % 2)) for i in range(samples)]
    sound = pygame.mixer.Sound(buffer=array('h', wave))
    sound.set_volume(0.1)
    return sound

# Create sounds for game events
ball_hit_paddle_sound = generate_beep_sound(523.25, 0.1)
ball_hit_wall_sound = generate_beep_sound(659.25, 0.1)

# Paddle and ball setup
paddle_width = 10
paddle_height = 60
paddle1_x = 50
paddle1_y = SCREEN_HEIGHT // 2 - paddle_height // 2
paddle1_speed = 0
paddle2_x = SCREEN_WIDTH - 50 - paddle_width
paddle2_y = SCREEN_HEIGHT // 2 - paddle_height // 2
paddle2_speed = 0
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_radius = 10
ball_speed_x = 4  # Adjusted for SNES-like speed
ball_speed_y = 4  # Adjusted for SNES-like speed

# Score variables
score1 = 0
score2 = 0
font = pygame.font.Font(None, 74)

# Setup the clock
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                paddle1_speed = -6
            elif event.key == pygame.K_s:
                paddle1_speed = 6
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_s):
                paddle1_speed = 0

    # Update paddle positions
    paddle1_y += paddle1_speed

    # AI for the right paddle
    if ball_y > paddle2_y + paddle_height / 2:
        paddle2_speed = 6  # Move down
    elif ball_y < paddle2_y + paddle_height / 2:
        paddle2_speed = -6  # Move up
    paddle2_y += paddle2_speed

    # Keep paddles within screen boundaries
    if paddle1_y < 0:
        paddle1_y = 0
    elif paddle1_y > SCREEN_HEIGHT - paddle_height:
        paddle1_y = SCREEN_HEIGHT - paddle_height

    if paddle2_y < 0:
        paddle2_y = 0
    elif paddle2_y > SCREEN_HEIGHT - paddle_height:
        paddle2_y = SCREEN_HEIGHT - paddle_height

    # Update ball position
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Check for ball collisions with paddles and walls
    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= SCREEN_HEIGHT:
        ball_speed_y *= -1
        ball_hit_wall_sound.play()

    if (ball_x - ball_radius <= paddle1_x + paddle_width and
        paddle1_y < ball_y < paddle1_y + paddle_height) or \
       (ball_x + ball_radius >= paddle2_x and
        paddle2_y < ball_y < paddle2_y + paddle_height):
        ball_speed_x *= -1
        ball_hit_paddle_sound.play()

    # Score update
    if ball_x < 0:
        score2 += 1
        ball_x, ball_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        ball_speed_x = -ball_speed_x

    if ball_x > SCREEN_WIDTH:
        score1 += 1
        ball_x, ball_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        ball_speed_x = -ball_speed_x

    # Clear screen
    screen.fill((0, 0, 0))

    # Draw the center line
    pygame.draw.line(screen, (255, 255, 255), (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 1)

    # Draw paddles and ball
    pygame.draw.rect(screen, (255, 255, 255), (paddle1_x, paddle1_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, (255, 255, 255), (paddle2_x, paddle2_y, paddle_width, paddle_height))
    pygame.draw.circle(screen, (255, 255, 255), (ball_x, ball_y), ball_radius)

    # Display scores
    text = font.render(f"{score1}  {score2}", True, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH // 2 - 50, 10))

    # Update display
    pygame.display.flip()

    # Limit to 60 frames per second
    clock.tick(60)

# Quit Pygame
pygame.quit()
