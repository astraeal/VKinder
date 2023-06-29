from collections import defaultdict


class StateStorage:
    def __init__(self) -> None:
        self.states = defaultdict(lambda: {
            'name': 'start',
            'data': dict()
        })

    def get_state(self, user_id: int) -> str:
        return self.states[user_id]['name']

    def set_state(self, user_id: int, state: str) -> None:
        self.states[user_id]['name'] = state

    def get_data(self, user_id: int) -> dict:
        return self.states[user_id]['data']
