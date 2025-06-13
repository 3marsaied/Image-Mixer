import cv2

def resize_by_height(image, target_height):
    h, w = image.shape[:2]
    scale = target_height / h
    new_width = 2 * h
    resized_image = cv2.resize(image, (new_width, target_height), interpolation=cv2.INTER_AREA)
    return resized_image