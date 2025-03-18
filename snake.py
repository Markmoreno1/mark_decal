import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Set up display dimensions
width, height = 600, 400
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red   = (255, 0, 0)
green = (0, 255, 0)

# Game settings
snake_block = 10
snake_speed = 12

clock = pygame.time.Clock()

# Fonts for displaying messages
font_style = pygame.font.SysFont(None, 50)

def draw_snake(snake_block, snake_list):
    """Draw each segment of the snake."""
    for x in snake_list:
        pygame.draw.rect(window, black, [x[0], x[1], snake_block, snake_block])

def show_message(msg, color):
    """Display a message on the screen."""
    mesg = font_style.render(msg, True, color)
    window.blit(mesg, [width / 6, height / 3])

def gameLoop():
    """Main game loop."""
    game_over = False
    game_close = False

    # Starting position of the snake's head (center of the window)
    x1 = width / 2
    y1 = height / 2

    # Initial movement (no movement)
    x1_change = 0
    y1_change = 0

    snake_list = []
    snake_length = 1

    # Place food at a random position
    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    while not game_over:
        # Game over screen loop
        while game_close:
            window.fill(white)
            show_message("You lost! Press Q-Quit or C-Play Again", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # Process events (keyboard, window close, etc.)
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

        # Check for collision with boundaries
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        # Update snake's head position
        x1 += x1_change
        y1 += y1_change
        window.fill(white)

        # Draw the food
        pygame.draw.rect(window, green, [foodx, foody, snake_block, snake_block])

        # Update snake's body
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check for collision with self
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        # Draw snake and update display
        draw_snake(snake_block, snake_list)
        pygame.display.update()

        # Check if snake eats the food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            snake_length += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Run the game
gameLoop()
