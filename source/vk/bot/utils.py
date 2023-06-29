import typing
from vk.enums import Sex
from vk.models import User

if typing.TYPE_CHECKING:
    from vk.bot.bot import VkBot


def get_states_queue(user_info: User) -> list[str]:
    queue = list()
    if user_info.age is None:
        queue.append({
            'name': 'input_age',
            'message': 'Введите свой возраст'
        })
    if user_info.city_id is None:
        queue.append({
            'name': 'input_city',
            'message': 'Введите свой город'
        })
    if user_info.sex is Sex.Unknown:
        queue.append({
            'name': 'input_sex',
            'message': 'Введите свой пол (М / Ж)'
        })
    return queue


def next_state_from_queue(user_id: int,
                          queue: list[str],
                          bot: 'VkBot') -> str:
    next_state = queue.pop()
    bot.send_message(user_id, next_state['message'])
    bot.states.set_state(user_id, next_state['name'])
    return next_state
