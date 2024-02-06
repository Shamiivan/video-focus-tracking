import cv2
import mediapipe as mp
import numpy as np
import serial
import time

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

# Initialize a counter for the measurements
measurement_count = 0

# Open a file to write the measurements
with open("measurements.txt", "a") as file:
    line = ""
    experiment_header = "Experiment 1: 3D  -- far\n"
    file.write(experiment_header)

    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as face_mesh:
        while cap.isOpened() and measurement_count < 100:
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
                    landmark_array = np.array(
                        [
                            (landmark.x, landmark.y, landmark.z)
                            for landmark in face_landmarks.landmark
                        ]
                    )
                    # Optionally print landmark_array or handle it according to your needs.
                    # print(landmark_array)
                    mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style(),
                    )
            cv2.imshow("MediaPipe Face Mesh", cv2.flip(image, 1))

            # Serial communication processing.
            if ser.in_waiting > 0 and measurement_count < 50000:
                line = ser.readline().decode("utf-8").rstrip()
                print(f"Serial data: {line}")
                file.write(f"{line}\n")
                measurement_count += 1

            # Break the loop if 'ESC' is pressed.
            if cv2.waitKey(5) & 0xFF == 27:
                break

# Clean up
cap.release()
cv2.destroyAllWindows()
ser.close()
