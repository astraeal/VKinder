from typing import Optional

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from vk.bot.states import StateStorage
from vk.bot.handlers import (
    start_handler,
    input_city_handler,
    input_age_handler,
    search_handler,
    stop_handler,
    wrong_command_handler,
)

from vk.models import User
from vk.tools.tools import VkTools

from search.engine import SearchEngine


class VkBot:
    def __init__(self, community_api: VkApi, application_api: VkApi) -> None:
        self.api = community_api.get_api()
        self.tools = VkTools(application_api)
        self.search = SearchEngine(self.tools)
        self.states = StateStorage()

    def send_message(self,
                     user_id: int,
                     text: str,
                     attachments: Optional[list[str]] = None) -> None:
        self.api.messages.send(
            user_id=user_id,
            message=text,
            attachment=attachments,
            random_id=get_random_id())

    def send_profile(self, user_id: int, profile: User) -> None:
        age_text = ''
        if profile.age:
            age_text = f', {profile.age} '
            tens = profile.age % 100 // 10
            units = profile.age % 10
            if tens == 1 or units in (0, 5, 6, 7, 8, 9):
                age_text += 'лет'
            elif units == 1:
                age_text += 'год'
            else:
                age_text += 'года'

        self.send_message(
            user_id=user_id,
            attachments=profile.photos,
            text=f'{profile.fullname}{age_text}\n'
                 f'Ссылка: {profile.url}'
        )

    def run(self) -> None:
        longpoll = VkLongPoll(self.api._vk)

        for event in longpoll.listen():
            if event.type != VkEventType.MESSAGE_NEW or not event.to_me:
                continue

            user_id = event.user_id
            state = self.states.get_state(user_id)
            text = event.text.lower()

            if text in ('начать', 'настройки'):
                start_handler(event, self)
            elif state == 'input_city':
                input_city_handler(event, self)
            elif state == 'input_age':
                input_age_handler(event, self)
            elif state == 'search' and text == 'дальше':
                search_handler(event, self)
            elif state == 'search' and text == 'стоп':
                stop_handler(event, self)
            else:
                wrong_command_handler(event, self)
