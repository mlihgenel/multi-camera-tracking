from log import logger

def yolo_track_frame(frame, model, tracker_config="botsort.yaml", classes=[0, 15, 16, 2, 7]):

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
            return annotated_frame
        else:
            return frame
            
    except Exception as e:
        logger.error(f"YOLO tracking hatası: {e}")
        return frame
            

