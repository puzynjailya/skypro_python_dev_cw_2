import pytest
from utils import Posts
from exceptions import *


class Test_Post:

    def test_json_uploader(self):
        """
        Проверяем функцию загрузки файла json
        """
        posts = Posts()
        assert isinstance(posts.json_uploader(), list) == True, 'Возвращен неверный тип данных (не список)'

    def test_json_uploader_file_not_exist_error(self):
        """
        Проверяем наличие ошибки
        """
        posts = Posts()

        with pytest.raises(DataLoaderError):
            json_file = posts.json_uploader('./static/data/data_.json')



    def test_posts_search(self):
        """
        Проверяем функцию поиска постов
        """
        posts = Posts()
        target_word = '5000'
        target_post = {"poster_name": "larry",
                       "poster_avatar": "https://randus.org/avatars/m/81898dbdbdffdb18.png",
                       "pic": "https://images.unsplash.com/photo-1581235854265-41981cb85c88?ixlib=rb-1.2.1&ixid"
                              "=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=880&q=80",
                       "content": "Утром проснулся раньше всех – вижу у бассейна на вешалке висит оранжевое пальто. "
                                  "О, думаю – как это мое пальто за мной забралось так далеко – за целых 5000 "
                                  "километров. Присмотрелся – а это зонтик. И как только успел его сюда притащить! "
                                  "За завтраком сижу напротив своего попутчика, и все не решаюсь спросить его: "
                                  "«Может быть, мы все-таки не попутчики? Может, нам надо разъехаться в разные "
                                  "стороны? Вы не боитесь, что я сейчас сбегу?». Он не боится. Он вообще ничего не "
                                  "боится, кроме одного – когда у него в машине не работает сигнализация. А если она "
                                  "не работает, то он садится в машину и продолжает идти своим путем.",
                       "views_count": 366,
                       "likes_count": 198,
                       "pk": 4}
        matches = posts.posts_search(target_word)
        assert target_post in matches, 'Не работает функция поиска постов'

    def test_get_posts_by_user(self):
        """
        Проверяем работу поиск по имени пользователя
        """
        posts = Posts()
        user_name = 'leo'
        posts_list = posts.get_posts_by_user(user_name)

        # Если длина не очень, то выводим первый косячок
        # Опустим тест, т.к. в реальности количество постов может меняться
        # assert len(posts_list) == 2, 'Ошибка количества найденных постов'

        # Если имя не то, в найденных постах, то выводим  косячок
        for post in posts_list:
            assert post.get('poster_name') == user_name, f"Ошибка выполнения поиска по имени {user_name}"

    def test_get_comments_by_post_id(self):
        """
        Проверяем нахождение комментов по id поста
        """
        posts = Posts()
        post_id = 1
        comments_list = posts.get_comments_by_post_id(post_id=1)
        for comment in comments_list:
            assert comment.get('post_id') == post_id, f"Ошибка выполнения поиска комментария по ИД поста {post_id}"

    def test_get_post_by_pk(self):
        """
        Проверяем поиск поста по его ID
        """
        posts = Posts()
        post_id = 1
        post = posts.get_post_by_pk(post_id)
        assert post.get('pk') == post_id, f"Ошибка выполнения поиска по ИД поста {post_id}"

    def test_get_post_by_pk_id_error(self):
        """
        Проверяем на то, что появляется ошибка, если ид поста нет в списке
        """
        posts = Posts()
        post_id = 12
        with pytest.raises(IDDoesntExistError):
            post = posts.get_post_by_pk(post_id)

    def test_get_post_by_pk_type_error(self):
        """
        Проверяем на то, что появляется ошибка, если ид поста не того типа данных
        """
        posts = Posts()
        post_id = '1'
        with pytest.raises(TypeError):
            post = posts.get_post_by_pk(post_id)
