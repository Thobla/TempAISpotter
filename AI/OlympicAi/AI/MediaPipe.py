import os
import cv2
import mediapipe as mp
from moviepy.editor import VideoFileClip

class MediaPipeVideoProcessor:
    def __init__(self):
        self.pose = mp.solutions.pose.Pose()
        self.drawer = mp.solutions.drawing_utils

    def process_video(self, input_path: str, output_path: str):
        temp_path = "temp_output.mp4"  # Intermediate OpenCV output

        cap = cv2.VideoCapture(input_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS) or 25.0

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(temp_path, fourcc, fps, (width, height))

        if not out.isOpened():
            raise IOError(f"Failed to open VideoWriter for {temp_path}")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame.shape[1] != width or frame.shape[0] != height:
                frame = cv2.resize(frame, (width, height))

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(rgb_frame)

            if results.pose_landmarks:
                self.drawer.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp.solutions.pose.POSE_CONNECTIONS
                )

            out.write(frame)

        cap.release()
        out.release()

        # Finalize with MoviePy to ensure platform compatibility
        finalize_mp4(temp_path, output_path)

        # Clean up temp file
        os.remove(temp_path)

        print(f"✅ Video finalized and saved to {output_path}")


def finalize_mp4(input_path: str, output_path: str):
    clip = VideoFileClip(input_path)
    clip.write_videofile(output_path, codec='libx264', audio=False)




# Old version
"""import cv2
import mediapipe as mp

class MediaPipeVideoProcessor:
    def __init__(self):
        self.pose = mp.solutions.pose.Pose()
        self.drawer = mp.solutions.drawing_utils

    def process_video(self, input_path: str, output_path: str):
        cap = cv2.VideoCapture(input_path)
        width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps    = cap.get(cv2.CAP_PROP_FPS)

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Convert to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(rgb_frame)

            # Draw pose landmarks
            if results.pose_landmarks:
                self.drawer.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp.solutions.pose.POSE_CONNECTIONS
                )

            out.write(frame)

        cap.release()
        out.release()
"""