from ast import arg
import cv2
from multiprocessing import Process, Manager
from camera_worker import camera_worker 
from log import logger
from track import yolo_worker


def main():
    SOURCES = [
                "securitycameravideos/video5.mp4",
                # "securitycameravideos/video2.mp4"
               ]

    manager = Manager()
    stop_event = manager.Event() 
    result_queue = manager.Queue()
    yolo_queue = manager.Queue()
    
    processes = []
    for cam_id, src in enumerate(SOURCES):
        
        p_cam = Process(target=camera_worker, args=(cam_id, src, result_queue, stop_event, yolo_queue))
        p_cam.start()
        processes.append(p_cam)
        
        p_yolo = Process(target=yolo_worker, args=(yolo_queue, stop_event))
        p_yolo.start()
        processes.append(p_yolo)
        
    prev_motion = {cam_id: False for cam_id in range(len(SOURCES))}
    try:
        while True:
            cam_id, frame_id, time, frame, motion = result_queue.get()
            if frame is None:
                cv2.destroyWindow(f"Cam{cam_id}")
                continue
            if motion and not prev_motion[cam_id]: 
                logger.info(f"Cam{cam_id} Hareket başladı. {time}")
                prev_motion[cam_id] = True 
                
            elif not motion:
                prev_motion[cam_id] = False
            if motion: 
                cv2.putText(frame, "Motion Detected", (10, 300), cv2.FONT_HERSHEY_PLAIN, 2, 255, 2)

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
