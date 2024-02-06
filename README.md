# Anti - spoofing

# ESP32 Pinout Map

### Analysis Approach:

t- **Uniformity**: All measurements within each experiment are consistent,
except for "Experiment 3: 3D -- close," which shows variability. This variance
is expected in 3D environments due to depth differences.

- **Comparison**:
  - **2D Experiments**: The "2D -- close" measurements are significantly lower
    than any other readings, suggesting minimal distance or detection close to
    the sensor. The "2D -- far" in the context seems to be mistakenly mixed,
    with one set showing very high values (similar to "Experiment 2: 2D -- far"
    with values around 398970) indicating a maximum range detection and another
    set with moderate values (similar to "Experiment 1: 2D -- far" with values
    around 205837), possibly indicating a mid-range detection.
  - **3D Experiments**: "3D -- close" readings vary, indicating depth perception
    capability of the sensor. "3D -- far" shows high uniform values, indicating
    the sensor's ability to detect objects at a distance with less variance than
    at closer ranges.

### Table of Results

| Experiment                          | Condition | Measurement Values Range | Number of Measurements | Observation                                   |
| ----------------------------------- | --------- | ------------------------ | ---------------------- | --------------------------------------------- |
| 1: 2D -- close                      | Close     | 349                      | 100                    | Minimal detection range.                      |
| 2: 2D -- far (mixed up with 3D far) | Far       | 398970                   | 100                    | Maximum detection range or sensor's limit.    |
| 3: 3D -- close                      | Close     | 180946 to 272364         | 44                     | Variability indicating depth perception.      |
| 1: 2D -- far                        | Far       | 205837                   | 100                    | Moderate detection range.                     |
| 4: 3D -- far                        | Far       | 434660                   | 100                    | High uniform values indicating far detection. |

### Observations:

- **2D Close vs. 2D Far**: The stark difference between the 2D close and far
  readings (considering the corrected 2D far experiment with consistent 205837
  readings) suggests that the sensor can distinguish between proximity levels in
  a controlled (flat) environment.
- **3D Close Variability**: The variability in the "3D -- close" experiment
  reflects the sensor's response to different depth levels within the 3D
  object's range, showcasing the sensor's utility in depth-sensitive
  applications.
- **Maximum Range Detection**: The high uniform readings in "2D -- far"
  (mistakenly mixed but likely intended as a distinct measurement set indicating
  far detection) and "3D -- far" experiments suggest the sensor's maximum range
  or detection limit under the test conditions.

### Conclusion:

# The data analysis demonstrates the sensor's capability to differentiate between 2D and 3D objects at various distances. The variance in 3D close measurements highlights the sensor's potential in applications requiring depth detection, such as navigation aids, obstacle detection, and interactive installations. The uniformity in other measurements confirms the sensor's reliability under less complex conditions. Further experimentation could explore the sensor's performance across different materials, lighting conditions, and angles to fully leverage its capabilities in real-world applications.

# Anti-spoofing

# Esp 32 Pinout Map

| Pin  | ESP32 |
| ---- | ----- |
| VIN  | 3.3V  |
| GND  | GND   |
| SCL  | G22   |
| SDA  | G21   |
| INT  | G17   |
| Lpin | G16   |

> 1a5266a8a97f4bdd7d3d3b1d66f63b1213bafacd
