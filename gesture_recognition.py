class GestureRecognizer:
    def __init__(self):
        # Landmark IDs for fingertips and their corresponding lower joints
        self.tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky

    def get_finger_states(self, landmarks):
        """
        Returns a list of 5 values (0 or 1) representing whether
        each finger is extended (1) or folded (0).
        Order: [Thumb, Index, Middle, Ring, Pinky]
        """
        if not landmarks or len(landmarks) < 21:
            return []

        fingers = []

        # Thumb (compare x-coordinates since thumb moves sideways)
        if landmarks[self.tip_ids[0]][1] > landmarks[self.tip_ids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other 4 fingers (compare y-coordinates: tip above joint = extended)
        for i in range(1, 5):
            tip_y = landmarks[self.tip_ids[i]][2]
            pip_y = landmarks[self.tip_ids[i] - 2][2]
            if tip_y < pip_y:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def recognize_gesture(self, landmarks):
        """
        Returns a gesture label string based on finger states.
        For now: only OPEN_PALM is implemented (more gestures added next).
        """
        fingers = self.get_finger_states(landmarks)

        if not fingers:
            return "NONE"

        total_extended = sum(fingers)

        # Open Palm: most/all fingers extended
        if total_extended >= 4:
            return "OPEN_PALM"

        return "UNKNOWN"