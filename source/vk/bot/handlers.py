import typing
from vk_api.longpoll import Event

from vk.enums import Sex
from vk.bot.utils import (
    get_next_state_by_user,
    get_prompt_by_state,
    change_state_and_send_prompt,
)

if typing.TYPE_CHECKING:
    from vk.bot.bot import VkBot


def start_handler(event: Event, bot: 'VkBot') -> None:
    bot.send_message(
        user_id=event.user_id,
        text='Приветствую! VKinder - это бот, который поможет тебе найти '
             'свою вторую половинку'
    )

    user_info = bot.tools.get_user_info(event.user_id)
    if user_info is None:
        bot.send_message(
            user_id=event.user_id,
            text='Произошла ошибка, попробуйте повторить позднее')
        return

    data = bot.states.get_data(event.user_id)
    data['info'] = user_info

    next_state = get_next_state_by_user(user_info)
    bot.states.set_state(event.user_id, next_state)

    if next_state != 'search':
        bot.send_message(
            user_id=event.user_id,
            text='Похоже, у тебя на странице есть не все нужные данные, '
                 'поэтому сейчас я попрошу тебя их отправить мне'
        )
        bot.send_message(event.user_id, get_prompt_by_state(next_state))
    else:
        search_handler(event, bot)


def input_city_handler(event: Event, bot: 'VkBot') -> None:
    city = event.text
    city_id = bot.tools.get_city_id(city)

    if city_id is None:
        bot.send_message(
            user_id=event.user_id,
            text='Произошла ошибка, попробуйте ввести город еще раз'
        )
        return

    if city_id == 0:
        bot.send_message(
            user_id=event.user_id,
            text='Такого города не найдено, попробуйте ввести город еще раз'
        )
        return

    user_info = bot.states.get_data(event.user_id)['info']
    user_info.city_id = city_id

    state = change_state_and_send_prompt(user_info, bot)
    if state == 'search':
        search_handler(event, bot)


def input_age_handler(event: Event, bot: 'VkBot') -> None:
    if not event.text.isdigit():
        bot.send_message(
            user_id=event.user_id,
            text='Ответ должен содержать только цифры, '
                 'попробуйте еще раз'
        )
        return

    age = int(event.text)
    if age < 16 or age > 100:
        bot.send_message(
            user_id=event.user_id,
            text='Возраст должен быть не меньше 16 лет, '
                 'но не больше 100 лет, попробуйте еще раз'
        )
        return

    user_info = bot.states.get_data(event.user_id)['info']
    user_info.age = age

    state = change_state_and_send_prompt(user_info, bot)
    if state == 'search':
        search_handler(event, bot)


def input_sex_handler(event: Event, bot: 'VkBot') -> None:
    raw_sex = event.text.lower()
    if raw_sex not in 'мж':
        bot.send_message(
            user_id=event.user_id,
            text='Пол может быть только "М" или "Ж", попробуйте еще раз'
        )
        return

    sex = Sex.Male if raw_sex == 'м' else Sex.Female

    user_info = bot.states.get_data(event.user_id)['info']
    user_info.sex = sex

    change_state_and_send_prompt(user_info, bot)
    search_handler(event, bot)


def search_handler(event: Event, bot: 'VkBot') -> None:
    current_user_profile = bot.states.get_data(event.user_id)['info']
    profile = bot.search.next(current_user_profile)
    bot.send_profile(event.user_id, profile)
    bot.send_message(
        user_id=event.user_id,
        text='Отправьте "Дальше", чтобы получить еще, '
             'или "Стоп", чтобы закончить'
    )


def stop_handler(event: Event, bot: 'VkBot') -> None:
    bot.send_message(
        user_id=event.user_id,
        text='Спасибо за использование бота!\n'
             'Чтобы снова его запустить, отправьте "Начать" или "Настройки"'
    )
    bot.states.set_state(event.user_id, 'stop')


def wrong_command_handler(event: Event, bot: 'VkBot') -> None:
    state = bot.states.get_state(event.user_id)
    if state == 'start':
        message = 'Чтобы начать использовать бота, отправьте "Начать"'
    elif state == 'stop':
        message = 'Чтобы снова запустить бота, отправьте "Начать"'
    elif state == 'search':
        message = ('Отправьте "Дальше", чтобы найти еще одного человека, '
                   'или "Стоп", чтобы закончить поиск')
    else:
        message = 'Ошибка, я не знаю такой команды'

    bot.send_message(
        user_id=event.user_id,
        text=message,
    )
