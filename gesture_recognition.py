import math

class GestureRecognizer:
    def __init__(self):
        # Landmark IDs for fingertips and their corresponding lower joints
        self.tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
        self.pinch_threshold = 40  # pixels — tune this based on your camera/distance

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

    def get_pinch_distance(self, landmarks):
        """
        Calculates Euclidean distance between thumb tip (id 4)
        and index tip (id 8). Returns None if landmarks unavailable.
        """
        if not landmarks or len(landmarks) < 21:
            return None

        x1, y1 = landmarks[4][1], landmarks[4][2]
        x2, y2 = landmarks[8][1], landmarks[8][2]

        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return distance

    def recognize_gesture(self, landmarks):
        """
        Returns a gesture label string based on finger states.
        Currently supports: OPEN_PALM, FIST, INDEX, PINCH
        """
        fingers = self.get_finger_states(landmarks)

        if not fingers:
            return "NONE"

        total_extended = sum(fingers)

        # Fist: all (or nearly all) fingers folded
        if total_extended == 0:
            return "FIST"

        # Pinch: thumb and index close together, other fingers folded
        distance = self.get_pinch_distance(landmarks)
        if distance is not None and distance < self.pinch_threshold and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            return "PINCH"

        # Index: only the index finger extended
        if fingers[1] == 1 and fingers[0] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            return "INDEX"

        # Open Palm: most/all fingers extended
        if total_extended >= 4:
            return "OPEN_PALM"

        return "UNKNOWN"