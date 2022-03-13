from app import app
import random
import pytest

# Задаем список ключей для проверки
dict_keys = ["poster_name", "poster_avatar", "pic", "views_count", "likes_count", "pk"]

# Задаем случайное значение поста для теста
test_value = random.randint(1,7)


# Выполняем проверку выдачи всех постов
def test_all_posts():
    response = app.test_client().get('/api/posts')

    assert response.status_code == 200, 'Ошибка ответа'
    assert isinstance(response.json, list) == True, 'Возвращен неверный тип данных (не список)'

    for data in response.json:
        for key in dict_keys:
            assert key in list(data.keys()), f'Ошибка ключа {key} вложенного словаря'


# Выполняем проверку выдачи одного поста
def test_single_post():
    response = app.test_client().get(f'/api/posts/{test_value}')
    assert response.status_code == 200, 'Ошибка ответа'
    assert isinstance(response.json, dict) == True, 'Возвращен неверный тип данных (не словарь)'

    for key in dict_keys:
        assert key in list(response.json.keys()), f'Ошибка ключа {key} вложенного словаря'
