import requests
import json
import os
import openai


class ReceiptQA(object):
    def __init__(self):
        self.system = """
        Task Overview: You will be given a text string resulting from the OCR scan of a receipt, primarily in traditional Chinese characters. This receipt is typical of transactions in Hong Kong, involving Cantonese language elements, numerals, and symbols. Your job is to answer questions about this receipt.
        
        Types of Questions:
        1. Product Presence: Determine if a specific product is mentioned in the receipt. Search the OCR text for a match; consider minor inconsistencies due to scanning errors. Respond with "有" (Yes) if the product is found, and "没有" (No) if it is not.
        2. Product Price Inquiry: First, verify if the product or product category exists in the text. If absent, reply with "嗰件嘢似乎唔喺單據入面". If present, locate the price typically listed after the product name and respond with "嘅價錢可能係" with the price.
        3. Total Cost Calculation: Identify the total cost of the purchase. Look for keywords like "總計", "總数", or "合計" near the end of the receipt, often near the symbols 'HKD' or '$'. Extract the numerical value associated with these keywords, ensuring to report the amount as a floating-point number, excluding any symbols.
        
        Additional Guidelines:
        1. Handle OCR inaccuracies by considering close matches as valid.
        2. Do not perform any calculations or conversions; report values as they appear.
        3. Ensure responses are concise and directly related to the query.
        4. No additional text should be included in your response.

        Here is a demonstration:
        input ocr_text: "Bello\nDining\n天水圍天一商城2樓2008號鋪\n臺號\n11\n人數\n5\n單號\n000048\n日期\n2017-06-03\n18:10:54\n名稱\n數量\n金額\n芝士吞拿魚焗薯皮\n1\n38.\n00\n香脆流心芝士條\n1\n36.\n00\n忌廉吞拿魚長通粉\n1\n64.\n00\n香辣烤雞薄餅\n1\n78.\n00\n經典漢堡\n(配薯條)\n1\n56.\n00\n總金額:272.\n00\n0O1\n100\n000048\n2017-06-03\n18:48:20\nGeneral"
        If the question is: 请问有冇香脆流心芝士条？
        The answer is: 有
        If the question is: 忌廉吞拿魚長通粉幾多錢？
        The answer is: 164.00
        If the question is: 我總共花咗幾多錢？
        The answer is: 272.00
        """
        self.user = """小票的ocr是:{}.用户的question是{}.请输出answer."""

        self.parameters = {
            'engine': 'gpt-3.5-turbo',
            'max_tokens': 400,
            'stop': None,
        }

    def form_response(self, ocr_text, user_query):
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model=self.parameters['engine'],
            messages=[
                {"role": "user", "content": self.system},
                {"role": "user", "content": self.user.format(ocr_text, user_query)}
            ],
            max_tokens=self.parameters['max_tokens'],
            stop=self.parameters['stop'],
        )
        resp = f"{response['choices'][0]['message']['content']}"
        if resp:
            return resp
        else:
            return "請再試一次。"
