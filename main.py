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

    print("Webcam + Hand Tracking + Gesture Recognition started.")
    print("Press 'Q' to quit.")

    while True:
        success, frame = cap.read()

        if not success:
            print("Error: Failed to read frame from webcam.")
            break

        # Flip frame horizontally for a mirror effect
        frame = cv2.flip(frame, 1)

        # Detect hands
        frame = tracker.find_hands(frame)

        # Get landmark positions
        landmarks = tracker.get_landmark_positions(frame)

        # Default gesture
        gesture = "NONE"

        if landmarks:
            # Recognize gesture
            gesture = recognizer.recognize_gesture(landmarks)

            # Get index fingertip position
            index_tip = landmarks[8]

            # Draw circle on index fingertip
            cv2.circle(
                frame,
                (index_tip[1], index_tip[2]),
                8,
                (255, 0, 255),
                cv2.FILLED
            )

            # Get pinch distance
            distance = recognizer.get_pinch_distance(landmarks)

            # Display pinch distance for threshold tuning
            if distance is not None:
                cv2.putText(
                    frame,
                    f"Pinch Dist: {int(distance)}",
                    (10, 110),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 0),
                    2
                )

        # Display gesture text
        cv2.putText(
            frame,
            f"Gesture: {gesture}",
            (10, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 255),
            2
        )

        # Display quit instruction
        cv2.putText(
            frame,
            "Press 'Q' to Quit",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        # Show webcam window
        cv2.imshow(
            "Gesture Controlled Virtual Light Controller",
            frame
        )

        # Quit when Q is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()