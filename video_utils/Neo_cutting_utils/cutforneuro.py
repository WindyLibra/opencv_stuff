import cv2
import os


def get_video_path_and_save_dir(video_path, config_file_path="config_video.txt"):
    """
  Reads video path and determines the save directory for images.

  Args:
      video_path: Path to the video file.
      config_file_path: Path to the optional configuration file containing the save directory.

  Returns:
      A tuple containing the video path and the save directory path.
  """
    if os.path.exists(config_file_path):
        with open(config_file_path, "r") as f:
            parts = f.split(".")
            save_dir = parts[0]
    else:
        # Extract directory and filename from video path
        video_dir, filename = os.path.split(video_path)
        save_dir = os.path.join(video_dir, filename.split(".")[0])

    # Create save directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    return video_path, save_dir


def extract_frames_and_resize(video_path, save_dir, resize_width=1280, resize_height=960, frame_skip=5):
    """
  Extracts frames from a video, resizes them (if needed), and saves them as images.

  Args:
      video_path: Path to the video file.
      save_dir: Path to the directory where images will be saved.
      resize_width: Width to resize frames to (default: 1280).
      resize_height: Height to resize frames to (default: 960).
      frame_skip: Number of frames to skip between saving images (default: 4).
  """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error opening video file:", video_path)
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    should_resize = frame_width > resize_width or frame_height > resize_height

    file_count = 1
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if file_count % (frame_skip + 1) == 1:  # Save every nth frame (starting from 1)
            print(f"Saving frame {file_count:04d}")
            filename = os.path.join(save_dir, f"{os.path.basename(video_path)}_1_{file_count:04d}.jpg")

            if should_resize:
                resized_frame = cv2.resize(frame, (resize_width, resize_height), interpolation=cv2.INTER_LINEAR)
                cv2.imwrite(filename, resized_frame)
            else:
                cv2.imwrite(filename, frame)

        file_count += 1

        key = cv2.waitKey(20)
        if key == ord('q') or key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


# Get video path and save directory
video_path, save_dir = get_video_path_and_save_dir("C:/Users/aram_/OneDrive/Documents/Videos for labeling/pushki_1_for_label.mp4")

# Extract frames and resize (optional)
extract_frames_and_resize(video_path, save_dir)

print("Finished processing video")
