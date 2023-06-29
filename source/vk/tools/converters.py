from datetime import datetime, date

from vk.models import User
from vk.enums import Sex, Relation


def dict_to_user(raw_user: dict) -> User:
    """Преобразует словарь в пользователя

    Args:
        raw_user: Словарь, содержащий необходимые данные

    Returns:
        Пользователь, созданный из словаря
    """

    if raw_user['bdate'].count('.') == 2:
        today = date.today()
        bday = datetime.strptime(raw_user['bdate'], '%d.%M.%Y').date()

        had_bday_this_year = (today.month, today.day) < (bday.month, bday.day)
        age = today.year - bday.year - had_bday_this_year
    else:
        age = None

    fullname = f'{raw_user["first_name"]} {raw_user["last_name"]}'
    city_id = raw_user['city']['id'] if 'city' in raw_user else None
    sex = Sex(raw_user.get('sex', 0))
    relation = Relation(raw_user.get('relation', 0))

    return User(
        id=raw_user['id'],
        fullname=fullname,
        city_id=city_id,
        sex=sex,
        relation=relation,
        age=age,
    )
