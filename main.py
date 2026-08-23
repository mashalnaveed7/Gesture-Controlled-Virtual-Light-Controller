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

    print("Gesture Test Mode started. Press 'Q' to quit.")

    # Track gesture counts to confirm each one has been successfully detected
    detected_gestures = set()

    while True:
        success, frame = cap.read()

        if not success:
            print("Error: Failed to read frame from webcam.")
            break

        frame = cv2.flip(frame, 1)
        frame = tracker.find_hands(frame)
        landmarks = tracker.get_landmark_positions(frame)

        gesture = "NONE"
        distance = None

        if landmarks:
            gesture = recognizer.recognize_gesture(landmarks)
            distance = recognizer.get_pinch_distance(landmarks)

            index_tip = landmarks[8]
            cv2.circle(frame, (index_tip[1], index_tip[2]), 8, (255, 0, 255), cv2.FILLED)

            if gesture in ["OPEN_PALM", "FIST", "INDEX", "PINCH", "TWO_FINGERS"]:
                detected_gestures.add(gesture)

        # --- On-screen info panel ---
        cv2.rectangle(frame, (0, 0), (350, 160), (0, 0, 0), -1)

        cv2.putText(frame, f"Gesture: {gesture}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        if distance is not None:
            cv2.putText(frame, f"Pinch Dist: {int(distance)}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        cv2.putText(frame, f"Tested: {len(detected_gestures)}/5", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.putText(frame, ", ".join(sorted(detected_gestures)) or "None yet", (10, 115),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)

        cv2.putText(frame, "Press 'Q' to Quit", (10, 145),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 0), 1)

        cv2.imshow("Gesture Controlled Virtual Light Controller - TEST MODE", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    print("\n--- Test Summary ---")
    all_gestures = {"OPEN_PALM", "FIST", "INDEX", "PINCH", "TWO_FINGERS"}
    missing = all_gestures - detected_gestures
    if not missing:
        print("✅ All 5 gestures detected successfully!")
    else:
        print(f"⚠️ Missing gestures: {missing}")

if __name__ == "__main__":
    main()