import cv2


def draw_outlined_box(img, box_tuple, color_bgr=(0, 130, 255), outline_color=(91, 89, 88)):
    x, y, w, h = box_tuple
    cv2.rectangle(img, (x, y), (x + w, y + h), outline_color, thickness=3)
    cv2.rectangle(img, (x, y), (x + w, y + h), color_bgr, thickness=2)



