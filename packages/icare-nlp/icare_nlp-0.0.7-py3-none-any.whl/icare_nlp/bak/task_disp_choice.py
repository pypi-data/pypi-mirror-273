import json
import os

from icare_nlp_tools.icare_nlp.object_desc import ObjectDesc
from icare_nlp_tools.icare_nlp.object_qa import ObjectQA
from icare_nlp_tools.icare_nlp.receipt_desc import ReceiptDesc
from icare_nlp_tools.icare_nlp.bak.receipt_qa_total import ReceiptQA

class TaskDisp(object):
    def __init__(self):
        self.intro_can="\n SYSTEM: 你想我幫你做咩任務？请输入对应嘅数字：1 俾我形容周围环境，2 俾我答覆关于周围环境嘅问题，3 俾我形容收据，4 俾我答覆收据嘅总费用，5 俾我形容 QR 码，同埋 6 俾我答覆关于 QR 码嘅问题。如果你想退出，请輸入7。"
        self.task_id=0
        self.object_desc = ObjectDesc()
        self.object_qa=ObjectQA()
        self.receipt_desc=ReceiptDesc()
        self.receipt_qa=ReceiptQA()


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
                print("搵唔到文件。請輸入一個有效嘅文件路徑。")

    def disp_start(self):
        while True:
            print(self.intro_can)
            self.task_choice = int(input("\n USER: 請輸入任務編號:(1-7): "))
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
                question = input("\n USER: 你嘅问题係： ")
                obj_qa_res = self.object_qa.form_response(question, obj_detect)
                print("SYSTEM: "+obj_qa_res)

            elif self.task_choice == 3:
                ocr_text_file =  self.get_file_path("\n USER: OCR 检测文本係 (json file path)： ")
                ocr_text = self.extract_ocr_text(ocr_text_file)
                rc_desc_res = self.receipt_desc.form_response(ocr_text)
                print("SYSTEM: "+rc_desc_res)
                user_task_follow=input("\n USER: 有冇關於收據總價嘅問題？如果有，輸入Yes，如果冇，輸入No.")
                if user_task_follow.lower()=="yes":
                    rc_qa_res = self.receipt_qa.form_response(ocr_text)
                    print("SYSTEM: "+rc_qa_res)
                else:
                    continue

            elif self.task_choice == 4:
                ocr_text_file =  self.get_file_path("\n USER: OCR 检测文本係 (json file path)： ")
                ocr_text = self.extract_ocr_text(ocr_text_file)
                rc_qa_res = self.receipt_qa.form_response(ocr_text)
                print("SYSTEM: "+rc_qa_res)
            elif self.task_choice == 7:
                print("\n SYSTEM: Icare NLP 模組已經退出 \n")
                break
            else:
                print("\n SYSTEM: 唔係有效嘅輸入，請重新輸入。\n")
                continue
