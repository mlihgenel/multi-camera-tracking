import cv2
import time 
from datetime import datetime
from src.core.detection.detect_motion import detect_motion
from src.core.log import logger
from dotenv import load_dotenv 
import os 

load_dotenv()

def camera_worker(cam_id, src, result_queue, stop_event, skip=1):
    
    try:
        cap = cv2.VideoCapture(src)
        if not cap.isOpened():
            print(f"[Cam{cam_id}] Kamera açılamadı")
            logger.warning(f"Cam{cam_id} açılamadı")
            return
        logger.info("Kamera/video başarılya başlatıldı")
    except:
         pass    
    
    frame_id = 0
    try:
        mask = cv2.createBackgroundSubtractorMOG2(250, 150, True)
    except Exception as e:
        logger.warning(f"Motion detection maskelemesinde hata: {e}")
    
    count_frame = 0 

    while not stop_event.is_set():
        
        ret, frame = cap.read()
        if not ret or frame is None:
            logger.info(f"Cam{cam_id} görüntü bitti")
            result_queue.put((cam_id, None, None, None, None))
            break
        try:
            height = int(os.getenv("FRAME_HEIGHT"))
            width = int(os.getenv("FRAME_WIDTH"))
            frame_resized = cv2.resize(frame, (height, width))
        except:
            logger.warning("Frame boyutlandırmasında hata oluştur") 
        
        if frame_id % skip == 0:
            count_frame += 1 
            motion = detect_motion(frame_resized, mask, count_frame) 
            result_queue.put((cam_id, frame_id, datetime.now().strftime("%d-%m-%Y %H:%M:%S"), frame_resized, motion))
            time.sleep(0.03)
            
        frame_id += 1
        

    cap.release()
    
