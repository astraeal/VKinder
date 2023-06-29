from dataclasses import dataclass, field
from typing import Optional

from vk.enums import Sex, Relation


@dataclass
class User:
    """Пользователь

    Attributes:
        id: ID в ВК
        fullname: Полное имя
        sex: Пол
        relation: Семейное положение
        age: Возраст
        city_id: ID города
        photos: Список фотографий
        url: Ссылка на страницу ВК
    """

    id: int
    fullname: str
    sex: Sex
    relation: Relation
    age: Optional[int]
    city_id: Optional[int]
    photos: list[str] = field(default_factory=list)

    @property
    def url(self) -> str:
        return f'https://vk.com/id{self.id}'
