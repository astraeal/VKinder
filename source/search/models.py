from dataclasses import dataclass

from core.contants import USERS_PER_REQUEST


@dataclass
class UserSearchSettings:
    city: int
    sex: int
    age: int
    offset: int = 0
    count: int = USERS_PER_REQUEST
