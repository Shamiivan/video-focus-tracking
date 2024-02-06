import serial
import time

serial_port = "/dev/cu.usbserial-0001"
baud_rate = 115200  

try:
    with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode("utf-8").rstrip()
                print(line)
            time.sleep(0.01) 
except serial.SerialException as e:
    print(f"Error opening serial port {serial_port}: {e}")
except KeyboardInterrupt:
    print("Program terminated!")
