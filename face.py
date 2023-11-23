import pygame

# Initialize Pygame
pygame.init()

# Define the screen size
#screen_width, screen_height = 800, 600
#screen = pygame.display.set_mode((screen_width, screen_height))

# Set the display to full screen
infoObject = pygame.display.Info()
width, height = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)


# Define colors
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)  # Color for the eyes
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)  # Color for the face

# Set up robot face properties
face_color = WHITE
face_radius = 100
face_position = (width // 2, height // 2)

# Define emotions as different sets of eyes and mouths
emotions = {
    'normal': {'eyebrows': 'none', 'eyes': 'normal', 'mouth': 'smile'},
    'tie': {'eyebrows': 'surprise', 'eyes': 'normal', 'mouth': 'surprise'},
    'sad': {'eyebrows': 'surprise', 'eyes': 'sad', 'mouth': 'frown'},
    'angry': {'eyebrows': 'surprise', 'eyes': 'angry', 'mouth': 'line'}
}

# Start with a default emotion
current_emotion = 'normal'

# Function to draw the robot face based on the current emotion
def draw_robot_face(emotion):
    screen.fill(BLACK)

    # Draw the face
    pygame.draw.circle(screen, BLACK, face_position, face_radius)

    # Eyebrows
    if emotions[emotion]['eyebrows'] == 'none':
        # Draw nothing
        pass
    elif emotions[emotion]['eyebrows'] == 'surprise':
        # Draw surprise eyebrows
        pygame.draw.arc(screen, LIGHT_BLUE, (face_position[0] - 280, face_position[1] - 200, 80, 80), 2*3.14, 3.14, 5) # posw,posh) erase (draw black), draw (blue), line size)
        pygame.draw.arc(screen, LIGHT_BLUE, (face_position[0] + 220, face_position[1] - 200, 80, 80), 2*3.14, 3.14, 5) # posw,posh) erase (draw black), draw (blue), line size)

    # Eyes
    if emotions[emotion]['eyes'] == 'normal':
        # Draw normal eyes
        pygame.draw.ellipse(screen, LIGHT_BLUE, (face_position[0] - 250, face_position[1] - 100, 20, 40)) #pos, w, h
        pygame.draw.ellipse(screen, LIGHT_BLUE, (face_position[0] + 250, face_position[1] - 100, 20, 40))
    elif emotions[emotion]['eyes'] == 'sad':
        # Draw sad eyes
        pygame.draw.ellipse(screen, LIGHT_BLUE, (face_position[0] - 50, face_position[1] - 20, 30, 20))
        pygame.draw.ellipse(screen, LIGHT_BLUE, (face_position[0] + 20, face_position[1] - 20, 30, 20))
    elif emotions[emotion]['eyes'] == 'angry':
        # Draw angry eyes
        pygame.draw.line(screen, LIGHT_BLUE, (face_position[0] - 50, face_position[1] - 30), (face_position[0] - 20, face_position[1] - 20), 5)
        pygame.draw.line(screen, LIGHT_BLUE, (face_position[0] + 50, face_position[1] - 30), (face_position[0] + 20, face_position[1] - 20), 5)

    # Mouth
    if emotions[emotion]['mouth'] == 'smile':
        # Draw smile mouth
        pygame.draw.arc(screen, LIGHT_BLUE, (face_position[0] - 40, face_position[1], 80, 80), 3.14, 2*3.14, 5) # w,h) erase (draw black), draw (blue), line size)
    elif emotions[emotion]['mouth'] == 'surprise':
        # Draw surprise mouth
        pygame.draw.arc(screen, LIGHT_BLUE, (face_position[0] - 30, face_position[1], 50, 80), 0, 2*3.14, 5)
    elif emotions[emotion]['mouth'] == 'frown':
        # Draw frown mouth
        pygame.draw.arc(screen, LIGHT_BLUE, (face_position[0] - 40, face_position[1] + 20, 80, 50), 3.14, 2*3.14, 5)
    elif emotions[emotion]['mouth'] == 'line':
        # Draw line mouth
        pygame.draw.line(screen, LIGHT_BLUE, (face_position[0] - 40, face_position[1] + 40), (face_position[0] + 40, face_position[1] + 40), 5)

    pygame.display.flip()

# Main loop
running = True
while running:
    # Did the user click the window close button or press the ESC key?
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.KEYDOWN:
            # Check for specific key presses to change the emotion
            if event.key == pygame.K_1:
                current_emotion = 'normal'
            elif event.key == pygame.K_2:
                current_emotion = 'tie'
            elif event.key == pygame.K_3:
                current_emotion = 'sad'
            elif event.key == pygame.K_4:
                current_emotion = 'angry'
    
    draw_robot_face(current_emotion)

# Exit Pygame
pygame.quit()
