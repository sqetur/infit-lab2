#Вариант 33
#задание №1 - Повышение резкости Unsharp Mask, задание №2 - выравнивание гистограммы
from datetime import datetime
import os
import cv2
import numpy as np

INPUT_DIR = r"Lab2_Media\data\input"
OUTPUT_DIR = r"Lab2_Media\data\output\result.jpg"
LOG_FILE = r"Lab2_Media\logs\history.txt"

FILTER = "Повышение резкости Unsharp Mask + Выравнивание гистограммы"

def write_log(filename, status):
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"[{now}] Файл: {filename} | Фильтр: {FILTER} | Статус: {status}\n")

def unsharp_mask(img):
    blurred = cv2.GaussianBlur(img, (0, 0), 3)
    return cv2.addWeighted(img, 1.5, blurred, -0.5, 0)

def equalize_hist(img):
    # выравняла только яркость, чтобы не исказить цвета
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
    return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)

filename = input("Какой файл обработать image1.jpg или image2.png : ").strip()
path = INPUT_DIR + "\\" + filename

try:
    if os.path.exists(path) and not os.access(path, os.W_OK):
        raise PermissionError
    with open(path, "rb") as f:
        data = f.read()
except PermissionError:
    print(f"Ошибка: Нет прав на чтение файла {filename}. Обратитесь к администратору")
    write_log(filename, "Ошибка доступа")
except FileNotFoundError:
    print("Ошибка: Файл не найден")
    write_log(filename, "Файл не найден")
else:
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        print("Ошибка: Файл не является изображением")
        write_log(filename, "Неверный формат")
    else:
        result = equalize_hist(unsharp_mask(img))
        cv2.imwrite(OUTPUT_DIR, result)
        print("Готово! Результат сохранён в", OUTPUT_DIR)
        write_log(filename, "Успешно")
