import cv2
import numpy as np
import mediapipe as mp

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
    hand_shape = 0

    if hand_angles[1] < 90 and hand_angles[2] < 90 and hand_angles[3] < 90 and hand_angles[4] < 90:
        hand_shape = 1
    elif hand_angles[1] >= 90 and hand_angles[2] >= 90 and hand_angles[3] < 90 and hand_angles[4] < 90:
        hand_shape = 2
    elif hand_angles[1] >= 90 and hand_angles[2] >= 90 and hand_angles[3] >= 90 and hand_angles[4] >= 90:
        hand_shape = 3

    return hand_shape

# ウェブカメラからの映像を取得
cap = cv2.VideoCapture(0)


while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    # 画像をBGRからRGBに変換し、MediaPipeに渡す
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # RGBからBGRに戻す
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # 検出された手の情報を描画
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            #mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            hand_angles = FingerAngle(LandmarksToNumpy(hand_landmarks.landmark))
            hand_shape = HandshapeJudge(hand_angles)
            hand_shape_text = "NoSign"
            if hand_shape == 1:
                hand_shape_text = "Rock"
            elif hand_shape == 2:
                hand_shape_text = "Scissors"
            elif hand_shape == 3:
                hand_shape_text = "Paper"
            cv2.putText(image, hand_shape_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            #print(type(hand_landmarks.landmark[0].x))

    # ウィンドウに映像を表示
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(25) & 0xFF == 27:
        break

# リソースを解放
cap.release()
