import numpy as np
import face_recognition
from PIL import Image

# アスペクト比固定で縮尺変える
def scale_to_width(img, width):
    height = round(img.height * width / img.width)
    return img.resize((width, height))

# 読み込んだ画像にちんぽを縮尺変えて貼り付ける
def paste_chinpo(img):
    #chinpo = Image.open("back/image/chinpo.jpg") #デバッグ用
    chinpo = Image.open("image/chinpo.jpg")
    face_bboxes = face_recognition.face_locations(np.asarray(img))

    for xy in face_bboxes:
        workChinpo = scale_to_width(chinpo, xy[1]-xy[3])
        img.paste(workChinpo, (xy[3],xy[0]))
    
    return img