import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# model_path = "./models/pose_landmarker_full.task"

# BaseOptions = mp.tasks.BaseOptions
# PoseLandmarker = mp.tasks.vision.PoseLandmarker
# PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
# PoseLandmarkerResult = mp.tasks.vision.PoseLandmarkerResult
# VisionRunningMode = mp.tasks.vision.RunningMode

# # Create a pose landmarker instance with the live stream mode:
# def print_result(result: PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
#     print('pose landmarker result: {}'.format(result))

# options = PoseLandmarkerOptions(
#     base_options=BaseOptions(model_asset_path=model_path),
#     running_mode=VisionRunningMode.LIVE_STREAM,
#     result_callback=print_result)

# with PoseLandmarker.create_from_options(options) as landmarker:
#   # The landmarker is initialized. Use it here.
#   # ...

import cv2

# Open a connection to the webcam
cap = cv2.VideoCapture(0)  # Use 0 for the primary webcam

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If frame is read correctly, ret will be True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Display the resulting frame
    cv2.imshow('Live Webcam Feed', frame)

    # Press 'q' to exit the live feed window
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture when done
cap.release()
cv2.destroyAllWindows()