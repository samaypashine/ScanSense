# /**
#  * @file utils.py 
#  * @author Samay Pashine
#  * @brief File containing the utility function to improve the readability of the code.
#  * @version 1.4
#  * @date 2023-07-01
#  * 
#  * @copyright Copyright (c) 2023
#  * 
#  */

# Importing necessary libraries
import cv2
import numpy as np

def get_max_contour(contours, threshold_area=30000):
    """Function to find the largest contour.

    Args:
        contours (list): List of contour coordinates.
        threshold_area (int): Threshold value for area to avoid small contours.

    Returns:
        max_contour: Largest contour.
        max_area: Area of the largest contour.  
    """

    # Initial parameters
    max_contour = np.array([])
    max_area = 0

    for contour in contours:
        area = cv2.contourArea(contour)
        
        if area > threshold_area:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            
            if area > max_area and len(approx) >= 4:
                max_contour = approx
                max_area = area
    
    return max_contour, max_area