import cv2
from PIL import Image, ImageDraw, ImageFont
from paddleocr import PaddleOCR
import numpy as np

# 全局OCR对象初始化
ocr = PaddleOCR(use_gpu=True)

def ocr_detect(img_path):
    out = ocr.ocr(img_path, cls=True)
    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)
    font_path = 'zh_font.ttf'
    font_size = 20
    font = ImageFont.truetype(font_path, font_size)

    text = ''
    for line in out:
        for entry in line:
            vertices = entry[0]
            entry_text = entry[1][0].strip()

            # 绘制边框（使用cv2，因为Pillow没有直接绘制矩形边框的方法）
            cv2_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            cv2.rectangle(cv2_img, (int(vertices[0][0]), int(vertices[0][1])),
                          (int(vertices[2][0]), int(vertices[2][1])), (0, 255, 0), 2)

            # 使用Pillow绘制文本
            text_position = (int(vertices[0][0]), int(vertices[0][1]) - 10)
            draw.text(text_position, entry_text, font=font, fill=(0, 255, 0))

            if entry_text:
                text += entry_text + '\n'
            else:
                print("Skip: empty text")
    img = Image.fromarray(cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB))
    return text, img

# 测试函数
img_path = '/home/yi/Projects/icare_nlp_tools/dataset/can_receipts/12.jpg'
extracted_text, processed_img = ocr_detect(img_path)

# 保存或显示处理后的图像
processed_img.save('output_image.jpg')
processed_img.show()
