import numpy as np
from VAR import *
from PIL import Image
from collections import Counter
from tesser import tesser_predict


def get_info_class(detector, PATH):
    img = Image.open(PATH)
    img_arr = np.array(img.resize((detector.network_width(), detector.network_height())))
    detections = detector.perform_detect(image_path_or_buf=img_arr, show_image=False)
    detections_name = []
    for detection in detections:
        box = detection.left_x, detection.top_y, detection.width, detection.height
        detections_name.append(detection.class_name)
    return detections_name


def get_cost(names):
    if names:
        low_class = [x.lower() for x in names]
        #print(f'Задетектили {low_class}')
        #print (f' Результат работы tesser_predict {tesser_predict(PATH)}')
        
        if tesser_predict(PATH):
            weight = int(tesser_predict(PATH))/ 1000
            price = {key: round(Counter(low_class)[key]*INFO[key.lower()][0]*weight, 2) for key in Counter(low_class).keys()}
            label = list(price.keys())[0]
        else:
            price = {key: round(Counter(low_class)[key]*INFO[key.lower()][0]*INFO[key.lower()][1], 2) for key in Counter(low_class).keys()}
            label = list(price.keys())[0]
        print (f'Вы выбрали {OUT_INFO[label]} на сумму {price[label]} рублей.')
        return OUT_INFO[label], price[label]     
    else:
        return 0, 0        