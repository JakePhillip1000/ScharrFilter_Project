import imageio
import numpy as np
#from scipy.signal import convolve2d

# Modify the following parameters to reduce the video conversion time
resolution_scale = 0.4  # Reduce the resolution of the video
fps_scale = 1  # Reduce the frames per second

# Function to convert a color frame to grayscale
def rgb_to_gray(frame):
    return np.dot(frame[..., :3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)

# Create the Scharr function
def scharr(image):
    # The scharr operator (scharr kernel)
    vertical = np.array([
        [-3, 0, 3],
        [-10, 0, 10],
        [-3, 0, 3]
    ])
    
    horizontal = np.array([
        [-3, -10, -3],
        [0, 0, 0],
        [3, 10, 3]
    ])
    
    # Get image dimensions
    height, width = image.shape
    
    # Initialize output image, make all arrays zeros
    output_image = np.zeros((height, width))
    
    # Apply Scharr kernels, i = height, j = width
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            region = image[i-1:i+2, j-1:j+2] # specify the region of the image that will be filtered
            grad_x = np.sum(region * vertical)
            grad_y = np.sum(region * horizontal)
            magnitude = np.sqrt(grad_x**2 + grad_y**2)
            output_image[i, j] = np.clip(magnitude, 0, 255) # the magnitude of the graient should be 0-255
    
    # return out as a 8 bit integer values from 0-255
    return output_image.astype(np.uint8) # uint8 holds value 0-255

# Input video file path
input_video_path = 'videos/SAO.mp4'

# Output video file path
output_video_path = 'Processed_video/SAO_processed.mp4'

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
            
            # Apply the Scharr filter and write the scharr filter
            scharr_frame = scharr(gray_frame)
            writer.append_data(scharr_frame)
        
        frame_count += 1
finally:
    writer.close()
