import requests

pokemon_list_url = "https://pokeapi.co/api/v2/pokemon?limit=20"
response = requests.get(pokemon_list_url)

if response.status_code == 200:
    data = response.json()
    pokemons = data['results']

    print("Список первых 20 покемонов:")
    for i, pokemon in enumerate(pokemons, 1):
        print(f"{i}. {pokemon['name']}")

    pokemon_name = input("\nВведите название покемона: ").lower().strip()

    pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(pokemon_url)

    if response.status_code == 200:
        pokemon_data = response.json()

        # 4. Извлекаем и выводим данные
        name = pokemon_data['name']
        types = [t['type']['name'] for t in pokemon_data['types']]
        weight = pokemon_data['weight'] / 10  # переводим в кг
        height = pokemon_data['height'] / 10  # переводим в метры
        abilities = [a['ability']['name'] for a in pokemon_data['abilities']]

        print(f"\nИнформация о покемоне {name}:")
        print(f"Имя: {name}")
        print(f"Тип: {', '.join(types)}")
        print(f"Вес: {weight} кг")
        print(f"Рост: {height} м")
        print(f"Способности: {', '.join(abilities)}")

    else:
        print(f"Покемон с именем '{pokemon_name}' не найден.")

else:
    print("Ошибка при получении списка покемонов")
