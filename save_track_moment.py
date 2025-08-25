import os
import cv2

FILE_NAME = os.path.join("tracking_moments")
os.makedirs(FILE_NAME, exist_ok=True)

class TrackVideoWriter:
    def __init__(self, output_dir=FILE_NAME, codec="mp4v", fps=20.0):
        self.output_dir = output_dir
        self.codec = cv2.VideoWriter_fourcc(*codec)
        self.fps = fps
        self.out = None
        self.active = False

    def start(self, cam_id, frame_id, frame):
        filename = os.path.join(self.output_dir, f"cam{cam_id}")
        os.makedirs(filename, exist_ok=True)
        
        file = os.path.join(filename, f"cam{cam_id}_{frame_id}.mp4")
        self.out = cv2.VideoWriter(file, self.codec, self.fps, (frame.shape[1], frame.shape[0]))
        if not self.out.isOpened():
            self.out = None
            self.active = False
            return
        self.active = True
        
    def write(self, frame):
        if self.active and self.out is not None:
            self.out.write(frame)

    def stop(self):
        if self.active and self.out is not None:
            self.out.release()
        self.out = None
        self.active = False
