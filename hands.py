import pygame
import random
import hand_detection as hd

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)

# Load images
rock_image = pygame.image.load('image/rock.png')
scissors_image = pygame.image.load('image/scissors.png')
paper_image = pygame.image.load('image/paper.png')

hands_image_size = (200, 200)
# Resize the images
rock_image = pygame.transform.scale(rock_image, hands_image_size)
scissors_image = pygame.transform.scale(scissors_image, hands_image_size)
paper_image = pygame.transform.scale(paper_image, hands_image_size)

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
    'normal': {'eyebrows': 'none', 'eyes': 'normal', 'mouth': 'smile'},
    'tie': {'eyebrows': 'surprise', 'eyes': 'normal', 'mouth': 'surprise'},
    'win1': {'eyebrows': 'none', 'eyes': 'happy', 'mouth': 'cat'},
    'lose1': {'eyebrows': 'surprise', 'eyes': 'normal', 'mouth': 'sad'},
    'win2': {'eyebrows': 'none', 'eyes': 'excited', 'mouth': 'tongue'},
    'lose2': {'eyebrows': 'none', 'eyes': 'cry', 'mouth': 'sad'}
}

# Start with a default emotion
current_emotion = 'normal'

# Function to draw the robot face based on the current emotion
def draw_robot_face(emotion):
    # Draw the face
    pygame.draw.circle(screen, BLACK, face_position, face_radius)
    line_width = 20

    # Eyebrows
    if emotions[emotion]['eyebrows'] == 'none':
        # Draw nothing
        pass
    elif emotions[emotion]['eyebrows'] == 'surprise':
        # Draw surprise eyebrows
        pygame.draw.arc(screen, LIGHT_BLUE, (face_position[0] - 430, face_position[1] - 250, 100, 100), 2*3.14, 3.14, width=line_width) # posw,posh) erase (draw black), draw (blue), line size)
        pygame.draw.arc(screen, LIGHT_BLUE, (face_position[0] + 370, face_position[1] - 250, 100, 100), 2*3.14, 3.14, width=line_width) # posw,posh) erase (draw black), draw (blue), line size)

    # Eyes
    if emotions[emotion]['eyes'] == 'normal':
        # Draw normal eyes
        pygame.draw.ellipse(screen, LIGHT_BLUE, (face_position[0] - 400, face_position[1] - 150, 50, 150)) #Rect=（中心ｘ座標、中心ｙ座標、幅、高さ）
        pygame.draw.ellipse(screen, LIGHT_BLUE, (face_position[0] + 400, face_position[1] - 150, 50, 150))
    elif emotions[emotion]['eyes'] == 'happy':
        # Draw happy eyes
        pygame.draw.arc(screen, LIGHT_BLUE, (face_position[0] - 430, face_position[1] - 180, 100, 100), 2*3.14, 3.14, width=line_width)
        pygame.draw.arc(screen, LIGHT_BLUE, (face_position[0] + 370, face_position[1] - 180, 100, 100), 2*3.14, 3.14, width=line_width)
    elif emotions[emotion]['eyes'] == 'excited':
        # Draw excited eyes
        pygame.draw.line(screen, LIGHT_BLUE, (face_position[0] - 300, face_position[1] - 150), (face_position[0] - 400, face_position[1] - 190), width=line_width)
        pygame.draw.line(screen, LIGHT_BLUE, (face_position[0] - 400, face_position[1] - 110), (face_position[0] - 300, face_position[1] - 150), width=line_width)
        pygame.draw.line(screen, LIGHT_BLUE, (face_position[0] + 300, face_position[1] - 150), (face_position[0] + 400, face_position[1] - 190), width=line_width)
        pygame.draw.line(screen, LIGHT_BLUE, (face_position[0] + 400, face_position[1] - 110), (face_position[0] + 300, face_position[1] - 150), width=line_width)
    elif emotions[emotion]['eyes'] == 'cry':
        # Draw cry eyes
        pygame.draw.line(screen, LIGHT_BLUE, (face_position[0] - 300, face_position[1] - 200), (face_position[0] - 400, face_position[1] - 200), width=line_width)
        pygame.draw.line(screen, LIGHT_BLUE, (face_position[0] + 300, face_position[1] - 200), (face_position[0] + 400, face_position[1] - 200), width=line_width)
        pygame.draw.line(screen, LIGHT_BLUE, (face_position[0] - 375, face_position[1] - 200), (face_position[0] - 375, face_position[1] + 200), width=line_width)
        pygame.draw.line(screen, LIGHT_BLUE, (face_position[0] - 325, face_position[1] - 200), (face_position[0] - 325, face_position[1] + 200), width=line_width)
        pygame.draw.line(screen, LIGHT_BLUE, (face_position[0] + 325, face_position[1] - 200), (face_position[0] + 325, face_position[1] + 200), width=line_width)
        pygame.draw.line(screen, LIGHT_BLUE, (face_position[0] + 375, face_position[1] - 200), (face_position[0] + 375, face_position[1] + 200), width=line_width)


    # Mouth
    if emotions[emotion]['mouth'] == 'smile':
        # Draw smile mouth
        pygame.draw.arc(screen, LIGHT_BLUE, (face_position[0] - 40, face_position[1] + 50, 80, 80), 3.14, 2*3.14, width=line_width) # w,h) erase (draw black), draw (blue), line size)
    elif emotions[emotion]['mouth'] == 'surprise':
        # Draw surprise mouth
        pygame.draw.arc(screen, LIGHT_BLUE, (face_position[0] - 30, face_position[1], 50, 80), 0, 2*3.14, width=line_width)
    elif emotions[emotion]['mouth'] == 'cat':
        # Draw cat mouth
        pygame.draw.arc(screen, LIGHT_BLUE, (face_position[0] - 60, face_position[1] + 100, 80, 80), 3.14, 2*3.14, width=line_width)
        pygame.draw.arc(screen, LIGHT_BLUE, (face_position[0] + 10, face_position[1] + 100, 80, 80), 3.14, 2*3.14, width=line_width)
    elif emotions[emotion]['mouth'] == 'sad':
        # Draw sad mouth
        pygame.draw.arc(screen, LIGHT_BLUE, (face_position[0] - 40, face_position[1] + 50, 110, 150), 2*3.14, 3.14, width=line_width)
        #pygame.draw.line(screen, LIGHT_BLUE, (face_position[0] - 20, face_position[1] + 120), (face_position[0] - 10, face_position[1] + 90), width=5)
        #pygame.draw.line(screen, LIGHT_BLUE, (face_position[0] + 50, face_position[1] + 120), (face_position[0] + 40, face_position[1] + 90), width=5)
    elif emotions[emotion]['mouth'] == 'tongue':
        # Draw mouth with tongue
        pygame.draw.arc(screen, LIGHT_BLUE, (face_position[0] - 80, face_position[1] + 20, 80, 80), 3.14, 2*3.14, width=line_width)
        pygame.draw.arc(screen, LIGHT_BLUE, (face_position[0] - 10, face_position[1] + 20, 80, 80), 3.14, 2*3.14, width=line_width)
        pygame.draw.arc(screen, LIGHT_BLUE, (face_position[0] - 40, face_position[1], 80, 200), 3.14, 2*3.14, width=line_width)

    pygame.display.flip()


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
        screen.blit(rock_image, (50, 350))
        draw_robot_face('normal')
        flipped_screen = pygame.transform.flip(screen, True, True)  # Flip horizontally and vertically
        screen.blit(flipped_screen, (0, 0))
        pygame.display.update()
        pygame.time.delay(1000)

    screen.fill((0, 0, 0))
    screen.blit(rock_image, (50, 350))
    draw_robot_face('normal')
    flipped_screen = pygame.transform.flip(screen, True, True)  # Flip horizontally and vertically
    screen.blit(flipped_screen, (0, 0))
    pygame.display.update()

    # Get hand shape
    hand_shape = hd.GetHandShape()
    judge = ( key - hand_shape + 3 ) % 3

    if judge == 0:
        current_emotion = 'tie'
        print('Draw')
    elif judge == 1:
        current_emotion = 'lose2'
        print('Win')
    elif judge == 2:
        current_emotion = 'win2'
        print('Lose')
    #print(current_emotion)

    screen.fill((0, 0, 0))

    # Draw the current image if it's not None
    if current_image is not None:
        screen.blit(current_image, (50, 350))  # Draw the image at position (50, 350)
    draw_robot_face(current_emotion)

    # Flip and update the screen
    flipped_screen = pygame.transform.flip(screen, True, True)  # Flip horizontally and vertical
    screen.blit(flipped_screen, (0, 0))

    # Update the display
    pygame.display.update()
    pygame.time.delay(5000)


# Quit pygame
pygame.quit()
