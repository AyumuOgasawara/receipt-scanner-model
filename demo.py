from PIL import Image, ImageEnhance

import pytesseract
import cv2
import os

import glob
import shutil

def preprocessing(image_path: str) -> Image:
    img = Image.open(image_path)
    img = ImageEnhance.Contrast(img).enhance(1.5)
    img = ImageEnhance.Sharpness(img).enhance(2)
    return img

def get_text(image: Image) -> str:
    return pytesseract.image_to_string(image, lang="jpn")

def get_bounding_boxes(image_path: str) -> cv2.typing.MatLike:
    img = cv2.imread(image_path)
    d = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, lang="jpn")
    n_boxes = len(d['level'])
    for i in range(n_boxes):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return img

if __name__ == "__main__":
    for i, fp in enumerate(glob.glob("raw/*.png")):
        output_file_dir = f"output/img0{i}"
        if not os.path.exists(output_file_dir):
            os.mkdir(output_file_dir)
        output_file_name = f"{output_file_dir}/img0{i}"
        preprocessed_image = preprocessing(fp)
        preprocessed_image.save(f"{output_file_name}_preprocessed.png")
        shutil.copyfile(fp, f"{output_file_name}.png")
        with open(f"{output_file_name}.txt", "w") as f:
            f.writelines(get_text(preprocessed_image))
        cv2.imwrite(f"{output_file_name}_boxes.png", get_bounding_boxes(fp))
        



import os
import sys
import pytesseract
from PIL import Image
from pytesseract import Output
import cv2

def image_to_text(image_path):
    # 画像を読み込む
    img = Image.open(image_path)

    # TesseractでOCRを実行
    text = pytesseract.image_to_string(img, lang='jpn')

    return text

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_dir_path = sys.argv[1]  # コマンドライン引数から画像ファイルのパスを取得
        file_list = [filename for filename in os.listdir(input_dir_path) if not filename.startswith('.')] 
        for filename in file_list:
            print(filename)
            plex = "png"
            if ".jpg" in "filename":
                plex = ".jpg"
            input_file_path = input_dir_path + "/" + filename
            output_file_dir = "output_dir/" + filename
            text = image_to_text(input_file_path)
            print(text)

            img = cv2.imread(input_file_path)
            d = pytesseract.image_to_data(img, output_type=Output.DICT)
            n_boxes = len(d['level'])
            for i in range(n_boxes):
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imwrite(output_file_dir, img)
    else:
        print("Usage: python app.py <path_to_image>")


