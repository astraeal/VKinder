from dataclasses import dataclass, field
from typing import Optional

from vk.enums import Sex, Relation


@dataclass
class User:
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
