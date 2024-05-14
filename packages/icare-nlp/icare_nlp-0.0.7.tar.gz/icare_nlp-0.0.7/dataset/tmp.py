import json
import os
with open("obj_detect_question.json", "r") as f:
    data=json.load(f)
for item in data:
    idx=item["index"]
    obj_detect=item["obj_detect"]
    with open(os.path.join("obj_detect_files", f"{idx}.json"), "w") as f_i:
        json.dump(obj_detect, f_i, indent=2)


import random
import json


with open("/home/yi/Projects/icare_nlp_tools/icare_nlp/resources/category_tactile_description.json", "r", encoding="utf-8") as f:
    data=json.load(f)

objects=[]
for item in data:
    exp_list=item["cate_expressions"].split(",")
    objects.extend(exp_list)

actions = [
    "我點樣可以攞到{}？", "{}喺邊？", "{}附近有冇其他物體？", "{}喺我手嘅邊個方向？"
]

# Generating new samples
samples = [action.format(obj.strip()) for obj in objects for action in actions]
random.shuffle(samples)

# Write the generated samples to a text file
file_path = 'object_qa.txt'
with open(file_path, 'w', encoding='utf-8') as file:
    for sample in samples:
        file.write(sample + '\n')