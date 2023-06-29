from dataclasses import dataclass


@dataclass
class UserSearchSettings:
    city: int
    sex: int
    age: int
    offset: int = 0
    count: int = 20
