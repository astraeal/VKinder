from dataclasses import dataclass

from core.contants import USERS_PER_REQUEST


@dataclass
class UserSearchSettings:
    """Параметры поиска пользователей

    Attributes:
        city: ID города поиска
        sex: Номер пола, согласно документации VK API
        age: Возраст, относительно которого следует искать
        offset: Смещение поиска
        count: Количество найденных пользователей за один запрос
    """

    city: int
    sex: int
    age: int
    offset: int = 0
    count: int = USERS_PER_REQUEST
