import typing

from vk.enums import Sex
from vk.models import User

if typing.TYPE_CHECKING:
    from vk.bot.bot import VkBot


def get_next_state_by_user(user_info: User) -> str:
    """Проверяет какие данные пользователя не заполнены
    и возвращает соответствующее состояние для получения данных

    Args:
        user_info: Информация о пользователе

    Returns:
        Следующее состояние
    """

    if user_info.city_id is None:
        return 'input_city'
    if user_info.age is None:
        return 'input_city'
    if user_info.sex == Sex.Unknown:
        return 'input_sex'
    return 'search'


def get_prompt_by_state(state: str) -> str:
    """Возвращает приглашение ко вводу в зависимости от состояния пользователя

    Args:
        state: Состояние пользователя

    Returns:
        Приглашение ко вводу
    """

    return {
        'input_city': 'Введите свой город',
        'input_age': 'Введите свой возраст',
        'input_sex': 'Введите свой пол (М / Ж)'
    }.get(state, 'Спасибо за терпение, приступаем к поиску!')


def change_state_and_send_prompt(user: User, bot: 'VkBot') -> str:
    """Изменяет состояние указанного пользователя на следующее
    и отправляет нужное приглашение ко вводу

    Args:
        user: Пользователь, состояние которого необходимо изменить
        bot (VkBot): Чат-бот

    Returns:
        Новое состояние пользователя
    """

    next_state = get_next_state_by_user(user)
    bot.states.set_state(user.id, next_state)
    bot.send_message(user.id, get_prompt_by_state(next_state))
    return next_state
