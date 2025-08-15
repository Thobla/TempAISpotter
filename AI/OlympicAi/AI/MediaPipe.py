import os
import cv2
import numpy as np
import mediapipe as mp
from AI.utils import *
from mediapipe.python.solutions.pose import PoseLandmark



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
        
        # Draws degrees at specified joints if calculate_angle is True    
        if calculate_angle:
            frame = self.draw_angle(frame, results)
        
        return frame


    def draw_angle(self, frame, results, joint_names=None):
        """
        Draws the angle at specified joints on the frame.
        Args:
            frame: The image frame.
            results: The MediaPipe pose results.
            joint_names: List of joint names to draw angles for (e.g., ["right_knee", "left_knee"]).
        """
        if joint_names is None:
            joint_names = ["right_knee", "left_knee"]  # Default to knees

        if not results.pose_landmarks:
            return frame

        landmarks = results.pose_landmarks.landmark
        h, w = frame.shape[:2]
        colors = {
            "right_knee": (255, 0, 0),
            "left_knee": (0, 0, 255),
            # Add more colors for other joints if needed
        }

        for joint in joint_names:
            try:
                hip, knee, ankle = get_joint_coords(landmarks, joint)
                angle = calculate_angle(hip, knee, ankle)
                anatomical_angle = 180 - angle
                knee_px = (
                    int(landmarks[JOINTS[joint]["knee"]].x * w),
                    int(landmarks[JOINTS[joint]["knee"]].y * h)
                )
                cv2.putText(
                    frame,
                    f"{int(anatomical_angle)}",
                    knee_px,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    colors.get(joint, (0, 255, 0)),
                    2,
                    cv2.LINE_AA
                )
            except Exception:
                pass  # Optionally log or print(e)
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
                    frame = self.draw_pose(frame, results, all_landmarks, calculate_angle)

                out.write(frame)

        cap.release()
        out.release()
        print(f"✅ Video processed and saved to {output_path}")


    def verdict(self, path:str):
        """
        Processes a video file and returns a verdict based on the pose analysis.
        Args:
            input_path (str): Path to the input video file.
        Returns:
            str: Verdict based on the analysis.
        """
        #output_path = input_path.replace(".mp4", "_processed.mp4")
        #self.process_video(input_path, output_path, all_landmarks=True, draw_skeleton=True, calculate_angle=True)
        verdict = {"video": "id",
                   "path": path,
                   "verdict": "Bad",
                   "Reason": "Knee angle too high"}
        return verdict

