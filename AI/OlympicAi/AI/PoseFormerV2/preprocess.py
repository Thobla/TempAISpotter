import numpy as np

# Mapping from MediaPipe (33) → Human3.6M (17)
H36M_MAP = [0, 11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28, 2, 5, 8, 9]

class PosePreprocessor:
    def select_17_keypoints(self, mp_landmarks):
        # mp_landmarks: [frames, 33, 3]
        selected = mp_landmarks[:, H36M_MAP, :2]  # take only x,y
        return selected

    def normalize(self, poses):
        # center pelvis, scale torso
        left_hip, right_hip = 23, 24
        pelvis = (poses[:, left_hip, :] + poses[:, right_hip, :]) / 2
        centered = poses - pelvis[:, None, :]
        scale = np.linalg.norm(centered[:, 11, :] - centered[:, 23, :], axis=1).mean()
        return centered / (scale + 1e-6)
