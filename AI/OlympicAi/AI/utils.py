import numpy as np
from mediapipe.python.solutions.pose import PoseLandmark


# Dictionary of joint indices for easy access
JOINTS = {
    "right_knee": {
        "hip": PoseLandmark.RIGHT_HIP.value,
        "knee": PoseLandmark.RIGHT_KNEE.value,
        "ankle": PoseLandmark.RIGHT_ANKLE.value,
    },
    "left_knee": {
        "hip": PoseLandmark.LEFT_HIP.value,
        "knee": PoseLandmark.LEFT_KNEE.value,
        "ankle": PoseLandmark.LEFT_ANKLE.value,
    },
    # Add more joints as needed
}


def get_joint_coords(landmarks, joint_name):
    """
    Returns the coordinates (x, y, z) for the specified joint.
    Args:
        landmarks: List of pose landmarks from MediaPipe.
        joint_name: Name of the joint as in JOINTS.
    Returns:
        Tuple of (hip, knee, ankle) coordinates for the joint.
    """
    joint = JOINTS[joint_name]
    hip = [landmarks[joint["hip"]].x, landmarks[joint["hip"]].y, landmarks[joint["hip"]].z]
    knee = [landmarks[joint["knee"]].x, landmarks[joint["knee"]].y, landmarks[joint["knee"]].z]
    ankle = [landmarks[joint["ankle"]].x, landmarks[joint["ankle"]].y, landmarks[joint["ankle"]].z]
    return hip, knee, ankle


def calculate_angle(p1, p2, p3):
    """
    Calculate the angle between three points in 2D (x, y) space.
    Args:
        p1, p2, p3: Points in (x, y) format.
    Returns:
        Angle in degrees.
    """
    a = np.array([p1[0] - p2[0], p1[1] - p2[1]])
    b = np.array([p3[0] - p2[0], p3[1] - p2[1]])
    cosine_angle = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    # Clamp value to avoid numerical errors
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
    angle = np.arccos(cosine_angle)
    return np.degrees(angle)