import cv2
import time
from multiprocessing import Process, Manager
from camera import camera_worker 

def main():
    SOURCES = ["securitycameravideos/SecurityCameraSamplevideo.mp4", 
               "securitycameravideos/SecurityCamera–Sample.mp4",
               "securitycameravideos/Camera– SampleFootage.mp4"
            ]

    manager = Manager()
    stop_event = manager.Event() 
    result_queue = manager.Queue()

    processes = []
    for cam_id, src in enumerate(SOURCES):
        p = Process(target=camera_worker, args=(cam_id, src, result_queue, stop_event))
        p.start()
        processes.append(p)

    try:
        while True:
            cam_id, frame_id, time, gray, motion = result_queue.get()
            if gray is None:
                cv2.destroyWindow(f"Cam{cam_id}")
                continue
            if motion: 
                cv2.putText(gray, "Hareket Algılandı", (10, 300), cv2.FONT_HERSHEY_PLAIN, 2, 255, 2)
            print(f"[Main] Cam#{cam_id} Frame#{frame_id}")
            cv2.imshow(f"Cam{cam_id}", gray)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        stop_event.set()  
        for p in processes:
            p.join()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
