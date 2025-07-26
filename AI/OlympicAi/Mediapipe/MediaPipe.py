import os
import cv2
import numpy as np
import mediapipe as mp
from utils import *
from mediapipe.python.solutions.pose import PoseLandmark
from moviepy.editor import VideoFileClip



class MediaPipeVideoProcessor:
    def __init__(self):
        self.pose = mp.solutions.pose.Pose()
        self.drawer = mp.solutions.drawing_utils

    def draw_pose(self, frame, results, all_landmarks=True, calculate_angle=False):
        """Draws pose skeleton on the frame based on the all_landmarks flag."""
        mp_pose = mp.solutions.pose
        mp_drawing = mp.solutions.drawing_utils

        if not results.pose_landmarks:
            return frame

        if all_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
            )
        else:
            exclude_ids = {
                PoseLandmark.NOSE.value,
                PoseLandmark.LEFT_EYE_INNER.value,
                PoseLandmark.LEFT_EYE_OUTER.value,
                PoseLandmark.RIGHT_EYE_INNER.value,
                PoseLandmark.RIGHT_EYE_OUTER.value,
                PoseLandmark.LEFT_EAR.value,
                PoseLandmark.RIGHT_EAR.value,
                PoseLandmark.MOUTH_LEFT.value,
                PoseLandmark.MOUTH_RIGHT.value,
            }
            filtered_connections = [
                (start, end) for (start, end) in mp_pose.POSE_CONNECTIONS
                if start not in exclude_ids and end not in exclude_ids
            ]
            landmark_specs = {}
            for idx in range(len(results.pose_landmarks.landmark)):
                if idx in exclude_ids:
                    landmark_specs[idx] = mp_drawing.DrawingSpec(thickness=0, circle_radius=0)
                else:
                    landmark_specs[idx] = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                filtered_connections,
                landmark_drawing_spec=landmark_specs,
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
            )
        return frame

    def process_video(self, input_path: str, output_path: str, all_landmarks: bool = True, draw_skeleton: bool = True, calculate_angle = False):
        """
        Loads a video, optionally adds MediaPipe pose skeleton to each frame, and saves the processed video.
        Args:
            input_path (str): Path to the input video file.
            output_path (str): Path to save the output video file.
            all_landmarks (bool): Whether to draw all landmarks or exclude some.
            draw_skeleton (bool): Whether to draw the skeleton at all.
        """
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            raise IOError(f"Cannot open video file: {input_path}")

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS) or 25.0

        fourcc = cv2.VideoWriter_fourcc(*'.avi')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        if not out.isOpened():
            cap.release()
            raise IOError(f"Cannot open video writer for: {output_path}")

        mp_pose = mp.solutions.pose

        with mp_pose.Pose(static_image_mode=False) as pose:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(rgb_frame)

                if draw_skeleton:
                    frame = self.draw_pose(frame, results, all_landmarks)

                out.write(frame)

        cap.release()
        out.release()
        print(f"✅ Video processed and saved to {output_path}")






