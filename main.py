import cv2
import mediapipe as mp
import numpy as np
import serial
import time
from typing import Tuple

# Constants
UNCERTAINTY: int = 50000
THRESHOLD: int = 300000
MIN: int = THRESHOLD - UNCERTAINTY
MAX: int = THRESHOLD + UNCERTAINTY
SERIAL_PORT: str = "/dev/cu.usbserial-0001"
BAUD_RATE: int = 115200


def get_inverse_diff(value: int, reference: int) -> float:
    """Calculate the inverse difference relative to a threshold."""
    diff: int = abs(value - reference)
    return 0.0 if diff == 0 else (1 - diff / THRESHOLD) * 100


def determine_face_depth(depth: int) -> str:
    """Determine whether a face appears to be 2D or 3D based on its depth."""
    if depth >= MAX:
        return "100% detecting a 3D face"
    elif depth <= MIN:
        return "100% detecting a 2D Face"
    elif MIN < depth < MAX:
        reference = MAX if depth >= THRESHOLD else MIN
        diff = get_inverse_diff(depth, reference)
        return f"Not sure but {diff}% likely to be {'3D' if depth >= THRESHOLD else '2D'} face"
    return ""


def initialize_media_pipe() -> (
    Tuple[
        mp.solutions.drawing_utils,
        mp.solutions.drawing_styles,
        mp.solutions.face_mesh.FaceMesh,
        mp.solutions.drawing_utils.DrawingSpec,
    ]
):
    """Initialize MediaPipe Face Mesh."""
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_face_mesh = mp.solutions.face_mesh
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    return mp_drawing, mp_drawing_styles, mp_face_mesh, drawing_spec


def initialize_serial_communication() -> serial.Serial:
    """Initialize serial communication."""
    return serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)


def main() -> None:
    mp_drawing, mp_drawing_styles, mp_face_mesh, drawing_spec = initialize_media_pipe()
    ser = initialize_serial_communication()
    cap = cv2.VideoCapture(0)
    measurement: int = 1

    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as face_mesh:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            display_text: str = "Checking"

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    display_text = determine_face_depth(measurement)
                    mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style(),
                    )

            flipped_image = cv2.flip(image, 1)
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

            if ser.in_waiting > 0:
                measurement = int(ser.readline().decode("utf-8").rstrip())
                print(f"Serial data: {measurement}")

            if cv2.waitKey(5) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()
    ser.close()


if __name__ == "__main__":
    main()
