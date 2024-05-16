import os
os.environ["CUDA_VISIBLE_DEVICES"] = "3"
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json
from tqdm import tqdm


system="""
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
text: "Bello\nDining\n天水圍天一商城2樓2008號鋪\n臺號\n11\n人數\n5\n單號\n000048\n日期\n2017-06-03\n18:10:54\n名稱\n數量\n金額\n芝士吞拿魚焗薯皮\n1\n38.\n00\n香脆流心芝士條\n1\n36.\n00\n忌廉吞拿魚長通粉\n1\n64.\n00\n香辣烤雞薄餅\n1\n78.\n00\n經典漢堡\n(配薯條)\n1\n56.\n00\n總金額:272.\n00\n0O1\n100\n000048\n2017-06-03\n18:48:20\nGeneral"
You should return: 272.00
"""


user="""
小票的ocr是:{}. 请输出总花费的数目。Please ensure to output only the float number without additional words.
"""



#load model
model_id = "/data/zy/models/Meta-Llama-3-8B-Instruct-hf"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="cuda",
)

def inference(model, tokenizer, messages):
    input_ids = tokenizer.apply_chat_template(messages,add_generation_prompt=True,return_tensors="pt").to(model.device)

    terminators = [tokenizer.eos_token_id,tokenizer.convert_tokens_to_ids("<|eot_id|>")]

    outputs = model.generate(
        input_ids,
        max_new_tokens=256,
        eos_token_id=terminators,
        do_sample=True,
        temperature=0.6,
        top_p=0.9,
    )
    response = outputs[0][input_ids.shape[-1]:]
    return tokenizer.decode(response, skip_special_tokens=True)


#load data
with open("ocr_res_with_gt.json", "r", encoding="utf-8") as f:
    ocr_data=json.load(f)

infer_res_list=[]
for item in tqdm(ocr_data):
    idx=item["index"]
    ocr_text_i=item["ocr_text"]
    cost_gt=item["cost_gt"]
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user.format(ocr_text_i)}
    ]
    infer_res=inference(model, tokenizer, messages)
    infer_res_list.append({"index":idx, "ocr_text":ocr_text_i, "cost_gt":cost_gt,"llama_infer_res":infer_res})

with open("llama_infer_res.json", "w", encoding="utf-8") as f:
    json.dump(infer_res_list, f, ensure_ascii=False, indent=2)