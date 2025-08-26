import os
import cv2
from src.core.log import logger 
from datetime import datetime
from dotenv import load_dotenv

try:
    load_dotenv()
    
    FILE_NAME = os.getenv("TRACK_MOMENTS")
    os.makedirs(FILE_NAME, exist_ok=True)
    CODEC = os.getenv("CODEC")
    FPS = float(os.getenv("FPS"))
    
except Exception as e: 
    logger.error(f".env dosyasından değişkenler alınamadı: {e}")

class TrackVideoWriter:
    def __init__(self, output_dir=FILE_NAME, codec=CODEC, fps=FPS):
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

    def start(self, cam_id):
        try:
            try:
                filename = os.path.join(self.output_dir, f"cam{cam_id}")
                os.makedirs(filename, exist_ok=True)
                time = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
                file = os.path.join(filename, f"cam{cam_id}_{time}.{os.getenv("VIDEO_FORMAT")}")
            except Exception as e:
                logger.error(f"Dosya yolunda hata bulundu: {e}")    
                
            try:
                height = int(os.getenv("FRAME_HEIGHT"))
                width = int(os.getenv("FRAME_WIDTH"))
                self.out = cv2.VideoWriter(file, self.codec, self.fps, (height, width))
            except Exception as e:
                logger.error(f"Video yazılmasında hata: {e}")
                
            if not self.out.isOpened():
                self.out = None
                self.active = False
                return
            self.active = True
            logger.info(f"Takip anı kaydedilmeye başlandı: Cam{cam_id}")
        except Exception as e:
             logger.error(f"Video kaydedilmeye başlayamadı: {e}")
                    
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
