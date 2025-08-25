import cv2
from multiprocessing import Process, Manager
from camera_worker import camera_worker 
from log import logger
from track import yolo_track_frame
from ultralytics import YOLO
import os 
from save_track_moment import TrackVideoWriter

def main():
    try:
        SOURCES = [
                    "videos/video5.mp4",
                    #"videos/video2.mp4",
                    #"videos/video3.mp4",
                ]
        logger.info("Video kaynakları alındı")
    except Exception as e:
        logger.error(f"Videolar bulunamadı: {e}")
        
    try:
        manager = Manager()
        stop_event = manager.Event() 
        result_queue = manager.Queue()
        
        logger.info("Kuyruklar(Queue) oluşturuldu")
        
    except Exception as e:
        logger.error(f"Kuyruklar(Queue) oluşturulamadı: {e}")            

    try:
        MODEL_PATH = "models/"
        MODEL_TYPE = os.path.join(MODEL_PATH, "yolo11n.pt")
        model = YOLO(MODEL_TYPE)
        tracker = "botsort.yaml"
        logger.info(f"YOLO modeli oluşturuldu: {MODEL_TYPE.split("/")[1]} / tracker: {tracker}")
    
    except Exception as e:
        logger.error(f"YOLO modeli ya da tracker hatası: {e}")
    
    
    try:        
        processes = []
        for cam_id, src in enumerate(SOURCES):
            p = Process(target=camera_worker, args=(cam_id, src, result_queue, stop_event))
            p.start()
            processes.append(p)
        logger.info("Processler başarıyla oluşturuldu")
    except Exception as e:
        logger.error(f"Process oluşturulurken hata çıktı: {e}")

        
    try:            
        prev_motion = {cam_id: False for cam_id in range(len(SOURCES))} # hareket takibini kontrol için
        tracking_active = {cam_id: False for cam_id in range(len(SOURCES))} # track takibi için 
        tracking_counter = {cam_id: 0 for cam_id in range(len(SOURCES))} # track işlemini hızlandırmak için
        video_writers = {cam_id: TrackVideoWriter() for cam_id in range(len(SOURCES))} # track anlarını kaydetmek için
        tracking_interval = 3 # frame atlayarak takip işleminin hızlandırılması 
    except Exception as e: 
        logger.error(f"Gerekli dictler oluşturulamadı: {e}")
    
    try:
        while True:
            cam_id, frame_id, time, frame, motion = result_queue.get()
            if frame is None:
                try:
                    cv2.destroyWindow(f"Cam{cam_id}")
                except Exception as e:
                    logger.error(f"Pencere kapatılamadı {e}")
                continue
                
            # Hareket durumu kontrolü
            if motion and not prev_motion[cam_id]: 
                logger.info(f"Cam{cam_id} Hareket başladı")
                prev_motion[cam_id] = True 
                tracking_active[cam_id] = True
                tracking_counter[cam_id] = 0
        
            elif not motion and prev_motion[cam_id]:
                logger.info(f"Cam{cam_id} Hareket bitti")
                prev_motion[cam_id] = False
                tracking_active[cam_id] = False
                tracking_counter[cam_id] = 0
                
            # YOLO tracking - sadece hareket varken ve belirli aralıklarla
            if motion and tracking_active[cam_id]:
                tracking_counter[cam_id] += 1
                # Her framede değil belirtilen framede bir takip yapılması
                if tracking_counter[cam_id] % tracking_interval == 0: 
                    frame = yolo_track_frame(frame, model, tracker)
            
            if motion and not video_writers[cam_id].active:
                video_writers[cam_id].start(cam_id, frame)

            if motion and video_writers[cam_id].active:
                video_writers[cam_id].write(frame)

            if not motion and video_writers[cam_id].active:
                video_writers[cam_id].stop()
                    
            # Ekrana bilgi yazdırılması 
            if motion: 
                cv2.putText(frame, "Motion Detected", (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                if tracking_active[cam_id]:
                    cv2.putText(frame, "Tracking Active", (10, 60), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            else:
                cv2.putText(frame, "No Motion", (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

            cv2.imshow(f"Cam{cam_id}", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        stop_event.set()  
        for p in processes:
            p.join()
        cv2.destroyAllWindows()
        
if __name__ == "__main__":
    main()
