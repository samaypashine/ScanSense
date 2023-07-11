# /**
#  * @file scansense.py 
#  * @author Samay Pashine
#  * @brief Code to guide user to keep the complete document in the frame by detecting edges.
#  * @version 1.1
#  * @date 2023-07-07
#  * 
#  * @copyright Copyright (c) 2023
#  * 
#  */

# Importing necessary libraries.
import os
import argparse
import logging
import numpy as np
from camera import *
from datetime import datetime
from utils import get_max_contour, calculate_segment_distance


def check_violations(points, shape, margin=10):
    """Function to check the violations of the document corners.

    Args:
        points (List): List of coordinates
        shape (tuple): shape of the frame
        margin (int, optional): violation margin around the boundaries. Defaults to 10.

    Returns:
        List: List of actions to follow to fix the violations.
    """
    margin_x_max, margin_y_max = shape[1] - margin, shape[0] - margin
    violation_list = []
    violation_count = 0

    for i in points:
        flag = False
        x, y = i[0][0], i[0][1]

        if x < margin:
            flag = True
            if 'LEFT' not in violation_list:
                violation_list.append('LEFT')
    
        if x > margin_x_max:
            flag = True
            if 'RIGHT' not in violation_list:
                violation_list.append('RIGHT')
        
        if y < margin:
            flag = True
            if 'UP' not in violation_list:
                violation_list.append('UP')
        
        if y > margin_y_max:
            flag = True
            if 'DOWN' not in violation_list:
                violation_list.append('DOWN')
        
        if flag:
            violation_count += 1
        
    if violation_count > 3:
        return ['TOP']
    else:
        return violation_list

# Driver code to initialize the parameters and start the guidance system.
if __name__ == '__main__':
    # Initializing the argument parser.
    parser = argparse.ArgumentParser(description='Guidance system for OCR through edge detection.')
    parser.add_argument('-debug', default=False, help='Debug mode')
    args = parser.parse_args()

    # Configuring the log handler.
    log_path = r'logs' + os.sep + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.log'
    os.makedirs(r'logs', exist_ok=True)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
                        handlers=[logging.FileHandler(log_path), logging.StreamHandler()])

    # Initial Parameters.
    DEBUG = args.debug
    cap = ThreadedCamera(0)
    pixel_boundary = 40
    margin = 10
    translucent_color = [230, 210, 80]
    alpha = 0.5
    fps_history = list()
    dist_x, dist_y = 0, 0
    segments = 20
    intermediate_dist = 20

    img_dir = os.sep.join([os.curdir, 'images'])
    output_dir = os.sep.join([os.curdir, 'outputs'])
    os.makedirs(output_dir, exist_ok=True)

    # for img_name in os.listdir(os.sep.join([img_dir])):
    while True:
        try:
            # Capturing the frame.
            start_time = time.time()
            img = cap.grab_frame()
            # img = cv2.imread(os.sep.join([img_dir, img_name]))
            aspect_ratio = img.shape[1] / img.shape[0]
            # img = cv2.resize(img, (480, int(480 / aspect_ratio)))            

            logging.info(f'Image Dimensions     : ({img.shape[1]}, {img.shape[0]})')
            logging.info(f'Aspect Ratio         : {aspect_ratio}')
            logging.info(f'Pixel Boundary       : {pixel_boundary}')

            # Creating an artifical pixel boundary to assist in locating the document corners.
            if dist_x == 0 and dist_y == 0:
                dist_x, dist_y, inter_x, inter_y =  calculate_segment_distance(img.shape, segments=segments, intermediate_dist=intermediate_dist)
            
            for i in range(1, segments):
                img = cv2.line(img, (0, int((inter_y * i) + (dist_y * (i-1)))), (0, int((inter_y * i) + (dist_y * i))), color=[255, 255, 255], thickness=5)
                img = cv2.line(img, (img.shape[1], int((inter_y * i) + (dist_y * (i-1)))), (img.shape[1], int((inter_y * i) + (dist_y * i))), color=[255, 255, 255], thickness=5)
                img = cv2.line(img, (int((inter_x * i) + (dist_x * (i-1))), 0), (int((inter_x * i) + (dist_x * i)), 0), color=[255, 255, 255], thickness=5)
                img = cv2.line(img, (int((inter_x * i) + (dist_x * (i-1))), img.shape[0]), (int((inter_x * i) + (dist_x * i)), img.shape[0]), color=[255, 255, 255], thickness=5)

            # Pre-processing the image, and detecting the edges in the image.
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img_blur = cv2.GaussianBlur(img_gray, (5, 5), 1)
            img_canny = cv2.Canny(img_blur, 0, 255)

            # Post-processing to stabalize the image.
            kernel = np.ones((5, 5))
            img_dilate = cv2.dilate(img_canny, kernel, iterations=2)
            img_eroded = cv2.erode(img_dilate, kernel, iterations=1)

            # Finding the contours, and selecting the largest contour.
            contours, hierarchy = cv2.findContours(img_eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours, max_area = get_max_contour(contours, threshold_area=15000)            
            
            # Creating a convex hull to get the shortest polygon for corners.
            points = np.array(contours, dtype=np.int32)
            hull = cv2.convexHull(contours)

            # Checking the violations of the corners coordinates to the boundary.
            action = check_violations(hull, img.shape, margin=margin)

            # Drawing the contour, and convex hull to visualize the document location.
            overlay = img.copy()
            cv2.drawContours(img, hull, -1, (0, 0, 255), 10)
            cv2.polylines(img, [hull], isClosed=True, color=translucent_color, thickness=2)
            cv2.fillPoly(overlay, [hull], translucent_color)
            img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

            fps_history.append(int(1 / (time.time() - start_time)))
            logging.info(f'Num. of Contours     : {len(hull)}')
            logging.info(f'Max Area             : {max_area}')
            logging.info(f'Action               : {action}')
            logging.info(f'FPS                  : {np.mean(fps_history)}')
            if len(action) == 0:
                logging.info('---------------------------- CAPTURE THE FRAME AND USE IT FOR OCR. ----------------------------')
            logging.info('-----------------------------------------------------------------------------------------------')

            cv2.imwrite(os.sep.join([output_dir, "{}.jpg".format(time.time())]), img)
            cv2.imshow('Display', img)
            key = cv2.waitKey(200)
            if key == ord('q'):
                break
        except Exception as e:
            if DEBUG:
                logging.error(f'Error Code : {e}')
            continue
