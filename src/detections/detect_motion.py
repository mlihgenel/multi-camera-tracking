import numpy as np
from dotenv import load_dotenv
import os 

load_dotenv()
PIXEL_THRESH = int(os.getenv("PIXEL_THRESH"))

def detect_motion(frame, mask, frame_count, pixel_thresh=PIXEL_THRESH):
    mask_upper = mask.apply(frame)
    pixel_count = np.count_nonzero(mask_upper)
    motion = False
    
    if frame_count > 1 and pixel_count > pixel_thresh:
        motion = True
    return motion
