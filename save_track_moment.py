import os
import cv2
from log import logger 
from datetime import datetime

FILE_NAME = os.path.join("tracking_moments")
os.makedirs(FILE_NAME, exist_ok=True)

class TrackVideoWriter:
    def __init__(self, output_dir=FILE_NAME, codec="mp4v", fps=20.0):
        try:
            self.output_dir = output_dir
        except Exception as e:
            logger.error(f"Dosya yolu bunulamadı: {e}")
        try:
            self.codec = cv2.VideoWriter_fourcc(*codec)
        except Exception as e: 
            logger.warning(f"codec hatası: {e}")
        self.fps = fps
        self.out = None
        self.active = False

    def start(self, cam_id, frame):
        try:
            try:
                filename = os.path.join(self.output_dir, f"cam{cam_id}")
                os.makedirs(filename, exist_ok=True)
                time = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
                file = os.path.join(filename, f"cam{cam_id}_{time}.mp4")
            except Exception as e:
                logger.error(f"Dosya yolunda hata bulundu: {e}")    
                
            try:
                self.out = cv2.VideoWriter(file, self.codec, self.fps, (frame.shape[1], frame.shape[0]))
            except Exception as e:
                logger.error(f"Video yazılmasında hata: {e}")
                
            if not self.out.isOpened():
                self.out = None
                self.active = False
                return
            self.active = True
            logger.info("Takip anı kaydedilmeye başlandı")
        except Exception as e:
             logger.error("Video kaydedilmeye başlayamadı: {e}")
                    
    def write(self, frame):
        try:
            if self.active and self.out is not None:
                self.out.write(frame)
        except Exception as e:
            logger.error(f"Video yazılırken hata oluştur: {e}")
            
    def stop(self):
        if self.active and self.out is not None:
            self.out.release()
        self.out = None
        self.active = False
