import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))

# Load images
rock_image = pygame.image.load('image/rock.png')
scissors_image = pygame.image.load('image/scissors.png')
paper_image = pygame.image.load('image/paper.png')

# Resize the images
rock_image = pygame.transform.scale(rock_image, (100, 100))
scissors_image = pygame.transform.scale(scissors_image, (100, 100))
paper_image = pygame.transform.scale(paper_image, (100, 100))

# Set the initial image to None (to display nothing)
current_image = None

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        # Change image on key press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_image = rock_image
            elif event.key == pygame.K_2:
                current_image = scissors_image
            elif event.key == pygame.K_3:
                current_image = paper_image
            elif event.key == pygame.K_0:
                current_image = None  # Set to None to display nothing

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the current image if it's not None
    if current_image is not None:
        screen.blit(current_image, (50, 50))  # Draw the image at position (50, 50)

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
