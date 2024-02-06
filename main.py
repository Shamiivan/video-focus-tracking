import cv2
import mediapipe as mp
import numpy as np
import serial
import time

UNCERTAINTY = 50000
THRESHOLD = 300000  # Lower bound considering the uncertainty
MIN = THRESHOLD - UNCERTAINTY
MAX = THRESHOLD + UNCERTAINTY


def get_inverse_diff(value, reference):
    diff = abs(value - reference)
    if diff == 0:
        return 0
    else:
        return (1 - diff / THRESHOLD) * 100


# function to check if
def is_3d(depth: int) -> str:
    if depth >= MAX:
        return "100% detecting a 3D face"
    elif depth <= MIN:
        return "100 % detecting a 2D Face"
    elif (depth >= THRESHOLD) and depth < MAX:
        diff = get_inverse_diff(depth, MAX)
        return f"Not sure but {diff}% it's 3D face"
    elif (depth < THRESHOLD) and (depth > MIN):
        diff = get_inverse_diff(depth, MIN)
        return f"Not sure but {diff}% it a 2D face"
    else:
        return " "


# Initialize MediaPipe Face Mesh.
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

# Initialize serial communication.
serial_port = "/dev/cu.usbserial-0001"  # Adjust this according to your system.
baud_rate = 115200
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# Start capturing video.
cap = cv2.VideoCapture(0)
measurement = 1

with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
) as face_mesh:
    while cap.isOpened():
        display_text = "Checking"
        # Video frame processing.
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image)

        # Draw the face mesh annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                display_text = is_3d(measurement)
                # landmark_array = np.array(
                #     [
                #         (landmark.x, landmark.y, landmark.z)
                #         for landmark in face_landmarks.landmark
                #     ]
                # )
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style(),
                )

        flipped_image = cv2.flip(image, 1)  # Flip the image for a mirror effect

        cv2.putText(
            flipped_image,
            display_text,
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 0),
            2,
            cv2.LINE_AA,
        )
        cv2.imshow("MediaPipe Face Mesh", flipped_image)

        # Serial communication processing.
        if ser.in_waiting > 0:
            line = ser.readline().decode("utf-8").rstrip()
            measurement = int(line)
            print(f"Serial data: {line}")

        # Break the loop if 'ESC' is pressed.
        if cv2.waitKey(5) & 0xFF == 27:
            break

# Clean up
cap.release()
cv2.destroyAllWindows()
ser.close()
