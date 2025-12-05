import requests
from django.shortcuts import render


# Функция для получения списка всех пород с API
def get_breeds():

    url = "https://dog.ceo/api/breeds/list/all"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'success':
            breeds = []

            # Итерация по всем породам из ответа API
            for breed, sub_breeds in data['message'].items():
                breeds.append(breed)

                # Добавление подпород (если есть)
                for sub_breed in sub_breeds:
                    breeds.append(f"{breed}/{sub_breed}")

            return breeds
    return []


# Функция для получения изображений конкретных пород
def get_dog_images(breeds):
    images = []  # Список для хранения информации об изображениях

    # Обработка каждой породы из списка
    for breed in breeds:
        breed_clean = breed.strip().lower().replace(' ', '')

        # Определение URL в зависимости от типа породы
        if '/' in breed_clean:
            main_breed, sub_breed = breed_clean.split('/')  # Разделение на основную и подпороду
            url = f"https://dog.ceo/api/breed/{main_breed}/{sub_breed}/images/random"
        else:
            url = f"https://dog.ceo/api/breed/{breed_clean}/images/random"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                images.append({
                    'breed': breed,
                    'image_url': data['message']
                })

    return images


# Основная view-функция для главной страницы
def home(request):
    if request.method == 'POST':
        breeds_input = request.POST.get('breeds', '')

        # Преобразование строки в список пород
        breeds_list = [b.strip() for b in breeds_input.split(',') if b.strip()]

        if breeds_list:
            images = get_dog_images(breeds_list)

            # Подготовка контекста для шаблона
            context = {
                'breeds': get_breeds(),  # Список всех доступных пород
                'selected_breeds': breeds_list,  # Введенные пользователем породы
                'images': images  # Полученные изображения
            }
            return render(request, 'home.html', context)

    context = {
        'breeds': get_breeds()
    }

    return render(request, 'home.html', context)
