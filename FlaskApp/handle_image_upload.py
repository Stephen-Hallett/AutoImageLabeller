import cv2 as cv
import os
import numpy as np

def handle_upload(filename, obj_filename, label,remove=False):
    img = cv.imread(filename)
    obj = cv.imread(obj_filename, cv.IMREAD_UNCHANGED)
    if obj.shape[1:-1] == img.shape[:1]:
        obj = cv.rotate(obj, cv.ROTATE_90_CLOCKWISE)

    try:
        scale = obj[:, :, 3]
        object_area = np.where(scale == 255)
    except:
        scale = cv.cvtColor(obj, cv.COLOR_BGR2GRAY)
        object_area = np.where(scale < 255)

    min_x = min(object_area[1])
    min_y = min(object_area[0])
    max_x = max(object_area[1])
    max_y = max(object_area[0])

    print(os.path.join("results",os.path.basename(filename)))

    width=obj.shape[1]
    height = obj.shape[0]
    yolo_height = (max_y-min_y)/height
    yolo_width = (max_x-min_x)/width
    yolo_center_y = ((min_y+max_y) * 0.5)/height
    yolo_center_x = ((min_x+max_x) * 0.5)/width

    label = " ".join(map(str,[label, yolo_center_x, yolo_center_y, yolo_width, yolo_height]))
    base = filename[:filename.rfind(".")]
    cv.imwrite(base+".jpg", img)
    with open(base+".txt", "w") as f:
        f.write(label)

    cv.rectangle(img, (min_x, min_y), (max_x, max_y), color=(255,0,0), thickness=4)
    example_file = base[:-1]+"example.jpg"
    cv.imwrite(example_file, img)

    if remove:
        os.remove(filename)
        os.remove(obj_filename)

    return example_file
    
