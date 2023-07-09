# /**
#  * @file utils.py 
#  * @author Samay Pashine
#  * @brief File containing the utility function to improve the readability of the code.
#  * @version 1.5
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

def calculate_segment_distance(shape, segments = 10, intermediate_dist = 20):
    """Function to calculate the segment length, and intermediate distance between segment for the boundary.

    Args:
        shape (Tuple): Shape of Image
        segments (int, optional): Number of segements. Defaults to 10.
        intermediate_dist (int, optional): Distance between the segments. Defaults to 20.

    Returns:
        int: segment length of x
        int: segment length of y
        int: distance between segments for x
        int: distance between segments for y
    """
    dist_x = (shape[1] // segments)
    dist_y = (shape[0] // segments)
    
    inter_x = int((shape[1] - intermediate_dist) / segments)
    inter_y = int((shape[0] - intermediate_dist) / segments)
    return int(dist_x), int(dist_y), int(inter_x), int(inter_y) 
