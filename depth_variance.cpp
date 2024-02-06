#include <Wire.h>

#include <SparkFun_VL53L5CX_Library.h>

SparkFun_VL53L5CX myImager;
VL53L5CX_ResultsData
    measurementData; // Result data class structure, 1356 byes of RAM

int imageResolution = 0; // Used to pretty print output
int imageWidth = 0;      // Used to pretty print output

void setup() {
  Serial.begin(115200);
  Serial.println("SparkFun VL53L5CX Imager Example");

  Wire.begin();          // This resets to 100kHz I2C
  Wire.setClock(400000); // Sensor has max I2C freq of 400kHz

  Serial.println(
      "Initializing sensor board. This can take up to 10s. Please wait.");
  if (myImager.begin() == false) {
    Serial.println(F("Sensor not found "));
    while (1)
      ;
  }

  myImager.setResolution(8 * 8); // Enable all 64 pads

  imageResolution = myImager.getResolution(); // Query sensor for current
                                              // resolution - either 4x4 or 8x8
  imageWidth = sqrt(imageResolution); // Calculate printing width

  myImager.startRanging();
}

void loop() {
  // Poll sensor for new data
  if (myImager.isDataReady() == true) {
    if (myImager.getRangingData(
            &measurementData)) // Read distance data into array
    {
      long sum = 0;              // For calculating mean
      long sumSqDiff = 0;        // For calculating variance
      int validMeasurements = 0; // To only consider valid measurements

      // First, compute the sum of all valid distances
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
        long mean = sum / validMeasurements;

        // Next, compute the sum of squared differences from the mean
        for (int i = 0; i < imageResolution; i++) {
          if (measurementData.distance_mm[i] >
              0) // Assuming 0 is invalid measurement
          {
            long diff = measurementData.distance_mm[i] - mean;
            sumSqDiff += diff * diff;
          }
        }

        // Finally, calculate variance
        long variance = sumSqDiff / validMeasurements;

        Serial.print("Depth Variance: ");
        Serial.println(variance);
      } else {
        Serial.println("No valid measurements for variance calculation.");
      }

      // Optional: Continue to print the distance matrix as before
    }
  }

  delay(5); // Small delay between polling
}
