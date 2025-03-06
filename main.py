import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display dimensions
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

# Create the display surface
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set window title
pygame.display.set_caption("My Game")

# Fill screen with white color
screen.fill((255, 255, 255))

# Update the display
pygame.display.flip()

# Draw the pipes
def draw_pipes(x, gap_start):
    # Draw top portion of pipe
    top_pipe = pygame.draw.rect(screen, (255, 255, 0), (x, 0, 50, gap_start))
    
    # Draw bottom portion of pipe
    bottom_pipe = pygame.draw.rect(screen, (255, 255, 0), (x, gap_start + 100, 50, 600 - (gap_start + 100)))

def draw_bird():
    # Bird dimensions
    bird_width = 20
    bird_height = 15
    
    # Calculate bird position (center of screen)
    bird_x = SCREEN_WIDTH // 2 - bird_width // 2
    bird_y = SCREEN_HEIGHT // 2 - bird_height // 2
    
    # Draw the bird as a yellow rectangle
    bird = pygame.draw.rect(screen, (255, 255, 0), (bird_x, bird_y, bird_width, bird_height))
    
    # Draw an eye (black circle)
    eye_x = bird_x + bird_width - 10
    eye_y = bird_y + 10
    pygame.draw.circle(screen, (0, 0, 0), (eye_x, eye_y), 4)
    
    # Update display to show bird
    pygame.display.update()

def check_collision(bird_x, bird_y, pipe):
    # Bird hitbox dimensions
    bird_width = 20
    bird_height = 15
    
    # Create bird rectangle for collision detection
    bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)

    #Check if bird collides with pipes
    if bird_rect.colliderect(pipe):
        return True
            
    return False


def game_loop():
    # Bird initial state
    bird_y = SCREEN_HEIGHT // 2  # Starting y position
    bird_speed = 0
    gravity = 0.5
    jump_strength = -10

    # Pipe initial state
    pipe_speed = 5  # Speed at which pipes move left
    pipes = [(SCREEN_WIDTH, random.randint(0, 350))]  # Start with one pipe at right edge

    # Define user score
    user_score = 0

    # Define pipe passed state
    passed_pipes = set()
    
    while True:
        # Apply gravity to bird
        bird_speed += gravity
        bird_y += bird_speed

        # Keep bird within screen bounds
        if bird_y < 0:
            bird_y = 0
            bird_speed = 0
        elif bird_y > SCREEN_HEIGHT - 15:  # 15 is bird height
            bird_y = SCREEN_HEIGHT - 15
            bird_speed = 0

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    bird_speed = jump_strength

        # Clear screen
        screen.fill((255, 255, 255))

        # Draw bird
        bird_x = SCREEN_WIDTH // 2 - 20 // 2  # 20 is bird width
        pygame.draw.rect(screen, (255, 255, 0), (bird_x, bird_y, 20, 15))
        pygame.draw.circle(screen, (0, 0, 0), (bird_x + 10, bird_y + 10), 4)

        # Draw all pipes at their current positions
        for x, gap_pos in pipes:
            draw_pipes(x, gap_pos)
            
        # Move existing pipes left
        pipes = [(x - pipe_speed, gap_pos) for x, gap_pos in pipes]
            
        # Remove pipes that are off screen
        pipes = [(x, gap_pos) for x, gap_pos in pipes if x >= -50]
            
        # Add new pipe when rightmost pipe moves in enough
        if pipes[-1][0] <= SCREEN_WIDTH - 300:  # Space pipes 300px apart
            pipes.append((SCREEN_WIDTH, random.randint(0, 350)))

        pygame.display.update()
        pygame.time.delay(30)
    
        for pipe in pipes:  # Fixed missing colon
            # Create rectangles for top and bottom pipes
            top_pipe = pygame.Rect(pipe[0], pipe[1] - 400, 50, 400)  # Top pipe extends upward
            bottom_pipe = pygame.Rect(pipe[0], pipe[1] + 100, 50, 400)  # Bottom pipe starts below gap
            
            # Check collision with either pipe
            if check_collision(bird_x, bird_y, top_pipe) or check_collision(bird_x, bird_y, bottom_pipe):
                print("Game Over")
                pygame.quit()
                sys.exit()

# Start the game
game_loop()
