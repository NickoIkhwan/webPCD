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
        self.objects_count = 0  
        self.traffic_weight = 0 
        self.current_file_id = None  
        self.stop_processing = False  

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

        objects_count = 0
        traffic_weight = 0

        results = self.model.predict(frame, conf=0.5, verbose=False)
        frame = results[0].plot()

        for r in results:
            boxes = r.boxes
            objects_count = len(boxes)
            for box in boxes:
                cls_id = int(box.cls[0])
                label = r.names[cls_id]
                
                if label.lower() == 'mobil':
                    traffic_weight += 4
                elif label.lower() == 'kendaraan besar':
                    traffic_weight += 6
                else:
                    traffic_weight += 1

        if traffic_weight > 100:
            traffic_weight = 100

        self.traffic_weight = traffic_weight
        self.objects_count = objects_count

        
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    def get_frames(self, video_path):
        current_timer = 10       
        last_time_update = time.time()
        lampu_state = "GREEN"     
        objects_count = 0


        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            if self.stop_processing:
                break
            
            ret, frame = cap.read()
            if not ret: break
            
            try:
                results = self.model.predict(frame, conf=0.5, verbose=False)
                frame = results[0].plot() 

                traffic_weight = 0
                objects_count = 0
                for r in results:
                    boxes = r.boxes
                    objects_count += len(boxes)
                    for box in boxes:
                        cls_id = int(box.cls[0])
                        label = r.names[cls_id]
                        
                        if label.lower() == 'mobil':
                            traffic_weight += 4
                        elif label.lower() == 'kendaraan besar':
                            traffic_weight += 6
                        else:
                            traffic_weight += 1

                if traffic_weight > 100:
                    traffic_weight = 100
                
                self.traffic_weight = traffic_weight 
                self.objects_count = objects_count 

                if time.time() - last_time_update >= 1:
                    if current_timer > 0:
                        current_timer -= 1
                    last_time_update = time.time()

                if current_timer <= 0:
                    if lampu_state == "RED":
                        lampu_state = "GREEN"
                        current_timer = 20 if self.traffic_weight > 80 else 10
                    else: 
                        lampu_state = "RED"
                        current_timer = 30 if self.traffic_weight > 80 else 15

                color_map = {"RED": (0, 0, 255), "GREEN": (0, 255, 0)}
                current_color = color_map[lampu_state]

                cv2.putText(frame, f"STATUS: {lampu_state}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, current_color, 3)
                cv2.putText(frame, f"TIMER: {current_timer}s", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
                _, buffer = cv2.imencode('.jpg', frame)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            
            except Exception as e:
                print(f"Error processing frame: {e}")
                continue

        cap.release()

