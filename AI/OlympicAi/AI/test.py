from MediaPipe import MediaPipeVideoProcessor

# Paths to input and output video files
input_video = "AI/clean_helland.mp4"      # Replace with your actual test video path
output_video = "clean_media.mp4"    # This will be created with skeleton overlay

# Create processor and run
processor = MediaPipeVideoProcessor()
processor.process_video(input_video, output_video)

print("Processing complete. Check:", output_video)
