import cv2


def draw_outlined_box(img, box_tuple, color_bgr=(0, 130, 255), outline_color=(91, 89, 88)):
    x, y, w, h = box_tuple
    cv2.rectangle(img, (x, y), (x + w, y + h), outline_color, thickness=3)
    cv2.rectangle(img, (x, y), (x + w, y + h), color_bgr, thickness=2)


def put_centered_text(img, text, size, color, thickness, font=cv2.FONT_HERSHEY_SIMPLEX):
    text = str(text)
    text_size = cv2.getTextSize(text, font, size, thickness)[0]

    x = (img.shape[1] - text_size[0]) // 2
    y = (img.shape[0] + text_size[1]) // 2

    cv2.putText(img, text, (x, y), font, size, color, thickness)
