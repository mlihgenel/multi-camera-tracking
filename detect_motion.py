import cv2
import numpy as np
from log import logger 

def detect_motion(frame, mask, frame_count, pixel_thresh=200, area_thresh=500):
    frame_out = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mask_upper = mask.apply(frame)
    pixel_count = np.count_nonzero(mask_upper)
        
    motion = False
    
    if frame_count > 1 and pixel_count > pixel_thresh:
        motion = True
    return motion, frame_out
