import time
import pygame
import Adafruit_PCA9685

# Initialize the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Set the PWM frequency to 50hz, good for servos.
pwm.set_pwm_freq(50)

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))

# Define servo channel and starting angle
servo_channel = 0  # The channel the servo is connected to
current_angle = 90  # Assuming servo starts at 90 degrees

# Function to set the servo position gradually
def set_servo_angle(channel, target_angle, delay=0.02):
    global current_angle  # Use the global variable to track the current angle
    min_pulse = 205  # Min pulse length out of 4096
    max_pulse = 410  # Max pulse length out of 4096
    
    step = 1 if target_angle > current_angle else -1
    for angle in range(current_angle, target_angle, step):
        pulse = int(min_pulse + (angle / 180.0) * (max_pulse - min_pulse))
        pwm.set_pwm(channel, 0, pulse)
        time.sleep(delay)  # Wait for a short period to see the movement
    current_angle = target_angle  # Update the current angle once the loop is complete

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.KEYDOWN:
            # Move servo when certain keys are pressed
            if event.key == pygame.K_LEFT:
                # Turn servo to 45 degrees slowly
                set_servo_angle(servo_channel, 25)
            elif event.key == pygame.K_RIGHT:
                # Turn servo to 135 degrees slowly
                set_servo_angle(servo_channel, 135)

    # Update the display (not necessary for servo control, but included for pygame completeness)
    pygame.display.flip()

# Quit Pygame
pygame.quit()
