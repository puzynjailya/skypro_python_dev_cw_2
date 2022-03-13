import json  # Импортируем json для работы с файлами json
from exceptions import *  # Импортируем исключения
import re


class Posts:
    """
    Класс Posts предназначен для создания объектов постов и их обработки
    """

    def __init__(self, path=None):
        if path is None:
            path = './static/data/data.json'
            self.path = path
            self.all_posts = self.json_uploader()

    def json_uploader(self, path=None):
        """
        Загрузчик файлов JSON
        :param path: путь к файлу, по умолчанию = None. Может быть задан вручную
        :return: загруженный и обработанный файл json
        """
        # Если задан путь к файлу, то открываем по новому пути
        if path is not None:
            self.path = path
        # Пробуем открыть файл
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                return json.load(file)
        # Если ошибка, что файл не json или файл не найден, то создаем ошибку
        except (json.JSONDecodeError, FileNotFoundError):
            raise DataLoaderError(f'Ошибка загрузки файла')

    def posts_search(self, target_word):
        """
        Метод предназначен для поиска постов по ключевому слову
        """
        # Подгружаем все посты
        # all_posts = self.json_uploader()

        # Обновляем данные с хештегами
        self.all_posts = self.update_hashtags()

        # Разделяем, если юзер ввел несколько слов через пробел
        target_word = target_word.replace(',', ' ').split(' ')

        # Создаем пустой список, куда будем складывать слова
        match_list = []

        # Проходимся циклом и добавляем найденные данные в список постов
        for word in target_word:
            for data in self.all_posts:
                if word.lower() in data.get('content').lower():
                    match_list.append(data)
        return match_list

    '''
    def get_posts_all(self):
        
        Получает файл json и добавлеяет поле с укороченной информацией
        :return:
        
        #all_posts = self.json_uploader()
        for post in self.all_posts:
            if len(post["content"]) >= 25:
                post["short_description"] = post["content"][:22] + 3 * "."
        return self.all_posts
    '''

    def get_posts_by_user(self, user_name):
        """
        возвращает посты определенного пользователя
        :param user_name: имя пользователя
        :return: список постов определеного пользователя
        """
        self.all_posts = self.update_hashtags()
        # Создаем пустой список, куда будем складывать посты пользователя
        users_posts = []
        # Проходим циклом по распаршеому файлу json с постами и показываем все посты пользователя
        for post in self.all_posts:
            if post.get('poster_name').lower() == user_name.lower():
                users_posts.append(post)
        return users_posts

    def get_comments_by_post_id(self, post_id):
        """
        Метод поиска комментариев по связанному с ним ИД
        :param post_id: идентификтор поста
        :return: список комментариев к посту по его ИД
        """

        # Проверим, что мы задаем правильный формат идентификатора
        if not isinstance(post_id, int):
            raise TypeError('Ошибка ввода идентификатора поста')

        # Создаем бланк списка комментов
        comments_list = []
        # Подгружаем файл с комментариями
        decoded_comments = self.json_uploader('./static/data/comments.json')
        # Проходимся циклом по распаршеному файлу с комментариями и сохраняем совпадения по post_id
        for comment_data in decoded_comments:
            if comment_data.get('post_id') == post_id:
                comments_list.append(comment_data)

        return comments_list

    def get_post_by_pk(self, id):
        """
        Метод поиска поста по его ИД
        :param id: идентификатор искомого поста
        :return: данные из файла json с постом по ИД
        """

        # Проверим, что мы задаем правильный формат идентификатора
        if not isinstance(id, int):
            raise TypeError('Ошибка ввода идентификатора поста')

        # Задаем счетчик идентификаторов, чтобы проверить на дубли постов b
        counter = 0
        post_by_id = {}

        # Загружаем файл с постами
        # all_posts = self.json_uploader()
        self.all_posts = self.update_hashtags()
        # Проходимся по всем постам и ищем совпадение по id и pk
        for post_data in self.all_posts:
            if post_data['pk'] == id:
                post_by_id = post_data
                counter += 1
        # Если счетчик == 0, т.е. не найдено постов, то выводим ошибку
        if counter == 0:
            raise IDDoesntExistError('Такого ID нет в списке постов')
        # Если счетчик > 1, то выводим ошибку
        if counter > 1:
            raise PostIDCountError('Ошибка в данных JSON файла')

        return post_by_id

    def update_hashtags(self):
        """
        Метод обновления хештегов на html код
        :return: данные из файла json с постом по ИД
        """

        def search_hashtag(data):
            match_list = re.findall(r'#[\w]*', data.get('content'))
            if match_list:
                for tag in match_list:
                    url = f'<a href="/tag/{{{tag[1:]}}}">{tag}</a>'
                    data['content'] = data['content'].replace(tag, url)
            return data

        for post in self.all_posts:
            post = search_hashtag(post)
        return self.all_posts

    def posts_search_by_hashtag(self, hashtag):
        """
        Метод предназначен для поиска постов по хештегу
        :param hashtag : str - искомый тег
        :return match_list : list - список найденных постов
        """

        # Обновляем данные с хештегами
        self.all_posts = self.update_hashtags()

        # Создаем пустой список, куда будем складывать слова
        match_list = []

        # Проходимся циклом и добавляем найденные данные в список постов
        for data in self.all_posts:
            if hashtag in data.get('content'):
                match_list.append(data)
        return match_list


    def add_data_to_json(self, post):
        """
        Метод предназначен для записи данных закладки в файл JSON
        :param post: dict - данные поста, хранящиеся в JSON файле
        """
        bookmarks = self.json_uploader(path='./static/data/bookmarks.json')
        if post not in bookmarks:
            bookmarks.append(post)
            with open(file='./static/data/bookmarks.json', mode='w', encoding='utf-8') as file:
                json.dump(bookmarks, file)


    def remove_data_from_json(self, post):
        """
        Метод предназначен для удаления данных закладки из файла JSON
        :param post: dict - данные поста, хранящиеся в JSON файле
        """
        bookmarks = self.json_uploader(path='./static/data/bookmarks.json')
        if post in bookmarks:
            bookmarks.remove(post)
            with open(file='./static/data/bookmarks.json', mode='w', encoding='utf-8') as file:
                json.dump(bookmarks, file)
