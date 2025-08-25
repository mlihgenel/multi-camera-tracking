import cv2
import time 
from datetime import datetime
from detect_motion import detect_motion
from log import logger

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
    
    while not stop_event.is_set(): # kontrol değişkeni 
        ret, frame = cap.read()
        if not ret or frame is None:
            print(f"Cam{cam_id} video bitti.")
            logger.info(f"Cam{cam_id} görüntü bitti")
            result_queue.put((cam_id, None, None, None, None))
            break
        try:
            frame_resized = cv2.resize(frame, (600,400))
        except:
            logger.warning("Frame boyutlandırmasında hata oluştur") 
        
        if frame_id % skip == 0:
            fps = cap.get(cv2.CAP_PROP_FPS)
            count_frame += 1 
            motion, processed_frame = detect_motion(frame_resized, mask, count_frame)            
            processed_frame = cv2.putText(processed_frame, f"{fps} FPS", (10,30), cv2.FONT_HERSHEY_DUPLEX, 0.8, 255, 1)
            result_queue.put((cam_id, frame_id, datetime.now().strftime("%d-%m-%Y %H:%M:%S"), frame_resized, motion))
            time.sleep(0.03)
            
        frame_id += 1
        

    cap.release()
    print(f"[Cam{cam_id}] Durduruldu.")
    
