from vk_api import VkApi
from vk_api.exceptions import ApiError

from vk.models import User
from vk.tools.converters import dict_to_user

from search.models import UserSearchSettings


class VkTools:
    """Инструменты для работы с VK API от лица приложения

    Attributes:
        api: Обертка для работы с методами VK API
    """

    def __init__(self, api: VkApi) -> None:
        """Инициализирует экземпляр класса

        Args:
            api: Обертка для работы с методами VK API от лица приложения
        """

        self.api = api.get_api()

    def search_users(self, settings: UserSearchSettings) -> list[User] | None:
        """Находит пользователей по заданным параметрам

        Args:
            settings: Параметры поиска

        Returns:
            Найденные пользователи или None, если произошла ошибка API
        """

        min_age = settings.age - 3
        if settings.age >= 18:
            min_age = min(min_age, 18)

        try:
            found_users = self.api.users.search(
                city=settings.city,
                sex=(3 - settings.sex),
                status=6,
                age_from=min_age,
                age_to=settings.age + 3,
                offset=settings.offset,
                has_photo=True,
                fields=['relation', 'bdate', 'city', 'sex'],
            )
        except ApiError as e:
            print(f'Ошибка API: {e}')
            return None

        opened_users = [
            dict_to_user(u)
            for u in found_users['items']
            if not u['is_closed']
        ]

        return opened_users

    def get_user_info(self, user_id: int) -> User | None:
        """Возвращает информацию о пользователе с указанным ID

        Args:
            user_id: ID пользователя

        Returns:
            Информация о пользователе или None, если произошла ошибка API
        """

        try:
            user_info = self.api.users.get(
                user_ids=[user_id],
                fields=['bdate', 'city', 'sex']
            )[0]
        except ApiError as e:
            print(f'Ошибка API: {e}')
            return None

        return dict_to_user(user_info)

    def get_user_photos(self,
                        user_id: int,
                        limit: int = 3) -> list[str] | None:
        """Возвращает лучшие фотографии пользователя с указанным ID

        Args:
            user_id: ID пользователя
            limit: Максимальное количество фотографий

        Returns:
            Фотографии в формате вложений, описанном в документации VK API
        """

        try:
            photos = self.api.photos.get(
                owner_id=user_id,
                album_id='profile',
                extended=True,
            )
        except ApiError as e:
            print(f'Ошибка API: {e}')
            return None

        sorted_photos = sorted(
            photos['items'],
            key=lambda p: p['likes']['count'] + p['comments']['count'] * 2,
            reverse=True
        )[:limit]

        return [
            f'photo{p["owner_id"]}_{p["id"]}'
            for p in sorted_photos
        ]

    def get_city_id(self, name: str) -> int | None:
        """Находит ID города по указанному названию

        Args:
            name: Название города

        Returns:
            ID города или 0, если такого города не найдно, или None,
            если произошла ошибка API
        """
        query = name[:15]
        try:
            result = self.api.database.get_cities(q=query, count=1)
        except ApiError as e:
            print(f'Ошибка API: {e}')
            return None

        if not result['items']:
            return 0

        return result['items'][0]['id']
