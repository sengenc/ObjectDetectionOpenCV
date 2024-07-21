import cv2
from object_detector import *
import numpy as np
from object_render import *
import matplotlib.pyplot as plt

# Load aruco detector
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)
arucoParam = cv2.aruco.DetectorParameters_create()

# Load object detector for edges
detector = HomogeneousBgDetector()
# Load object detector for the edges of our .stl object
imgDetector = HomogeneousBgDetector()
# Load renderer for our .stl object
imgRenderer = RenderObject()

# Path to the .stl file
myObject = imgRenderer.import_object('bird.stl')
# Default file name of the rendered object
myImage = cv2.imread('render.png')

# Load camera image
video = cv2.VideoCapture(0)


while True:
    _, frame = video.read()

    # Get aruco marker(s), the function means to find multiple markers
    # corners, ids, rejected = cv2.aruco.detectMarkers(frame, aruco_dict, parameters=arucoParam)
    corners, _, _ = cv2.aruco.detectMarkers(frame, aruco_dict, parameters=arucoParam)

    # Draw polygon around the marker (just marker)
    int_corners = np.int0(corners)
    cv2.polylines(frame, int_corners, True, (0, 255, 0), 3)

    # This is for the edges of all objects in camera
    contours = detector.detect_objects(frame)
    # This is the edges of our .stl model
    image_contours = imgDetector.detect_objects(myImage)

    # Drawing the edges of the model in camera (not in the center)
    for img_cont in image_contours:
        cv2.polylines(frame, [img_cont], True, (0, 0, 255), 2)

    for cnt in contours:

        # size of objects
        rect = cv2.minAreaRect(cnt)
        (x, y), (w, h), _ = rect
        # For the red dot in the middle of all objects
        cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)
        objAreas = cv2.contourArea(cnt)

        # lines around the object
        cv2.polylines(frame, [cnt], True, (255, 0, 0), 2)

        if len(corners) != 0:
            # Pixel to cm ratio
            aruco_perimeter = cv2.arcLength(corners[0], True)
            pixel_cm_ratio = aruco_perimeter / (4.7 * 4)

            # Pixel to area ratio, based on aruco`s pixels to its area
            arucoArea = cv2.contourArea(int_corners[0])
            pixel_area_ratio = arucoArea / (4.7 * 4.7)

            # # shows the width in pixels of objects, if you rotate the object, the pixels will change
            cv2.putText(frame, "Width {} cm".format(round(w / pixel_cm_ratio, 1)), (int(x), int(y - 15)), cv2.FONT_HERSHEY_PLAIN, 1, (10, 77, 0), 2)
            # # shows the height in pixels of objects, if you rotate the object, the pixels will change
            cv2.putText(frame, "Height {} cm".format(round(h / pixel_cm_ratio, 1)), (int(x), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 1, (10, 77, 0), 2)
            cv2.putText(frame, "Area {} cm2".format(round(objAreas / pixel_area_ratio, 2)), (int(x), int(y + 45)),
                        cv2.FONT_HERSHEY_PLAIN, 1, (10, 77, 0), 2)
        else:
            # shows the width in pixels of objects, if you rotate the object, the pixels will change
            cv2.putText(frame, "Width {}".format(round(w, 1)), (int(x), int(y - 15)), cv2.FONT_HERSHEY_PLAIN, 1,
                        (10, 77, 0), 2)
            # shows the height in pixels of objects, if you rotate the object, the pixels will change
            cv2.putText(frame, "Height {}".format(round(h, 1)), (int(x), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 1,
                        (10, 77, 0), 2)
            cv2.putText(frame, "Area {}".format(objAreas), (int(x), int(y + 45)),
                        cv2.FONT_HERSHEY_PLAIN, 1, (10, 77, 0), 2)

    cv2.imshow('cameraView', frame)
    if cv2.waitKey(1) == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
