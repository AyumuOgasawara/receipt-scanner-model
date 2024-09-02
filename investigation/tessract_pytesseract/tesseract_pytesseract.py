from PIL import Image, ImageEnhance

import cv2

import glob
import numpy as np

import pytesseract


LANG = "eng+jpn"


def preprocessing(image_path: str) -> Image.Image:
    """
    画像の前処理を行う
    """
    img = Image.open(image_path)
    img = img.convert("L")
    img = ImageEnhance.Contrast(img).enhance(2)

    cv2_img = np.array(img, dtype=np.uint8)
    cv2_img = cv2.fastNlMeansDenoising(cv2_img, None, 20)

    img = Image.fromarray(cv2_img)
    return img


def get_text(image: Image.Image) -> str:
    """
    画像データをtextに変換
    """
    return pytesseract.image_to_string(image, lang=LANG)


def scan(fp: str, out_dir: str) -> None:
    receipt_source_name = fp.split("/")[-1].replace(".jpeg", "")
    output_file_name = f"{out_dir}/{receipt_source_name}"

    # 画像の前処理
    preprocessed_image = preprocessing(fp)
    preprocessed_fp = f"{output_file_name}_preprocessed.png"
    preprocessed_image.save(preprocessed_fp)

    # textデータに変換
    text = get_text(preprocessed_image)
    with open(f"{output_file_name}.txt", "w") as f:
        f.writelines(text)


def main() -> None:
    out_dir = "output"
    for fp in glob.glob("raw/*"):
        scan(fp=fp, out_dir=out_dir)


if __name__ == "__main__":
    main()
