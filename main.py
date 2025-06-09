import numpy as np
import cv2
import os
from tracker import *

# Initialize Tracker
tracker = ObjectTracker()

# Location of the first frame
firstframe_path = r'C:\obj_detection\ABANDONED OBJECT DETECTION\FrameNo0.png'
firstframe = cv2.imread(firstframe_path)
if firstframe is None:
    print(f"Error: Could not read the first frame image at {firstframe_path}")
    exit()

firstframe_gray = cv2.cvtColor(firstframe, cv2.COLOR_BGR2GRAY)
firstframe_blur = cv2.GaussianBlur(firstframe_gray, (3, 3), 0)

# List of video file paths to process
video_files = [
    r'C:\obj_detection\ABANDONED OBJECT DETECTION\input video.mp4',
    
]

# Loop through each video
for file_path in video_files:
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"Error: File does not exist at path: {file_path}")
        continue

    # Open the video file
    cap = cv2.VideoCapture(file_path)

    # Check if the video was opened successfully
    if not cap.isOpened():
        print(f"Error: Unable to open video file at path: {file_path}")
        continue
    else:
        print(f"Processing video: {file_path}")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Resize frame to match the size of the first frame
            frame_resized = cv2.resize(frame, (firstframe.shape[1], firstframe.shape[0]))

            frame_gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
            frame_blur = cv2.GaussianBlur(frame_gray, (3, 3), 0)

            # Find difference between first frame and current frame
            frame_diff = cv2.absdiff(firstframe_blur, frame_blur)

            # Canny Edge Detection
            edged = cv2.Canny(frame_diff, 5, 200)

            kernel = np.ones((10, 10), np.uint8)
            thresh = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel, iterations=2)

            # Find contours of all detected objects
            cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            detections = []
            for c in cnts:
                contourArea = cv2.contourArea(c)
                if 50 < contourArea < 10000:
                    (x, y, w, h) = cv2.boundingRect(c)
                    detections.append([x, y, w, h])

            # Update the tracker and get abandoned objects
            _, abandoned_objects = tracker.update(detections)

            # Draw rectangle and id over all abandoned objects
            for objects in abandoned_objects:
                _, x2, y2, w2, h2, _ = objects
                cv2.putText(frame_resized, "Suspicious object detected", (x2, y2 - 10), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 0, 255), 2)
                cv2.rectangle(frame_resized, (x2, y2), (x2 + w2, y2 + h2), (0, 0, 255), 2)

            # Show the frame
            cv2.imshow('main', frame_resized)

            # Break on 'q' key press
            if cv2.waitKey(15) == ord('q'):
                break

        cap.release()

# Destroy all OpenCV windows after processing all videos
cv2.destroyAllWindows()
