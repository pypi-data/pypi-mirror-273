import requests
import json
import os
import openai

class ReceiptQA(object):
    def __init__(self):
        self.system="""
        Task: You will be provided with a text string and tasked with calculating the total cost as indicated within. Please ensure to output only the float number without additional words. The numerical value of the cost typically follows keywords like "total", "總計", "總数", "合計", etc. This text string, which contains traditional Chinese characters, numbers, and symbols, is recognized via OCR and represents a receipt from Hong Kong, predominantly in Cantonese.
        
        Requirements:
        1. Please ensure to output only the float number without additional words.
        2. The floating-point number representing the cost can typically be found after the keyword "total," "總計," "總数," "合計," or similar terms, which may appear in various forms due to OCR errors. These variants could include "TTOL," "總金颚," and others.
        3. The total is often located at the bottom of the receipt, frequently near these keywords and may include symbols like 'HKD', '$', etc.
        4. In restaurant bills in the Hong Kong region, the total price of the dishes is often included along with a 10% service charge, but there will always be a displayed total price at the end, generally found after keywords such as "總計" (total), "總数" (total amount), or "合計" (sum total).
        5. It is crucial not to alter the value; you must return the floating-point number exactly as it appears in the text string, excluding symbols like '$'.
        6. You don't need to perform any additional calculations, as the total amount can be directly read from the text, although there might be issues with unclear recognition.
        7. If the answer is not discernible, return the null string.
        
        Here is a demonstration:
        input ocr_text: "Bello\nDining\n天水圍天一商城2樓2008號鋪\n臺號\n11\n人數\n5\n單號\n000048\n日期\n2017-06-03\n18:10:54\n名稱\n數量\n金額\n芝士吞拿魚焗薯皮\n1\n38.\n00\n香脆流心芝士條\n1\n36.\n00\n忌廉吞拿魚長通粉\n1\n64.\n00\n香辣烤雞薄餅\n1\n78.\n00\n經典漢堡\n(配薯條)\n1\n56.\n00\n總金額:272.\n00\n0O1\n100\n000048\n2017-06-03\n18:48:20\nGeneral"
        output: 272.00
        """
        self.user="""小票的ocr是:{}. 请输出总花费的数目。Please ensure to output only the float number without additional words."""

        self.parameters = {
            'engine': 'gpt-3.5-turbo',
            'max_tokens': 400,
            'stop': None,
        }
    def form_response(self, ocr_text):
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model=self.parameters['engine'],
            messages=[
                {"role": "user", "content": self.system},
                {"role": "user", "content": self.user.format(ocr_text)}
            ],
            max_tokens=self.parameters['max_tokens'],
            stop=self.parameters['stop'],
        )
        resp = f"{response['choices'][0]['message']['content']}"
        if resp:
            return "總花費係 "+resp+"."
        else:
            return "未識別到總花費，請再試多次。"
