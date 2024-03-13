from ultralytics import YOLO
import easyocr

detector = YOLO("modules/models/yolov8_detector.pt")
reader = easyocr.Reader(['ru'],
                        model_storage_directory='modules/models',
                        user_network_directory='modules/models',
                        recog_network='custom_ocr',
                        detector=False,
                        gpu=False,
                        )


def detect_number(image):
    labels_dict = {
    "0": "number"
    }
    numbers = detector(image)
    preds_list = []
    for number in numbers:
        prediction = {
        'x': int(number.to("cpu").numpy().boxes.xywh[:, 0][0]),
        'y': int(number.to("cpu").numpy().boxes.xywh[:, 1][0]),
        'w': int(number.to("cpu").numpy().boxes.xywh[:, 2][0]),
        'h': int(number.to("cpu").numpy().boxes.xywh[:, 3][0]),
        }
        prediction['confidence'] = str(number.to("cpu").numpy().boxes.conf[0])
        prediction['class'] = str((number.to("cpu").numpy().boxes.cls)[0].astype(int))
        prediction['name'] = prediction["class"].replace(prediction['class'], labels_dict[prediction['class']])
        preds_list.append(prediction)

    return preds_list

def recognize_digits_ocr(image):
    preds_list = []
    ocr_result = reader.recognize(image)
    conf = str(ocr_result[0][-1])
    digits = list(str(ocr_result[0][-2]))
    print(digits)
    for digit in digits:
        prediction = {
        'x': 0,
        'y': 0,
        'w': 0,
        'h': 0,
        }
        prediction['confidence'] = conf
        prediction['class'] = digit
        prediction['value'] = digit
        preds_list.append(prediction)

    return preds_list