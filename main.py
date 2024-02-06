import cv2
import time
import mediapipe as mp


def main():
    image_name = "image.jpg"
    capture_img(image_name)
    time.sleep(3)
    analyse_img(image_name)


def capture_img(image_name):
    # Initialize the camera
    cam = cv2.VideoCapture(0)

    # Check if the camera is opened successfully
    if not cam.isOpened():
        print("Error: Could not open the camera")
    else:
        # Add a  5-second delay for preparation
        time.sleep(5)

        # Capture a single frame from the camera
        ret, frame = cam.read()

        # Check if the frame was captured successfully
        if ret:
            # Display the captured frame
            cv2.imshow("Captured Image", frame)

            # Save the captured frame as 'output.jpg'
            cv2.imwrite(image_name, frame)

            # Wait for a key press and then close the image window
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("Error: Failed to capture the image")

    # Release the camera resource
    cam.release()


def analyse_img(image_name):
    mp_face_detection = mp.solutions.face_detection
    mp_drawing = mp.solutions.drawing_utils

    # Replace 'your_image.jpg' with the path to your image file
    image = cv2.imread(image_name)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with mp_face_detection.FaceDetection(
        min_detection_confidence=0.5
    ) as face_detection:
        results = face_detection.process(rgb_image)
        print(dir(results))
        print(results.detections)
        print(results.multi_face_landmarks)

        if results.detections:
            for detection in results.detections:
                mp_drawing.draw_detection(image, detection)

        cv2.imshow("MediaPipe Face Detection", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
