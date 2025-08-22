from ultralytics import YOLO
import cv2

def yolo_worker(yolo_queue, stop_event):

    model = YOLO("yolo11n.pt")
    tracker = "botsort.yaml"

    while not stop_event.is_set():
        if not yolo_queue.empty():
            frame, time, motion = yolo_queue.get()

            if motion:
                results = model.track(
                    source=frame,  # ❌ burada timestamp değil frame gidecek
                    tracker=tracker,
                    classes=[0, 15, 16, 2, 7],  # insan, köpek, kedi, araba, kamyon
                    iou=0.5,
                    persist=True,
                    show=False,
                    verbose=False
                )
                results[0].plot()
            

