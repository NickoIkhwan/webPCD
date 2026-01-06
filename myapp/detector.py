import cv2
import os
import time
import numpy as np
from ultralytics import YOLO
from django.conf import settings

class TrafficDetector:
    def __init__(self, model_rel_path):
        self.model_path = os.path.join(settings.MEDIA_ROOT, model_rel_path)
        self.model = YOLO(self.model_path)
        self.objects_count = 0  # Store current vehicle count
        self.current_file_id = None  # Track currently processing file
        self.stop_processing = False  # Flag to stop processing

    def process_file(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()

        if ext in ['.jpg', '.jpeg', '.png', '.bmp']:
            return self.process_image(file_path)
        elif ext in ['.mp4', '.avi', '.mov', '.mkv']:
            return self.get_frames(file_path)
        else:
            return None

    def process_image(self, image_path):
        frame = cv2.imread(image_path)
        if frame is None:
            return
            
        results = self.model.predict(frame, conf=0.5, verbose=False)
        annotated_frame = results[0].plot()
        
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    def get_frames(self, video_path):
        current_timer = 10        # Start with 10 seconds
        last_time_update = time.time()
        lampu_state = "GREEN"     # Start with GREEN
        objects_count = 0


        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            # Check if stop processing flag is set
            if self.stop_processing:
                break
            
            ret, frame = cap.read()
            if not ret: break
            
            results = self.model.predict(frame, conf=0.5, verbose=False)
            frame = results[0].plot() 

            for r in results:
                boxes = r.boxes.cpu().numpy()
                self.objects_count = len(boxes)

            if time.time() - last_time_update >= 1:
                if current_timer > 0:
                    current_timer -= 1
                last_time_update = time.time()

            if current_timer <= 0:
                if lampu_state == "RED":
                    # Switch to GREEN
                    lampu_state = "GREEN"
                    # If it's quiet, keep green short. If busy, green stays longer to clear traffic.
                    current_timer = 20 if self.objects_count > 20 else 10
                    
                else: # If currently GREEN
                    # Switch to RED
                    lampu_state = "RED"
                    # If busy, red stays longer to manage other lanes (simulated).
                    current_timer = 30 if self.objects_count > 20 else 15

            color_map = {"RED": (0, 0, 255), "GREEN": (0, 255, 0)}
            current_color = color_map[lampu_state]

            cv2.putText(frame, f"STATUS: {lampu_state}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, current_color, 3)
            cv2.putText(frame, f"TIMER: {current_timer}s", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, f"VEHICLES: {self.objects_count}", (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)    

            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        cap.release()

