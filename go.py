import serial
import time

def send_gcode(file_path, port='/dev/ttyUSB0', baudrate=115200):
    try:
        # Open serial connection
        with serial.Serial(port, baudrate, timeout=1) as ser:
            print(f"Connected to {port} at {baudrate} baud")
            
            # Wake up GRBL
            ser.write(b'\r\n')
            time.sleep(2)
            ser.flushInput()

            # Open the G-code file
            with open(file_path, 'r') as file:
                for line in file:
                    gcode_cmd = line.strip()
                    if gcode_cmd:
                        ser.write((gcode_cmd + '\n').encode())  # Send command
                        print(f"Sent: {gcode_cmd}")

                        # Wait for 'ok' response before sending the next command
                        while True:
                            response = ser.readline().decode().strip()
                            if response == "ok":
                                break
                            elif response:
                                print(f"GRBL: {response}")

                        time.sleep(0.1)  # Add small delay

            print("G-code sending completed.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_gcode('remove_buildplate.tap')

