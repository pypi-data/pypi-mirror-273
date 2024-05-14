import json
import os
print(os.getcwd())

from icare_nlp.receipt_desc import ReceiptDesc



with open("../../dataset/ocr_res.json", "r", encoding="utf-8") as f:
    data = json.load(f)

receipt_desc=ReceiptDesc()

for i in range(len(data)):
    ocr_text_i=data[i]["ocr_text"]
    ocr_desc_i=receipt_desc.form_response(ocr_text_i)
    print(ocr_desc_i)