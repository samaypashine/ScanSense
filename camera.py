# /**
#  * @file camera.py 
#  * @author Samay Pashine
#  * @brief Code to open the camera in a different thread.
#  * @version 1.3
#  * @date 2023-07-07
#  * 
#  * @copyright Copyright (c) 2023
#  * 
#  */

# Importing necessary libraries
import cv2
import time
from threading import Thread

# Class to capture frames in different thread.
class ThreadedCamera(object):
    def __init__(self, source=0):
        """Constructor initialize the capture variable with the source, and thread parameters.

        Args:
            source (int, optional): Camera code to use for capturing images. Defaults to 0.
        """
        self.capture = cv2.VideoCapture(source)
        time.sleep(2)
        self.thread = Thread(target=self.update, args=())

        self.thread.daemon = True
        self.thread.start()

    def update(self):
        """Function to update the frame in different thread.
        """
        while True:
            if self.capture.isOpened():
                self.capture.grab()
                time.sleep(0.005)

    def grab_frame(self):
        """Function to grab the frame from different thread.

        Returns:
            cv.Mat: return a BGR image.
        """
        _, img = self.capture.retrieve()
        return img
