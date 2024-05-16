import pyrealsense2 as rs
import cv2
import numpy as np
from ultralytics import YOLO
import warnings


warnings.filterwarnings('ignore')

model = YOLO('yolov8n.pt')

pipe = rs.pipeline()
config = rs.config()


config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)


profile = pipe.start(config)
cv2.setNumThreads(4)
try:
    while True:
        frames = pipe.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue
        if frames.frame_number % 6 == 0:
            frame_data = np.asanyarray(color_frame.get_data())
            results = model(frame_data)
            annotated_frame = results[0].plot()
            cv2.imshow('Image Window', annotated_frame)
            # 等待1毫秒,如果没有按键输入就继续执行
            key=cv2.waitKey(1)
            if key == ord("q"):
                break

finally:
    pipe.stop()
    cv2.destroyAllWindows()