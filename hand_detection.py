import cv2
import mediapipe as mp

# MediaPipeの手の検出モジュールを初期化
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

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
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # ウィンドウに映像を表示
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

# リソースを解放
cap.release()
