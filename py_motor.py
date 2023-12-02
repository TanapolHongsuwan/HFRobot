import pygame
import Adafruit_PCA9685

# Initialize the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Set the PWM frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))

# Define servo channel
servo_channel = 0  # The channel the servo is connected to

# Function to set the servo position
def set_servo_angle(channel, angle):
    # Convert the angle to a PWM value
    pulse_length = 4096    # The number of ticks a PWM signal should be high during one period (1/60 seconds)
    pulse = int((pulse_length * angle) / 180)  # Convert angle to pulse
    pwm.set_pwm(channel, 0, pulse)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.KEYDOWN:
            # Move servo when certain keys are pressed
            if event.key == pygame.K_LEFT:
                set_servo_angle(servo_channel, 45)  # Turn servo to 45 degrees
            elif event.key == pygame.K_RIGHT:
                set_servo_angle(servo_channel, 135) # Turn servo to 135 degrees
            # Add more key events to control the servo as needed

    # Update the display (not necessary for servo control, but included for pygame completeness)
    pygame.display.flip()

# Quit Pygame
pygame.quit()
