import pyrealsense2 as rs
import cv2
import numpy as np
from ultralytics import YOLO
import warnings
from icare_nlp.task_disp import TaskDisp
import pdb
from icare_nlp.utils import CvUtils
from icare_nlp.object_desc import ObjectDesc
from icare_nlp.object_qa import ObjectQA

warnings.filterwarnings('ignore')


#vision setting initialize
model = YOLO('yolov8n.pt')
pipe = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
profile = pipe.start(config)


#nlp setting initialize
task_disp=TaskDisp()

#init icare_nlp tool
cv_utils=CvUtils()
obj_desc=ObjectDesc()
obj_qa=ObjectQA()

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

            key=cv2.waitKey(1)
            if key == ord("q"):
                break
            elif key == ord("s"):
                cnt=0
                while True:
                    obj_detect=cv_utils.form_cv_json(results)
                    obj_desc_res = obj_desc.form_response(obj_detect)
                    if cnt==0:
                        print("\n SYSTEM: " + obj_desc_res)
                        cnt+=1
                    user_task_follow = input("\n SYSTEM: 有冇關於嗰個場景嘅問題？如果有，輸入Yes，如果冇，輸入No.\n USER: ")
                    if user_task_follow.lower() == "yes":
                        question = input("\n SYSTEM: 你嘅问题係： \n USER: ")
                        obj_qa_res = obj_qa.form_response(question, obj_detect)
                        print("\n SYSTEM: " + obj_qa_res)
                    if user_task_follow.lower() == "no":
                        break

finally:
    pipe.stop()
    cv2.destroyAllWindows()