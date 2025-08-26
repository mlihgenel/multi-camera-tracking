import time

class FPScounter:
    def __init__(self):
        self.start_time = time.time()
        self.frame_count = 0
        self.fps = 0

    def update(self):
        self.frame_count += 1
        now = time.time()
        time_diff = now - self.start_time

        if time_diff >= 1.0:  
            self.fps = self.frame_count / time_diff
            self.start_time = now
            self.frame_count = 0

        return self.fps
