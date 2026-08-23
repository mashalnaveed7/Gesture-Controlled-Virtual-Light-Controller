import cv2

def main():
    # Initialize webcam (0 = default camera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Webcam started. Press 'Q' to quit.")

    while True:
        success, frame = cap.read()

        if not success:
            print("Error: Failed to read frame from webcam.")
            break

        # Flip horizontally for a natural "mirror" view
        frame = cv2.flip(frame, 1)

        # Display FPS on screen (optional but nice touch)
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

        # Exit when 'Q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()