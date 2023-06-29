from enum import IntEnum


class Sex(IntEnum):
    """
    Перечисление всех доступных полов,
    согласно документации VK API
    """

    Unknown = 0
    Female = 1
    Male = 2


class Relation(IntEnum):
    """
    Перечисление всех доступных семейных положений,
    согласно документации VK API
    """

    Unknown = 0
    NotMarried = 1
    HasFriend = 2
    Engaged = 3
    Married = 4
    Complicated = 5
    ActivelyLooking = 6
    InLove = 7
    InCivilMarriage = 8
