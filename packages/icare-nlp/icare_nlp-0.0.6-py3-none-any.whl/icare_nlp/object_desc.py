import json
from importlib import resources
from collections import Counter

class ObjectDesc(object):
    def __init__(self):
        self.description = None
        with resources.open_text("icare_nlp.resources", "desc_words.json") as f:
            self.desc_words = json.load(f)
        # with open("./resources/desc_words.json", "r") as f:
        #     self.desc_words = json.load(f)

    def get_region(self, obj_x, obj_y):
        width_threshold = 640
        height_threshold = 360
        if obj_x < width_threshold and obj_y < height_threshold:
            region = "top left"
        elif obj_x >= width_threshold and obj_y < height_threshold:
            region = "top right"
        elif obj_x < width_threshold and obj_y >= height_threshold:
            region = "bottom left"
        else:
            region = "bottom right"
        return region

    def form_response_part_1(self, obj_detect):
        object_counts = Counter(obj["text"] for obj in obj_detect)
        sorted_items = sorted(object_counts.items(), key=lambda x: x[1], reverse=True)
        category_to_desc = {item['category']: item['desc_words'] for item in self.desc_words}
        output = []
        for item, count in sorted_items:
            desc = category_to_desc.get(item, "")
            output.append(f"{count}{desc}")
        desc_part1="而家眼前嘅景象有" + ", ".join(output)+"."
        return desc_part1

    def form_response_part_2(self, obj_detect):
        top_left=[]
        top_right=[]
        bottom_left=[]
        bottom_right=[]

        for item in obj_detect:
            obj_x,obj_y,obj_w,obj_h=item["position"]
            region=self.get_region(obj_x, obj_y)
            if region == "top left":
                top_left.append(item["text"])
            elif region == "top right":
                top_right.append(item["text"])
            elif region == "bottom left":
                bottom_left.append(item["text"])
            elif region == "bottom right":
                bottom_right.append(item["text"])
        objects_by_region={"左上": top_left, "右上": top_right, "左下": bottom_left,"右下": bottom_right}
        category_to_desc = {item['category']: item['desc_words'] for item in self.desc_words}
        desc_sentences=[]
        for region, objects in objects_by_region.items():
            object_counts = Counter(objects)
            for obj, count in object_counts.items():
                if count>0:
                    desc_sentences.append(f"視線{region}角嘅場景入面有{count}{category_to_desc[obj]}.")
        return "".join(desc_sentences)

    def form_response(self, obj_detect):
        desc_part1=self.form_response_part_1(obj_detect)
        desc_part2=self.form_response_part_2(obj_detect)
        return desc_part1 + desc_part2