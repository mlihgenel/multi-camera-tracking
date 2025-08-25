from log import logger
from csv_logger import CSVLogger
from datetime import datetime

csv_logger = CSVLogger()

def yolo_track_frame(cam_id, frame_id, frame, model, tracker_config="botsort.yaml", classes=[0, 15, 16, 2, 7]):

    try:
        results = model.track(
            source=frame,
            tracker=tracker_config,
            classes=classes,
            iou=0.5,
            persist=True,
            show=False,
            verbose=False
        )
        
        if results and len(results) > 0 and results[0].boxes is not None:
            annotated_frame = results[0].plot()
            
            try:
                timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                for box in results[0].boxes:
                    cls_id = int(box.cls.item())
                    conf = float(box.conf.item())
                    cls_name = results[0].names[cls_id]
                    
                    csv_logger.log_csv(cam_id, frame_id, timestamp, cls_name, conf)
                return annotated_frame
            except Exception as e:
                logger.warning(f"YOLO'dan takip nesneleri alınamadı.")
                return frame 
        else:
            return frame
        
            
    except Exception as e:
        logger.error(f"YOLO tracking hatası: {e}")
        return frame
            

