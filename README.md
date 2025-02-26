# Automated 3D Print Removal System

This repository contains code for an automated system that monitors a 3D printer using a webcam, detects when a print is complete, and triggers an Arctos robotic arm to remove the build plate.

## Overview

The system consists of two main Python scripts:
- `ocr.py`: Uses computer vision and OCR to monitor the 3D printer's display
- `go.py`: Sends G-code commands to control the Arctos robotic arm

When the camera detects the text "Print finish" on the printer's display, it automatically executes the G-code to remove the build plate.

## Hardware Setup

This implementation uses:
- **3D Printer**: Bambulab P1P
- **Robotic Arm**: Arctos robotic arm
- A webcam positioned to view the P1P's display screen
- USB connection to the Arctos robotic arm
- Computer to run the monitoring software (Raspberry Pi or similar works well)

## Requirements

### Hardware
- A webcam positioned to view the Bambulab P1P's display screen
- Arctos robotic arm
- USB connection to the Arctos arm
- Computer to run the monitoring software (Raspberry Pi or similar works well)

### Software
- Python 3.6+
- OpenCV
- Tesseract OCR
- pySerial
- ROS (Robot Operating System) - basic setup
- G-code file for your specific build plate removal procedure

## Installation

1. Install Python dependencies:
```bash
pip install opencv-python numpy pytesseract pyserial rospython
```

2. Install Tesseract OCR:
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract

# Windows
# Download installer from https://github.com/UB-Mannheim/tesseract/wiki
```

3. Install ROS (follow instructions at http://wiki.ros.org/ROS/Installation)

4. Clone this repository:
```bash
git clone https://github.com/yourusername/automated-print-removal.git
cd automated-print-removal
```

5. Create a G-code file named `remove_buildplate.tap` with commands specific to your setup (see G-code Configuration section below).

## Configuration

### Webcam Setup
Ensure your webcam has a clear view of the Bambulab P1P's display. You may need to adjust the webcam position or update the rotation settings in `ocr.py` if the image is not oriented correctly.

### Serial Port Configuration
In `go.py`, update the default serial port and baud rate if necessary:

```python
def send_gcode(file_path, port='/dev/ttyUSB0', baudrate=115200):
```

For Windows users, the port will typically be `COM3` or similar.

### G-code Configuration
The `remove_buildplate.tap` file contains G-code commands for the Arctos robotic arm to remove the build plate from your Bambulab P1P printer. You will need to customize this file based on:

1. The relative positions of your Arctos arm and Bambulab P1P printer
2. The exact movements needed to safely remove the build plate

**Important Note**: The zero coordinate (origin) in the example G-code file is defined as the position where the Arctos robotic arm is about to pick up the build plate. All movements in the G-code should be relative to this position.

#### Example G-code Structure
```
G90 ; Set absolute positioning
G0 Z10 ; Raise arm to safe height
G0 X0 Y0 ; Move to zero position (ready to pick buildplate)
G0 Z0 ; Lower to buildplate
; Commands to grip the buildplate
M97 B-10 T0.8 ; Raise with buildplate
G0 X100 Y50 ; Move to deposit location
; Commands to release the buildplate
M97 B110 T0.8 ; Raise after releasing
G0 X0 Y0 Z10 ; Return to home position
```

## Usage

1. Ensure your Bambulab P1P printer and Arctos robotic arm are properly connected and powered on.

2. Start the monitoring system:
```bash
python ocr.py
```

3. Start your 3D print on the Bambulab P1P as normal.

4. The system will monitor the printer display. When it detects "Print finish", it will automatically execute the G-code to control the Arctos arm to remove the build plate.

5. To stop the monitoring at any time, press `q` while the camera windows are in focus.

## Customization

### Modifying OCR Text Detection for Bambulab P1P
The Bambulab P1P displays "Print finish" when a print is complete. If your firmware shows different text, modify this line in `ocr.py`:

```python
if "Print finish" in text:
```

### Camera Adjustment
If your camera isn't working or you have multiple cameras, try changing the camera index:

```python
cap = cv2.VideoCapture(0)  # Try 1, 2, etc.
```

### Adjusting for Different Printer Positions
If you reposition your Bambulab P1P printer or Arctos arm, you'll need to update the coordinates in your `remove_buildplate.tap` file. Consider using a teach pendant or manual control to find the appropriate coordinates before updating the G-code.

## Troubleshooting

### OCR Not Detecting "Print finish" Text
- Ensure the webcam has a clear, well-lit view of the Bambulab P1P's display
- Adjust the threshold values in the image processing steps
- The P1P's display may have glare - adjust camera angle to minimize this

### Arctos Arm Not Responding
- Check serial connection and port settings
- Verify the G-code file contains valid commands for the Arctos arm
- Ensure you have proper permissions to access the serial port
- Verify the arm is powered on and in the correct operating mode

### Arm Movement Issues
- Double-check that your zero position is correctly set where the arm is about to pick the buildplate
- Ensure the G-code coordinates match your physical setup
- Start with slow movements (lower feed rates) to test the removal process

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
