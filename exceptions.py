# Ошибка загрузки файла JSON
class DataLoaderError(Exception):
    pass


# Ошибка задания неверного формата ID поста
class PostIDCountError(Exception):
    pass


# Попытка поиска несуществуещего ID в постах
class IDDoesntExistError(Exception):
    pass

