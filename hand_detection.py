import cv2
import pygame
import numpy as np
import mediapipe as mp
#from face import draw_robot_face

# MediaPipeの手の検出モジュールを初期化
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils


def LandmarksToNumpy(landmarks):
    return np.array([[landmark.x, landmark.y, landmark.z] for landmark in landmarks], dtype=np.float32)


def CalculateAngle(v1, v2):
    dot_product = np.dot(v1, v2)
    norms = np.linalg.norm(v1) * np.linalg.norm(v2)

    return np.arccos(dot_product / norms) * (180.0 / np.pi)

def FingerAngle(landmarks_array):
    thumb = CalculateAngle(landmarks_array[1] - landmarks_array[0], landmarks_array[3] - landmarks_array[4])
    index_finger = CalculateAngle(landmarks_array[5] - landmarks_array[0], landmarks_array[7] - landmarks_array[8])
    middle_finger = CalculateAngle(landmarks_array[9] - landmarks_array[0], landmarks_array[11] - landmarks_array[12])
    third_finger = CalculateAngle(landmarks_array[13] - landmarks_array[0], landmarks_array[15] - landmarks_array[16])
    little_finger = CalculateAngle(landmarks_array[17] - landmarks_array[0], landmarks_array[19] - landmarks_array[20])

    hand_angles = [thumb, index_finger, middle_finger, third_finger, little_finger]

    return hand_angles

def HandshapeJudge(hand_angles):
    hand_shape = "NoSign"

    if hand_angles[1] < 90 and hand_angles[2] < 90 and hand_angles[3] < 90 and hand_angles[4] < 90:
        hand_shape = "happy"
        #hand_shape = "Rock"
    elif hand_angles[1] >= 90 and hand_angles[2] >= 90 and hand_angles[3] < 90 and hand_angles[4] < 90:
        hand_shape = "sad"
        #hand_shape = "Scissors"
    elif hand_angles[1] >= 90 and hand_angles[2] >= 90 and hand_angles[3] >= 90 and hand_angles[4] >= 90:
        hand_shape = "angry"
        #hand_shape = "Paper"

    return hand_shape

# ウェブカメラからの映像を取得
cap = cv2.VideoCapture(0)
pygame.init()


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
    'happy': {'eyes': 'happy', 'mouth': 'smile'},
    'sad': {'eyes': 'sad', 'mouth': 'frown'},
    'angry': {'eyes': 'angry', 'mouth': 'line'}
}

# Start with a default emotion
current_emotion = 'happy'

# Function to draw the robot face based on the current emotion
def draw_robot_face(emotion):
    screen.fill(BLACK)

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

    pygame.display.flip()
#######################################


while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    # 画像をBGRからRGBに変換し、MediaPipeに渡す
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # RGBからBGRに戻す
    #image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # 検出された手の情報を描画
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            #mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            finger_angles = FingerAngle(LandmarksToNumpy(hand_landmarks.landmark))
            hand_shape = HandshapeJudge(finger_angles)
            if hand_shape == 'NoSign':
                pass
            else:
                draw_robot_face(hand_shape)
            #print(hand_shape)
            #cv2.putText(image, hand_shape_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            #print(type(hand_landmarks.landmark[0].x))

    # ウィンドウに映像を表示
    #cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(25) & 0xFF == 27:
        break

    # Pygameイベントループで終了条件をチェック
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                cap.release()
                pygame.quit()
                exit()


# リソースを解放
cap.release()
pygame.quit()
