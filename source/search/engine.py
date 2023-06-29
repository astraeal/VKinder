from vk.models import User
from vk.enums import Sex
from vk.tools.tools import VkTools

from database.utils import get_views, add_view

from search.models import UserSearchSettings


class SearchEngine:
    def __init__(self, tools: VkTools) -> None:
        self.tools = tools
        self.users = dict()

    def next(self, current_user: User) -> User:
        if current_user.id not in self.users:
            self.users[current_user.id] = {
                'settings': UserSearchSettings(
                    city=current_user.city_id,
                    sex=current_user.sex,
                    age=current_user.age,
                ),
                'queue': list()
            }

        if not self.users[current_user.id]['queue']:
            self.__fill_queue(current_user)

        selected_user = self.users[current_user.id]['queue'].pop()
        photos = self.tools.get_user_photos(selected_user.id)
        selected_user.photos = photos

        add_view(current_user.id, selected_user.id)

        return selected_user

    def __fill_queue(self, current_user: User) -> None:
        viewed = get_views(current_user.id)

        found_users = list()
        current_user_settings = self.users[current_user.id]['settings']
        while not found_users:
            found_users = self.tools.search_users(current_user_settings)
            found_users = [u for u in found_users if u.id not in viewed]
            current_user_settings.offset += current_user_settings.count

        sorted_users = sorted(
            found_users,
            key=lambda u: self.__rate_user(current_user, u)
        )
        self.users[current_user.id]['queue'] = sorted_users

    @classmethod
    def __rate_user(cls, current_user: User, other_user: User) -> int:
        score = 0

        if other_user.city_id:
            score += (current_user.city_id == other_user.city_id) * 5

        if other_user.age:
            score += (4 - abs(other_user.age - current_user.age)) // 2

        if other_user.sex:
            sex_score = 0
            if current_user.sex == Sex.Female:
                sex_score += other_user.sex == Sex.Male
            else:
                sex_score += other_user.sex == Sex.Female
            score += sex_score * 3

        return score
