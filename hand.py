import cv2
import numpy as np

# Hand type classification
class HandType:
    ROCK = "Rock"
    SCISSORS = "Scissors"
    PAPER = "Paper"
    UNKNOWN = "Unknown"

# Function to calculate the center from moments
def center(moments):
    if moments["m00"] != 0:
        cx = int(moments["m10"] / moments["m00"])
        cy = int(moments["m01"] / moments["m00"])
    else:
        cx, cy = 0, 0
    return (cx, cy)

# Function to calculate the radius from the contour
def radius(contour):
    _, radius = cv2.minEnclosingCircle(contour)
    return int(radius)

# Start video capture
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera could not be opened.")
else:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("No frame obtained from the camera.")
            break

        # Convert to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (15, 15), 0)

        # Threshold the image
        mean_val = cv2.mean(gray_frame)[0]
        _, binary = cv2.threshold(gray_frame, mean_val * 0.8, 255, cv2.THRESH_BINARY_INV)

        # Find contours
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the largest contour
        max_area = 0
        largest_contour = None
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                largest_contour = contour

        # If the largest contour is big enough to be a hand
        if max_area > 300000 and largest_contour is not None:  # Adjusted from 300000 for better sensitivity
            mask = np.zeros(frame.shape[:2], dtype=np.uint8)
            cv2.drawContours(mask, [largest_contour], -1, 255, -1)

            cnt_moments = cv2.moments(largest_contour)
            cnt_center = center(cnt_moments)
            cnt_radius = radius(largest_contour)

            # Draw a dot at the center of the hand
            cv2.circle(frame, cnt_center, 10, (255, 0, 0), -1)

            mask_circles = np.zeros(frame.shape[:2], dtype=np.uint8)
            cv2.circle(mask_circles, cnt_center, cnt_radius, 255, 20)
            cv2.circle(mask_circles, cnt_center, cnt_radius - 100, 255, 20)

            mask_hand = cv2.bitwise_and(mask, mask_circles)

            finger_contours, _ = cv2.findContours(mask_hand, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            finger_count = 0
            for contour in finger_contours:
                contour_area = cv2.contourArea(contour)
                if 500 < contour_area < 5000:  # Adjusted area thresholds for better sensitivity
                    finger_count += 1
                    finger_moments = cv2.moments(contour)
                    finger_center = center(finger_moments)
                    # Draw a dot at the center of each detected finger contour
                    cv2.circle(frame, finger_center, 5, (0, 255, 0), -1)

            detected_hand = HandType.UNKNOWN
            if finger_count <= 2:
                detected_hand = HandType.ROCK
            elif finger_count <= 4:
                detected_hand = HandType.SCISSORS
            else:
                detected_hand = HandType.PAPER

            # Draw the detected hand type on the screen
            cv2.putText(frame, detected_hand, (70, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 255, 255), 8, cv2.LINE_AA)

        cv2.imshow("Hand Type", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
