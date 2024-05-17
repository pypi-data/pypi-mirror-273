import json
import os
import zipfile

import cv2
import requests
from urllib.parse import urlencode
import torch

from data.neuro.letters_in_image import Letters_In_Image
from data.result.Class_text import Class_text
from data.result.Label_area import Label_area


class Text_Recognize_yolo:

    def __init__(self, model_path, yolo_path):
        """reads yolov5 taught model from yandex-disk and includes it in class example"""
        base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
        public_key = model_path  # Сюда вписываете вашу ссылку
        # Получаем загрузочную ссылку
        final_url = base_url + urlencode(dict(public_key=public_key))
        response = requests.get(final_url)
        download_url = response.json()['href']
        # Загружаем файл и сохраняем его
        download_response = requests.get(download_url)
        zip_path = 'text_recognize_yolo_2.zip'
        # print(download_response.content)
        with open(zip_path, 'wb') as f:
            f.write(download_response.content)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall()
        # weights_file_path = model_name + '_weights.pt'
        self.model = torch.hub.load(yolo_path, 'custom', 'best.pt', source='local')

        # for every text_class try to recognize text from all areas of text_class, length is depends on class and prod, returns string

    def work_image_cuts(self, number_image_cuts, l, h, w):
        """for every text_class try to recognize text from all areas of text_class, length is depends on class and prod, returns string """
        str = ''
        for number_image_cut in number_image_cuts:
            # cv2.imwrite('data/neuro_classes/cut.jpg', number_image_cut)
            cur_str = self.work_img_word(number_image_cut, h, w)
            if len(cur_str) == l:
                return cur_str
            if len(cur_str) > len(str):
                str = cur_str
        return str

        # main_method takes all image_text_areas from image_rama_cut and recognize text

    def work_image_cut(self, image_text_areas, image_rama_cut, number_l, number_h, number_w, prod_l, prod_h, prod_w, year_l, year_h, year_w):
        """main_method takes all image_text_areas from image_rama_cut and recognize text"""
        number_image_rects = image_text_areas.areas[Class_text.number]
        number_image_cuts = self.make_cuts(image_rama_cut, number_image_rects)
        number = self.work_image_cuts(number_image_cuts, number_l, number_h, number_w)
        prod_image_rects = image_text_areas.areas[Class_text.prod]
        prod_image_cuts = self.make_cuts(image_rama_cut, prod_image_rects)
        prod = self.work_image_cuts(prod_image_cuts, prod_l, prod_h, prod_w)
        year_image_rects = image_text_areas.areas[Class_text.year]
        year_image_cuts = self.make_cuts(image_rama_cut, year_image_rects)
        year = self.work_image_cuts(year_image_cuts, year_l, year_h, year_w)
        label_area = Label_area()
        label_area.labels[Class_text.number] = number
        label_area.labels[Class_text.prod] = prod
        label_area.labels[Class_text.year] = year
        return label_area

    def work_img_word(self, number_image_cut, number_h, number_w):
        h, w = number_image_cut.shape[:2]
        cv2.imwrite('img.jpg', number_image_cut)
        results = self.model(['img.jpg'], size=(number_h, number_w))
        json_res = results.pandas().xyxy[0].to_json(orient="records")
        res2 = json.loads(json_res)
        img_letters = Letters_In_Image.get_letters_in_image_from_yolo_json(res2)
        img_letters.sort_letters()
        img_letters.delete_intersections()
        os.remove('img.jpg')
        return img_letters.make_word()



    # cut text_areas imgs for each Rect from rect_array returns openCv imgs list
    def make_cuts(self, img_rama_cut, rect_array):
        """cut text_areas imgs for each Rect from rect_array returns openCv imgs list"""
        number_image_cuts = []
        for rect in rect_array:
            number_image_cuts.append(img_rama_cut[rect.ymin:rect.ymax, rect.xmin:rect.xmax])
        return number_image_cuts
        
