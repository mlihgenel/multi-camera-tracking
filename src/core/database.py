import sqlite3 
from datetime import datetime 
from dotenv import load_dotenv
import os
from src.core.log import logger

load_dotenv 

try:
    DB_PATH = os.getenv("DB_PATH")
except Exception as e:
    logger.error(f"Database yolu alınırken hata oluştu: {e}")
    

class TrackerDB():
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cam_id INTEGER,
            frame_id INTEGER,
            timestamp TEXT,
            class_name TEXT,
            confidence REAL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS motions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cam_id INTEGER,
            frame_id INTEGER,
            timestamp TEXT,
            motion INTEGER
        )
        """)
        
        conn.commit()
        conn.close()
        
    def add_detection(self, cam_id, frame_id, class_name, confidence, timestamp=None):
        try:
            if timestamp is None:
                timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            cursor = conn.cursor()  
            
            cursor.execute("""
                INSERT INTO detections (cam_id, frame_id, class_name, confidence, timestamp)
                VALUES (?,?,?,?,?)
                                """, (cam_id, frame_id, class_name, confidence, timestamp))
            
        except Exception as e:
            logger.error(f"Database eklemesi yapılamadı, hata: {e}")
            
        conn.commit()
        conn.close()

    def add_motion(self, cam_id, frame_id, motion, timestamp=None):
        try:
            if timestamp is None:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            cursor = conn.cursor()
            
            cursor.execute("""
            INSERT INTO motions (cam_id, frame_id, motion, timestamp)
            VALUES (?, ?, ?, ?)
            """, (cam_id, frame_id, int(motion), timestamp))
            
        except Exception as e:
            logger.error(f"Database eklemesi yapılamadı, hata: {e}")
            
        conn.commit()
        conn.close()

    