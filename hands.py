import pygame
import random
import hand_detection as hd

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

# Set the display to full screen
infoObject = pygame.display.Info()
width, height = infoObject.current_w, infoObject.current_h
#screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

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
    'happy': {'eyes': 'happy', 'mouth': 'smile'},
    'sad': {'eyes': 'sad', 'mouth': 'frown'},
    'angry': {'eyes': 'angry', 'mouth': 'line'}
}

# Start with a default emotion
current_emotion = 'happy'

# Function to draw the robot face based on the current emotion
def draw_robot_face(emotion):

    # Draw the face
    pygame.draw.circle(screen, BLACK, face_position, face_radius)

    # Eyes
    if emotions[emotion]['eyes'] == 'happy':
        # Draw happy eyes
        pygame.draw.ellipse(screen, LIGHT_BLUE, (face_position[0] - 50, face_position[1] - 20, 20, 30))
        pygame.draw.ellipse(screen, LIGHT_BLUE, (face_position[0] + 20, face_position[1] - 20, 20, 30))
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
        pygame.draw.arc(screen, LIGHT_BLUE, (face_position[0] - 45, face_position[1], 80, 50), 3.14, 2*3.14, 5)
    elif emotions[emotion]['mouth'] == 'frown':
        # Draw frown mouth
        pygame.draw.arc(screen, LIGHT_BLUE, (face_position[0] - 40, face_position[1] + 20, 80, 50), 3.14, 2*3.14, 5)
    elif emotions[emotion]['mouth'] == 'line':
        # Draw line mouth
        pygame.draw.line(screen, LIGHT_BLUE, (face_position[0] - 40, face_position[1] + 40), (face_position[0] + 40, face_position[1] + 40), 5)

    #pygame.display.flip()

# Main loop
running = True
current_emotion = 'happy'
current_image = paper_image
font = pygame.font.Font(None, 55)

# Clear the screen
screen.fill((0, 0, 0))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

    key = random.randrange(3)
    if key == 0:
        current_image = rock_image
    elif key == 1:
        current_image = scissors_image
    elif key == 2:
        current_image = paper_image

    for i in range(3, 0, -1):
        screen.fill((0, 0, 0))
        text = font.render(str(i), True, (255,255,255))
        screen.blit(text, [20, 100])
        screen.blit(rock_image, (50, 250))
        draw_robot_face('happy')
        pygame.display.update()
        pygame.time.delay(1000)

    screen.fill((0, 0, 0))
    screen.blit(current_image, (50, 250))
    draw_robot_face('happy')
    pygame.display.update()

    # Get hand shape
    hand_shape = hd.GetHandShape()
    judge = ( key - hand_shape + 3 ) % 3

    if judge == 0:
        current_emotion = 'sad'
        print('Draw')
    elif judge == 1:
        current_emotion = 'angry'
        print('Win')
    elif judge == 2:
        current_emotion = 'happy'
        print('Lose')
    #print(current_emotion)

    screen.fill((0, 0, 0))

    draw_robot_face(current_emotion)

    # Draw the current image if it's not None
    #if current_image is not None:
    screen.blit(current_image, (50, 250))  # Draw the image at position (50, 50)

    # Update the display
    pygame.display.update()
    pygame.time.delay(5000)


# Quit pygame
pygame.quit()
