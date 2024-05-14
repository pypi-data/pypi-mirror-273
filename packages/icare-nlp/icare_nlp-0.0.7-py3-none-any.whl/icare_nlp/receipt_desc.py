import re

class ReceiptDesc(object):
    def __init__(self):
        self.receipt_desc = "呢张收据主要嘅信息包括"

    def ocr_process(self, ocr_text):
        lines = ocr_text.split('\n')
        chinese_per_line = []
        for line in lines:
            chinese_characters = ''.join(re.findall(r'[\u4e00-\u9fff]+', line))
            chinese_per_line.append(chinese_characters)
        chinese_text_by_line = [chinese for chinese in chinese_per_line if chinese]
        return chinese_text_by_line

    def form_response(self, ocr_text):
        zh_lines=self.ocr_process(ocr_text)
        return self.receipt_desc+", ".join(zh_lines)