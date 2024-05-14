import json
import os
import torch
from .object_desc import ObjectDesc
from .object_qa import ObjectQA
from .receipt_desc import ReceiptDesc
from .receipt_qa import ReceiptQA
from transformers import AutoTokenizer, AutoModelForSequenceClassification
class TaskDisp(object):
    def __init__(self):
        self.cls_model="Yiyiyiyiyi/icare_task_disp_bert"
        self.tokenizer = AutoTokenizer.from_pretrained(self.cls_model)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.cls_model)
        self.model.eval()
        self.task_id=0
        self.object_desc = ObjectDesc()
        self.object_qa=ObjectQA()
        self.receipt_desc=ReceiptDesc()
        self.receipt_qa=ReceiptQA()

    def intent_classify(self, query):
        inputs = self.tokenizer(query, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
            prediction = torch.argmax(outputs.logits, dim=-1)
            pred_label = self.model.config.id2label[prediction.item()]
        if pred_label=="物體描述":
            self.task_choice=1
        elif pred_label=="物體問答":
            self.task_choice=2
        elif pred_label=="收據描述":
            self.task_choice=3
        elif pred_label=="收據問答":
            self.task_choice=4
        elif pred_label=="QR碼描述":
            self.task_choice=5
        elif pred_label=="QR碼問答":
            self.task_choice=6
        print("\n SYSTEM： 我會幫你完成呢個{}嘅任務。".format(pred_label))



    def extract_obj_detect(self, json_file):
        with open(json_file, "r") as f:
            obj_detect=json.load(f)
        return obj_detect

    def extract_ocr_text(self, json_file):
        with open(json_file, "r") as f:
            ocr_data=json.load(f)
        ocr_text=""
        for item in ocr_data:
            ocr_text+=item["text"]+'\n'
        return ocr_text

    def get_file_path(self, prompt):
        while True:
            file_path = input(prompt)
            if os.path.exists(file_path):
                return file_path
            else:
                print("SYSTEM： 搵唔到文件。請輸入一個有效嘅文件路徑。")

    def disp_start(self):
        while True:
            user_query = input("\n 講你想講嘅嘢，或者講exit或者退出. USER: ")
            if user_query=="exit" or user_query=="退出":
                self.task_choice=7
            else:
                self.intent_classify(user_query)
            if self.task_choice == 1:
                obj_detect_file=self.get_file_path("\n USER: 物件检测列表係 (json file path): ")
                obj_detect=self.extract_obj_detect(obj_detect_file)
                obj_desc_res=self.object_desc.form_response(obj_detect)
                print('\n')
                print("SYSTEM: "+obj_desc_res)
                user_task_follow=input("\n USER: 有冇關於嗰個場景嘅問題？如果有，輸入Yes，如果冇，輸入No.")
                if user_task_follow.lower()=="yes":
                    question = input("\n USER: 你嘅问题係： ")
                    obj_qa_res = self.object_qa.form_response(question, obj_detect)
                    print('\n')
                    print("SYSTEM: "+ obj_qa_res)
                else:
                    continue

            elif self.task_choice == 2:
                obj_detect_file = self.get_file_path("\n USER: 物件检测列表係 (json file path): ")
                obj_detect = self.extract_obj_detect(obj_detect_file)
                obj_qa_res = self.object_qa.form_response(user_query, obj_detect)
                print("SYSTEM: "+obj_qa_res)

            elif self.task_choice == 3:
                ocr_text_file =  self.get_file_path("\n USER: OCR 检测文本係 (json file path)： ")
                ocr_text = self.extract_ocr_text(ocr_text_file)
                rc_desc_res = self.receipt_desc.form_response(ocr_text)
                print("SYSTEM: "+rc_desc_res)
                user_task_follow=input("\n USER: 有冇關於收據總價嘅問題？如果有，輸入Yes，如果冇，輸入No.")
                if user_task_follow.lower()=="yes":
                    question = input("\n USER: 你嘅问题係： ")
                    rc_qa_res = self.receipt_qa.form_response(ocr_text,question)
                    print("SYSTEM: "+rc_qa_res)
                else:
                    continue

            elif self.task_choice == 4:
                ocr_text_file =  self.get_file_path("\n USER: OCR 检测文本係 (json file path)： ")
                ocr_text = self.extract_ocr_text(ocr_text_file)
                rc_qa_res = self.receipt_qa.form_response(ocr_text,user_query)
                print("SYSTEM: "+rc_qa_res)
            elif self.task_choice == 7:
                print("\n SYSTEM: Icare NLP 模組已經退出 \n")
                break
            else:
                print("\n SYSTEM: 唔係有效嘅輸入，請重新輸入。\n")
                continue
