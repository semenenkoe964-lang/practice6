import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Pokemon

API_URL = 'https://pokeapi.co/api/v2/pokemon/'


def index(request):
    # Главная страница: список команды
    team = Pokemon.objects.all()
    return render(request, 'manager/index.html', {'team': team})


def search_pokemon(request):
    # Поиск покемона через API
    search_result = None
    error_msg = None

    if request.method == 'POST':
        query = request.POST.get('query', '').lower().strip()
        if query:
            response = requests.get(f'{API_URL}{query}')
            if response.status_code == 200:
                data = response.json()

                # Собираем данные для предпросмотра
                search_result = {
                    'name': data['name'],
                    'api_id': data['id'],
                    'sprite_url': data['sprites']['front_default'],
                    'hp': data['stats'][0]['base_stat'],  # hp обычно первый в stats
                    'attack': data['stats'][1]['base_stat'],  # attack второй
                    'defense': data['stats'][2]['base_stat'],  # defense третий
                }

                # Проверяем, есть ли он уже в команде
                if Pokemon.objects.filter(name=search_result['name']).exists():
                    search_result['exists'] = True
            else:
                error_msg = "Покемон не найден!"

    return render(request, 'manager/search.html', {'result': search_result, 'error': error_msg})


def add_pokemon(request):
    # Добавление в БД
    if request.method == 'POST':
        name = request.POST.get('name')
        # Повторная проверка, чтобы не добавлять дубликаты
        if not Pokemon.objects.filter(name=name).exists():
            Pokemon.objects.create(
                name=name,
                api_id=request.POST.get('api_id'),
                sprite_url=request.POST.get('sprite_url'),
                hp=request.POST.get('hp'),
                attack=request.POST.get('attack'),
                defense=request.POST.get('defense'),
            )
            messages.success(request, f'{name.title()} добавлен в команду!')
        else:
            messages.warning(request, f'{name.title()} уже в команде!')

    return redirect('index')


def remove_pokemon(request, pokemon_id):
    # Удаление из команды
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    pokemon.delete()
    messages.success(request, 'Покемон удален из команды.')
    return redirect('index')


def detail_pokemon(request, pokemon_id):
    # Детальная страница
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    return render(request, 'manager/detail.html', {'pokemon': pokemon})


def battle(request):
    # Страница битвы
    team = Pokemon.objects.all()
    winner = None
    fighter1 = None
    fighter2 = None
    log = []

    if request.method == 'POST':
        p1_id = request.POST.get('pokemon1')
        p2_id = request.POST.get('pokemon2')

        if p1_id and p2_id and p1_id != p2_id:
            fighter1 = get_object_or_404(Pokemon, id=p1_id)
            fighter2 = get_object_or_404(Pokemon, id=p2_id)

            # Простая логика боя: (Атака + HP) против (Атака + HP)
            power1 = fighter1.attack + fighter1.hp
            power2 = fighter2.attack + fighter2.hp

            log.append(f"{fighter1.name} (Сила: {power1}) против {fighter2.name} (Сила: {power2})")

            if power1 > power2:
                winner = fighter1
                log.append(f"Победил {fighter1.name}!")
            elif power2 > power1:
                winner = fighter2
                log.append(f"Победил {fighter2.name}!")
            else:
                log.append("Ничья!")
        else:
            messages.error(request, "Выберите двух разных покемонов.")

    return render(request, 'manager/battle.html', {
        'team': team,
        'winner': winner,
        'fighter1': fighter1,
        'fighter2': fighter2,
        'log': log
    })