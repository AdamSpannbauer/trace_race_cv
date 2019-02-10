from urllib.request import urlopen
from urllib.parse import urlparse
import cv2
import numpy as np


def draw_outlined_box(img, box_tuple, color_bgr=(0, 130, 255), outline_color=(91, 89, 88)):
    x, y, w, h = box_tuple
    cv2.rectangle(img, (x, y), (x + w, y + h), outline_color, thickness=3)
    cv2.rectangle(img, (x, y), (x + w, y + h), color_bgr, thickness=2)


def adjust_text_y(y, text_height, n_lines, line_index):
    if n_lines == 1:
        return y

    line_gap = text_height // 2
    total_height = (n_lines - 1) * (text_height + line_gap)

    line_adjustment = line_index * (line_gap + text_height)

    return y + line_adjustment - total_height // 2


def put_centered_text(img, text, size, color, thickness, font=cv2.FONT_HERSHEY_SIMPLEX):
    text = str(text)
    text_lines = text.split('\n')
    n_lines = len(text_lines)

    text_line_sizes = [cv2.getTextSize(l, font, size, thickness)[0] for l in text_lines]

    img_h, img_w = img.shape[:2]
    for i, text_size in enumerate(text_line_sizes):
        x = (img_w - text_size[0]) // 2
        y = (img_h + text_size[1]) // 2

        y = adjust_text_y(y, text_size[1], n_lines, i)

        cv2.putText(img, text_lines[i], (x, y), font, size, color, thickness)


def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def imread_anywhere(path):
    if is_url(path):
        req = urlopen(path)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)
    else:
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    return img
