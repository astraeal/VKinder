from collections import defaultdict


class StateStorage:
    """Хранилище состояний пользователей

    Attributes:
        states: Словарь состояний и данных каждого пользователя
    """

    def __init__(self) -> None:
        """Инициализирует экземпляр класса"""

        self.states = defaultdict(lambda: {
            'name': 'start',
            'data': dict()
        })

    def get_state(self, user_id: int) -> str:
        """Возвращает состояние по ID пользователя

        Args:
            user_id: ID пользователя

        Returns:
            Состояние пользователя
        """

        return self.states[user_id]['name']

    def set_state(self, user_id: int, state: str) -> None:
        """Устанавливает новое состояние по ID пользователя

        Args:
            user_id: ID пользователя
            state: Новое состояние
        """

        self.states[user_id]['name'] = state

    def get_data(self, user_id: int) -> dict:
        """Возвращает данные по ID пользователя

        Args:
            user_id: ID пользователя

        Returns:
            Данные пользователя
        """

        return self.states[user_id]['data']
