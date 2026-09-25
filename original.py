import imageio
import numpy as np

# Modify the following parameters to reduce the video conversion time
resolution_scale = 0.4 # reduce the resolution of the video, e.g. 0.4 mean reducing from 100% to 40%
fps_scale = 0.3 # reduce the frame per second, e.g. 0.30 mean reducing from 100% to 30%

# Function to convert a color frame to grayscale
def rgb_to_gray(frame):
    height, width, _ = frame.shape
    gray_frame = np.zeros((height, width), dtype=np.uint8)
    
    for i in range(height):
        for j in range(width):
            # Calculate grayscale value using the luminance formula
            gray_pixel = 0.2989 * frame[i, j, 0] + 0.5870 * frame[i, j, 1] + 0.1140 * frame[i, j, 2]
            gray_frame[i, j] = int(gray_pixel)
    
    return gray_frame

# Implement your function here
def my_function(frame):
    # For example
    new_frame = rgb_to_gray(frame)

    return new_frame

# Input video file path
input_video_path = 'example_input.mp4'

# Output video file path
output_video_path = 'example_output.mp4'

# Create a reader and writer object using imageio
reader = imageio.get_reader(input_video_path)
fps = reader.get_meta_data()['fps']
frame_size = reader.get_meta_data()['size']

# Calculate the desired fps and resolution
target_fps = int(fps * fps_scale)
target_resolution = (int(frame_size[0] * resolution_scale), int(frame_size[1] * resolution_scale))

# Calculate the target number of frames to skip for FPS reduction
frame_skip = int(fps / target_fps)

# Calculate the scaling factors for resolution reduction
width_scale = frame_size[0] // target_resolution[0]
height_scale = frame_size[1] // target_resolution[1]

# Get video writer object
writer = imageio.get_writer(output_video_path, fps=target_fps)

try:
    frame_count = 0
    for frame in reader:
        # Apply FPS reduction by skipping frames
        if frame_count % frame_skip == 0:
            print("Converting Frame #" + str(frame_count+1))
            # Resize the frame to the target resolution
            resized_frame = frame[::height_scale, ::width_scale, :]
            
            # Convert the color frame to grayscale
            gray_frame = my_function(resized_frame)
            
            # Write the grayscale frame to the output video
            writer.append_data(gray_frame)
        
        frame_count += 1
finally:
    writer.close()

    