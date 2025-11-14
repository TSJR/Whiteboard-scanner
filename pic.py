from picamera2 import Picamera2, Preview
from time import sleep

picam2 = Picamera2()
config = picam2.create_still_configuration()
picam2.configure(config)
picam2.start()
sleep(2)
picam2.capture_file("test2.jpg")
picam2.stop()