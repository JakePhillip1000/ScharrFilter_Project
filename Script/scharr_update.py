# This is the faster version of processed
import imageio
import numpy as np
from scipy.signal import convolve2d

# Modify the following parameters to reduce the video conversion time
resolution_scale = 1  # Reduce the resolution of the video
fps_scale = 1  # Reduce the frames per second

# Function to convert a color frame to grayscale
def rgb_to_gray(frame):
    return np.dot(frame[..., :3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)

# Create the Scharr function using convolution
def scharr(image):
    vertical = np.array([
        [-3, 0, 3],
        [-10, 0, 10],
        [-3, 0, 3]
    ], dtype=np.float32)
    
    horizontal = np.array([
        [-3, -10, -3],
        [0, 0, 0],
        [3, 10, 3]
    ], dtype=np.float32)

    # Processed faster using covolution
    grad_x = convolve2d(image, vertical, mode="same", boundary="wrap")
    grad_y = convolve2d(image, horizontal, mode="same", boundary="wrap")
    magnitude = np.sqrt(grad_x**2 + grad_y**2)
    
    return np.clip(magnitude, 0, 255).astype(np.uint8)

# Input video file path
input_video_path = 'videos/mathfantasy.mp4'

# Output video file path
output_video_path = 'Processed_video/mathfantasy_processed.mp4'

# Create a reader and writer object using imageio
reader = imageio.get_reader(input_video_path)
fps = reader.get_meta_data()['fps']
frame_size = reader.get_meta_data()['size']

# Calculate the desired fps and resolution
target_fps = int(fps * fps_scale)
target_resolution = (int(frame_size[0] * resolution_scale), int(frame_size[1] * resolution_scale))

# Calculate the target number of frames to skip for FPS reduction
frame_skip = int(fps / target_fps)

# Get video writer object
writer = imageio.get_writer(output_video_path, fps=target_fps)

try:
    frame_count = 0
    for frame in reader:
        # Apply FPS reduction by skipping frames
        if frame_count % frame_skip == 0:
            print(f"Processing Frame #{frame_count + 1}")
            
            # Resize the frame to the target resolution
            resized_frame = frame[::int(1/resolution_scale), ::int(1/resolution_scale), :]

            # Convert the color grayscale
            gray_frame = rgb_to_gray(resized_frame)

            # Apply the Scharr filter and implement to scharr using functions
            scharr_frame = scharr(gray_frame)
            writer.append_data(scharr_frame)
        
        frame_count += 1
finally:
    writer.close()
