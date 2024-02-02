# video-focus-tracking

# Pinout Map

| Pin                                                 | ESP32 | Comments                                       |
| --------------------------------------------------- | ----- | ---------------------------------------------- |
| VIN                                                 | 3.3V  | Power                                          |
| GND                                                 | GND   | Ground                                         |
| SCL                                                 | G22   | Item3.3                                        |
| SDA                                                 | G21   | Item3.4                                        |
| INT                                                 | G17   | Interrupt output, defaults to opendrain output |
| (tristate), 47 kΩ pullup resistor to IOVDD required |       |                                                |
| Lpin                                                | G16   | Comms enable. Drive this pin to logic 0 to     |
| disable the I2C comms when the device is in         |       |                                                |
| LP mode. Drive this pin to logic 1 to enable I2C    |       |                                                |
| comms in LP mode. Typically used when it is         |       |                                                |
| required to change the I2C adress in multidevice    |       |                                                |
| systems. A 47 kΩ pullup resis                       |       |                                                |
