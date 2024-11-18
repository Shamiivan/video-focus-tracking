# Project Overview

The core challenge addressed by this project is the accurate classification of
objects or scenes as 2D or 3D faces on depth measurements.

### Problem

Mediapipe's API lacks the capability to distinguish between a 3D face and an
image of a face(2D). This project aims to address and resolve this limitation.

### High Level Breakdown of the Solution

To distinguish between 2D and 3D faces, I employed a Time of Flight (ToF) sensor
connected to an ESP32 microcontroller. This sensor captures depth information
across a 64-point grid (8 rows by 8 columns), allowing for detailed analysis of
the scene. The ESP32 processes this data to calculate the variance among the
measured points. A higher variance suggests a 3D scene due to the varying
distances of object parts from the sensor, while a lower variance indicates a
flat, 2D surface with more uniform distance measurements.

This depth data is then sent to a computer running a face detection program.
When a face is detected, the program analyzes the variance in depth
measurements. Based on predefined thresholds, it determines the dimensionality
of the face—whether it is 2D or 3D—taking into account the proximity of objects
to enhance the accuracy of its assessment.

## ESP32 Pinout Map

For interfacing the ESP32 with the ToF sensor, the following pinout map is used:

| Pin  | ESP32 |
| ---- | ----- |
| VIN  | 3.3V  |
| GND  | GND   |
| SCL  | G22   |
| SDA  | G21   |
| INT  | G17   |
| Lpin | G16   |

### Future Directions

Future exploration might delve into leveraging the variance in depth
measurements more extensively to refine the assessment process, potentially
incorporating probabilistic models for enhanced accuracy.
