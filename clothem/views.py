from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import numpy as np
from PIL import Image
from pathlib import Path
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import img_to_array

# Загрузка модели EfficientNetB0 с предобученными весами
model = EfficientNetB0(weights='imagenet')

BASE_DIR = Path(__file__).resolve().parent.parent

def main_page(request):
    if request.method == 'POST' and request.FILES.get('file_upload'):
        # Сохранение загруженного файла
        file = request.FILES['file_upload']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        print("Файл сохранен:", filename)
        file_path = fs.path(filename)

        # Открытие изображения и его подготовка для модели
        image = Image.open(file_path).convert('RGB').resize((224, 224))  # EfficientNet требует RGB и 224x224
        img_array = img_to_array(image)  # Преобразование в массив
        img_array = preprocess_input(img_array)  # Предобработка для EfficientNet
        img_array = np.expand_dims(img_array, axis=0)  # Добавление измерения batch

        # Предсказание с помощью модели
        prediction = model.predict(img_array)
        decoded_prediction = decode_predictions(prediction, top=1)[0]  # Декодирование результата
        predicted_label = decoded_prediction[0][1]  # Название класса
        confidence = decoded_prediction[0][2]  # Уверенность

        # Отображение результата на странице
        return render(request, 'answer_layout.html', {
            'label': predicted_label,
            'confidence': f"{confidence:.2%}",
            'image': '/media/' + filename
        })

    return render(request, 'main_page.html')
