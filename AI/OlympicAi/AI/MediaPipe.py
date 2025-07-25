import os
import cv2
import mediapipe as mp
from moviepy.editor import VideoFileClip

class MediaPipeVideoProcessor:
    def __init__(self):
        self.pose = mp.solutions.pose.Pose()
        self.drawer = mp.solutions.drawing_utils
        
        
    def process_video(self, input_path: str, output_path: str):
        """
        Loads a video, adds MediaPipe pose skeleton to each frame, and saves the processed video.
        Args:
            input_path (str): Path to the input video file.
            output_path (str): Path to save the output video file.
        """

        # Open the input video
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            raise IOError(f"Cannot open video file: {input_path}")

        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS) or 25.0

        # Prepare the output video writer
        fourcc = cv2.VideoWriter_fourcc(*'.avi')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        if not out.isOpened():
            cap.release()
            raise IOError(f"Cannot open video writer for: {output_path}")

        # Initialize MediaPipe Pose
        mp_pose = mp.solutions.pose
        mp_drawing = mp.solutions.drawing_utils

        with mp_pose.Pose(static_image_mode=False) as pose:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break  # End of video

                # Convert frame to RGB for MediaPipe
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(rgb_frame)

                # Draw skeleton if landmarks are detected
                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(
                        frame,
                        results.pose_landmarks,
                        mp_pose.POSE_CONNECTIONS
                    )

                # Write the processed frame to output
                out.write(frame)

        # Release resources
        cap.release()
        out.release()
        print(f"✅ Video processed and saved to {output_path}")




def finalize_mp4(input_path: str, output_path: str):
    clip = VideoFileClip(input_path)
    clip.write_videofile(output_path, codec='libx264', audio=False)


