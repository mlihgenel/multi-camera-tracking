import cv2
import numpy as np
import time 

    
def detect_motion(frame, mask, frame_count, pixel_thresh=500, area_thresh=500):
    frame_out = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mask_upper = mask.apply(frame)
    pixel_count = np.count_nonzero(mask_upper)
        
    motion = False
    if frame_count > 1 and pixel_count > pixel_thresh:
        motion = True
        contours, _ = cv2.findContours(mask_upper, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            if cv2.contourArea(cnt) > area_thresh:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame_out, (x, y), (x+w, y+h), 255, 2)
    
    return motion, frame_out


def camera_worker(cam_id, src, result_queue, stop_event, skip=1):
    cap = cv2.VideoCapture(src)
    if not cap.isOpened():
        print(f"[Cam{cam_id}] Kamera açılamadı")
        return

    frame_id = 0
    mask = cv2.createBackgroundSubtractorMOG2(250, 150, True)
    count_frame = 0 
    
    while not stop_event.is_set(): # kontrol değişkeni 
        ret, frame = cap.read()
        if not ret or frame is None:
            print(f"Cam{cam_id} video bitti.")
            result_queue.put((cam_id, None, None, None, None ))
            break
        try:
            frame_resized = cv2.resize(frame, (600,400))
        except:
            pass 
        
        if frame_id % skip == 0:
            fps = cap.get(cv2.CAP_PROP_FPS)
            count_frame += 1 
            motion, processed_frame = detect_motion(frame_resized, mask, count_frame)
            processed_frame = cv2.putText(processed_frame, f"{fps} FPS", (10,30), cv2.FONT_HERSHEY_DUPLEX, 0.8, 255, 1)
            result_queue.put((cam_id, frame_id, time.time(), processed_frame, motion))
            time.sleep(0.03)
        frame_id += 1

    cap.release()
    print(f"[Cam{cam_id}] Durduruldu.")
    
