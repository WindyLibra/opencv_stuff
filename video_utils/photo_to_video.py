import cv2
import os
from natsort import natsorted

# Directory containing your images
image_folder = r'C:\Users\aram_\OneDrive\Documents\all_jpg'
video_name = r'C:\Users\aram_\OneDrive\Рабочий стол\Tracking_Corners.mp4'

# Get the list of images in the directory
images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]

# Sort the images by filename
images = natsorted(images)

# Read the first image to get its shape
first_image_path = os.path.join(image_folder, images[0])
frame = cv2.imread(first_image_path)

# Check if the frame is successfully read
if frame is None:
    print(f"Failed to read the image: {first_image_path}")
    exit()

# Get the shape of the frame
height, width, layers = frame.shape

# Define the VideoWriter object
video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), 40, (width, height))

# Iterate through the images and add them to the video
for image in images:
    img_path = os.path.join(image_folder, image)
    img_frame = cv2.imread(img_path)
    if img_frame is not None:
        video.write(img_frame)
    else:
        print(f"Failed to read the image: {img_path}")

# Release the VideoWriter object
video.release()

# Optionally, display a message once the video is created
print("Video created successfully!")
