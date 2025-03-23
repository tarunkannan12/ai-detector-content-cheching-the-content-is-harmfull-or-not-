import cv2
import os

# List of vulgar words (can be expanded)
vulgar_words = ['badword1', 'badword2', 'badword3']

def analyze_text_for_vulgarity(text):
    """Simple function to check for vulgarity in text."""
    text = text.lower()
    for word in vulgar_words:
        if word in text:
            return True  # Found vulgar word
    return False  # No vulgarity detected

def extract_frames(video_path, frame_rate=30):
    """Extract frames from a video file at a specified frame rate."""
    video_capture = cv2.VideoCapture(video_path)
    frame_count = 0
    frames = []
    
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        if frame_count % frame_rate == 0:
            frame_filename = f"frame_{frame_count}.jpg"
            cv2.imwrite(frame_filename, frame)
            frames.append(frame_filename)
        frame_count += 1

    video_capture.release()
    return frames

def analyze_image_for_vulgarity(image_path):
    """Simple function to check if the image is explicit (e.g., very bright skin tone)."""
    # For demonstration, we will just look at the average color intensity.
    # A real model would be far more advanced.
    image = cv2.imread(image_path)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define a simple color threshold for detecting skin tones
    lower_skin = (0, 30, 60)
    upper_skin = (20, 150, 255)
    mask = cv2.inRange(hsv_image, lower_skin, upper_skin)
    skin_area = cv2.countNonZero(mask)

    if skin_area > 10000:  # If there's a significant amount of skin tone in the frame
        return True
    return False

def process_video_and_text(video_path, text_content=None):
    """Process video frames and text content for vulgarity detection."""
    print("Processing video frames...")
    frames = extract_frames(video_path, frame_rate=30)

    for frame in frames:
        print(f"Analyzing frame: {frame}")
        if analyze_image_for_vulgarity(frame):
            print(f"Vulgar image detected in frame: {frame}")
        else:
            print(f"Frame {frame} is clean.")

    if text_content:
        print("Analyzing text content...")
        if analyze_text_for_vulgarity(text_content):
            print("Vulgar content detected in text!")
        else:
            print("Text content is clean.")

# Example usage
video_path = "path_to_video.mp4"  # Replace with your video path
text_content = "This is an example text with badword1 and some other content."  # Optional text from the video

process_video_and_text(video_path, text_content)
