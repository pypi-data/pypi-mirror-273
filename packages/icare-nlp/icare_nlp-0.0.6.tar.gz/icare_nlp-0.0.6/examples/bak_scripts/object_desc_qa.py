import json
import os
print(os.getcwd())

from icare_nlp.object_qa import ObjectQA
from icare_nlp.object_desc import ObjectDesc


with open("../../dataset/obj_detect_question.json", "r", encoding="utf-8") as f:
    data = json.load(f)

object_desc=ObjectDesc()
object_qa=ObjectQA()
for item in data:
    idx=item["index"]
    obj_detect=item["obj_detect"]

    print("SCENE DESC: ", object_desc.form_response(obj_detect))
    questions=item["questions"]
    print("Index: ", idx)
    print("Object Detection: ", obj_detect)
    for k in questions:
        question=questions[k]
        ans=object_qa.form_response(question, obj_detect)

        print("Question: ", question)
        print("Answer: ", ans)
        print()