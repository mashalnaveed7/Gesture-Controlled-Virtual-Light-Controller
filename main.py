import cv2
from hand_tracking import HandTracker
from gesture_recognition import GestureRecognizer

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    tracker = HandTracker(max_hands=1)
    recognizer = GestureRecognizer()

    print("Webcam + Hand Tracking + Gesture Recognition started. Press 'Q' to quit.")

    while True:
        success, frame = cap.read()

        if not success:
            print("Error: Failed to read frame from webcam.")
            break

        frame = cv2.flip(frame, 1)
        frame = tracker.find_hands(frame)
        landmarks = tracker.get_landmark_positions(frame)

        gesture = "NONE"
        if landmarks:
            gesture = recognizer.recognize_gesture(landmarks)

            index_tip = landmarks[8]
            cv2.circle(frame, (index_tip[1], index_tip[2]), 8, (255, 0, 255), cv2.FILLED)

        # Display gesture text on screen
        cv2.putText(
            frame,
            f"Gesture: {gesture}",
            (10, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "Press 'Q' to Quit",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.imshow("Gesture Controlled Virtual Light Controller", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()