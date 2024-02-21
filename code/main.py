import RPi.GPIO as GPIO
import time
from picamera import PiCamera

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Button 1
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Button 2

# Initialize camera
camera = PiCamera()

def take_picture(channel):
    # Take a picture
    camera.capture('/home/pi/image.jpg')
    print("Picture Taken")

def refresh_camera(channel):
    # Stop and start the preview for refresh
    camera.stop_preview()
    camera.start_preview()
    print("Camera Refreshed")

# Setup event detection
GPIO.add_event_detect(17, GPIO.RISING, callback=take_picture, bouncetime=300)
GPIO.add_event_detect(27, GPIO.RISING, callback=refresh_camera, bouncetime=300)

# Start camera preview
camera.start_preview()

# Keep the program running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    camera.stop_preview()
    GPIO.cleanup()

