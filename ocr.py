import cv2
import numpy as np
import pytesseract
import rospy
import subprocess
from std_msgs.msg import String

def detect_text_from_webcam():
    # Initialize ROS node and publisher
    rospy.init_node('text_detector', anonymous=True)
    text_pub = rospy.Publisher('detected_text', String, queue_size=10)
    
    # Open webcam
    cap = cv2.VideoCapture(0)  # Try different indices (0, 1, 2) if this doesn't work
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    while not rospy.is_shutdown():
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Failed to capture image")
            break
            
        # Rotate the image 180 degrees
        rotated = cv2.rotate(frame, cv2.ROTATE_180)
        
        # Convert to grayscale
        gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold
        _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
        
        # Enhance contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # Detect text
        text = pytesseract.image_to_string(thresh)
        
        # Print detected text for debugging
        print("Detected text:", text)
        
        # Check for "Ready to print"
        if "Print finish" in text:
            print("Printer is finished, robot can now remove the buildplate.")
            subprocess.call(["python3", "go.py"])  # Call go.py using subprocess.call()
            break  # Stop processing further frames
        
        # Display the processed frames
        cv2.imshow('Original (Rotated)', rotated)
        cv2.imshow('Threshold', thresh)
        cv2.imshow('Enhanced', enhanced)
        
        # Press q to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        detect_text_from_webcam()
    except rospy.ROSInterruptException:
        pass

