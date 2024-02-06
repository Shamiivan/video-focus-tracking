#include <Wire.h>

#include <SparkFun_VL53L5CX_Library.h> //http://librarymanager/All#SparkFun_VL53L5CX

SparkFun_VL53L5CX myImager;
VL53L5CX_ResultsData
    measurementData; // Result data class structure, 1356 byes of RAM

int imageResolution = 0; // Used to pretty print output
int imageWidth = 0;      // Used to pretty print output

void setup() {
  Serial.begin(115200);
  Wire.begin();          // resets to 100kHz I2C
  Wire.setClock(400000); // Sensor has max I2C freq of 400kHz

  Serial.println("Initializing sensor board.");
  if (myImager.begin() == false) {
    Serial.println(F("Sensor not found "));
    while (1)
      ;
  }

  myImager.setResolution(8 * 8); // Enable all 64 pads

  imageResolution = myImager.getResolution(); // Query sensor for current
                                              // resolution - either 4x4 or 8x8
  imageWidth = sqrt(imageResolution);         // Calculate printing width

  myImager.startRanging();
}

void loop() {
  static int printCounter = 0; // Counter to control the frequency of Serial
                               // prints, to get optimization

  // Poll sensor for new data
  if (myImager.isDataReady() == true) {
    if (myImager.getRangingData(
            &measurementData)) // Read distance data into array
    {
      int sum = 0;               // Use int for sum
      int validMeasurements = 0; // To only consider valid measurements
      int mean = 0;

      // Compute the sum of all valid distances
      for (int i = 0; i < imageResolution; i++) {
        if (measurementData.distance_mm[i] >
            0) // Assuming 0 is invalid measurement
        {
          sum += measurementData.distance_mm[i];
          validMeasurements++;
        }
      }

      // Calculate mean if we have valid measurements
      if (validMeasurements > 0) {
        mean = sum / validMeasurements;
      }

      int sumSqDiff = 0; // Use int for squared differences sum

      // Compute the sum of squared differences from the mean
      for (int i = 0; i < imageResolution; i++) {
        if (measurementData.distance_mm[i] > 0) {
          int diff = measurementData.distance_mm[i] -
                     mean;          // Calculate difference from mean
          sumSqDiff += diff * diff; // Sum of squared differences
        }
      }

      // Calculate and print variance every 10th measurement to reduce Serial
      // load
      if (++printCounter >= 1) {
        printCounter = 0; // Reset counter

        if (validMeasurements > 0) {
          int variance = sumSqDiff / validMeasurements; // Calculate variance
          Serial.print("Depth Variance: ");
          Serial.println(variance);
        } else {
          Serial.println("No valid measurements for variance calculation.");
        }
      }
    }
  }

  delay(5);
}
