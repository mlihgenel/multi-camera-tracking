import csv 
import os
from src.core.log import logger 
from dotenv import load_dotenv

try:
    load_dotenv()
    FILENAME = os.getenv("CSV_LOG")
    
except Exception as e:
    logger.error(f".env dosyasından değişkenler alınamadı: {e}")
    
class CSVLogger():
    def __init__(self, filename=FILENAME):
        self.filename = filename
        if not os.path.exists(self.filename):
            try:
                with open(self.filename, mode="w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["cam_id", "frame_id", "timestamp", "obj_class", "confidence"])
            except Exception as e:
                logger.warning(f"CSV dosyasına oluşturulamadı: {e}")
                
    def log_csv(self, cam_id, frame_id, timestamp, cls_name, confidence):
        try:
            with open(self.filename, mode="a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([cam_id, frame_id, timestamp, cls_name, f"{confidence:.2f}"])
        except Exception as e:
            logger.warning(f"CSV dosyasına yazılırken hata oluştu: {e}")        
            
        
            