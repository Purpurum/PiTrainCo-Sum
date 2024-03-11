from modules.detectors import detect_number, recognize_digits_ocr

import numpy as np
from PIL import Image


def crop_image(image, x_center, y_center, width, height):
    left = x_center - width // 2
    top = y_center - height // 2
    right = x_center + width // 2
    bottom = y_center + height // 2
    cropped_image = image.crop((left, top, right, bottom))

    return cropped_image

def choose_valid_num(numbers_parameters):
    if len(numbers_parameters) > 1:
        chosen_pars = numbers_parameters[0]
        for number in numbers_parameters:
            width = number["w"]
            height = number["h"]
            if (width / height) > 3:
                chosen_pars = number
        return chosen_pars

    else:
        return numbers_parameters[0]

def extract_num_parameters(number_par):
    pars_dict = {}
    pars_dict["confidence"] = number_par["confidence"]
    pars_dict["height"] = number_par["h"]
    pars_dict["width"] = number_par["w"]
    pars_dict["number_center_x"] = number_par["x"]
    pars_dict["number_center_y"] = number_par["y"]

    return pars_dict

def extract_digit_parameters(digits):
    digits_list = []
    for digit in digits:
        digit_dict = {}
        value = digit["value"]
        digit_dict["confidence"] = float(digit["confidence"])
        digit_dict["digit_center_x"] = digit["x"]
        digit_dict["digit_center_y"] = digit["y"]
        digit_dict["height"] = digit["h"]
        digit_dict["is_valid"] = value.isdigit()
        digit_dict["value"] = value
        digit_dict["width"] = digit["w"]
        digits_list.append(digit_dict)
    return digits_list

def form_final_dict(number_pars, digits, image):
    res_dict = {}
    number = create_string_number(digits)
    res_dict["confidence"] = float(number_pars["confidence"])
    res_dict["digits"] = digits
    res_dict["height"] = number_pars["height"]
    res_dict["img_height"] = image.size[1]
    res_dict["img_name"] = "name.jpg"
    res_dict["img_type"] = "jpg"
    res_dict["img_width"] = image.size[0]
    res_dict["is_rule_complete"] = is_valid(number)
    res_dict["is_valid"] = res_dict["is_rule_complete"]
    res_dict["number"] = number
    res_dict["number_center_x"] = number_pars["number_center_x"]
    res_dict["number_center_y"] = number_pars["number_center_y"]
    res_dict["width"] = number_pars["width"]
    
    return [res_dict]

def create_string_number(digits):
    string = ""
    for digit in digits:
        string = string + digit["value"]
    return string

def is_valid_old(result):
    if not result:
        return 0

    cont_sum = 0
    control_num = -1

    if len(result) == 8:
        control_num = int(result[-1:])
        cont_sum = 0
        for i in range(7):
            num = int(result[i]) * (2, 1)[i % 2 == 1]
            if num >= 10:
                cont_sum += sum(list(map(int, set(str(num)))))
            else:
                cont_sum += num
    result = int((cont_sum % 10 == 0 and control_num == 0) or (10 - cont_sum % 10) == control_num)
    if result == 0:
        return False
    else:
        return True
    
def is_valid(result):
    if not result:
        return False

    cont_sum = 0
    control_num = -1

    if len(result) == 8:
        control_num = int(result[-1])
        for i in range(7):
            num = int(result[i]) * (2 if i % 2 == 0 else 1)
            if num >= 10:
                # Исправлено: теперь суммируем все цифры числа напрямую, без преобразования в множество.
                cont_sum += sum(int(digit) for digit in str(num))
            else:
                cont_sum += num

    is_valid_number = (cont_sum % 10 == 0 and control_num == 0) or (10 - cont_sum % 10) == control_num
    return is_valid_number

def process_image(image):
    numbers_parameters = detect_number(image)
    number_parameters = choose_valid_num(numbers_parameters)
    number_image = crop_image(image, number_parameters["x"], number_parameters["y"], number_parameters["w"], number_parameters["h"])
    image_array = np.array(number_image)
    digits_pars = recognize_digits_ocr(image_array)
    number_pars = extract_num_parameters(number_parameters)
    digits = extract_digit_parameters(digits_pars)
    result = form_final_dict(number_pars, digits, image)
    return result