import cv2
import pyrealsense2 as rs
import numpy as np
from paddleocr import PaddleOCR
import cv2
from PIL import Image, ImageDraw, ImageFont
from paddleocr import PaddleOCR
import numpy as np
from icare_nlp.receipt_desc import ReceiptDesc
from icare_nlp.receipt_qa import ReceiptQA

ocr = PaddleOCR()

#打开 RealSense 摄像头
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 10)
pipeline.start(config)

ocr = PaddleOCR(use_gpu=True)
receipt_desc=ReceiptDesc()
receipt_qa=ReceiptQA()
def ocr_detect(frame_data):
    # Convert the BGR image to RGB
    img = Image.fromarray(cv2.cvtColor(frame_data, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    font_path = 'zh_font.ttf'
    font_size = 20
    font = ImageFont.truetype(font_path, font_size)

    # Perform OCR using PaddleOCR
    out = ocr.ocr(frame_data, cls=True)  # directly use the frame data here

    text = ''
    if out is not None:
        for line in out:
            if line:
                for entry in line:
                    if entry:
                        vertices = entry[0]
                        entry_text = entry[1][0].strip()

                        # Convert image back to array to use cv2 for rectangle drawing
                        cv2_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                        cv2.rectangle(cv2_img, (int(vertices[0][0]), int(vertices[0][1])),
                                      (int(vertices[2][0]), int(vertices[2][1])), (0, 255, 0), 2)

                        # Convert back to Pillow Image to draw text
                        img = Image.fromarray(cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB))
                        draw = ImageDraw.Draw(img)

                        # Draw text using Pillow
                        text_position = (int(vertices[0][0]), int(vertices[0][1]) - 10)
                        draw.text(text_position, entry_text, font=font, fill=(0, 255, 0))

                        if entry_text:
                            text += entry_text + '\n'
                else:
                    print("Skip: empty text")
    else:
        print("No text detected")
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    return text, img

try:
    while True:
        frames = pipeline.wait_for_frames()
        # print(frames.frame_number)
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue
        if frames.frame_number % 6 == 0:
            frame_data = np.asanyarray(color_frame.get_data())

            ocr_text, img=ocr_detect(frame_data)
            cv2.imshow("Img", img)
            key = cv2.waitKey(1)
            if key == ord("q"):
                break
            if key==ord("s"):
                cnt=0
                while True:
                    rc_desc_res = receipt_desc.form_response(ocr_text)
                    if cnt==0:
                        print("\n SYSTEM: " + rc_desc_res)
                        cnt+=1
                    user_task_follow = input("\n SYSTEM: 有冇關於收據總價嘅問題？如果有，輸入Yes，如果冇，輸入No. \n USER: ")
                    if user_task_follow.lower() == "yes":
                        question = input("\n SYSTEM: 你嘅问题係： \n USER: ")
                        rc_qa_res = receipt_qa.form_response(ocr_text, question)
                        print("\n SYSTEM: " + rc_qa_res)
                    if user_task_follow.lower() == "no":
                        break

except KeyboardInterrupt:
    pass
finally:
    pipeline.stop()