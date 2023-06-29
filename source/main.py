import os
import dotenv
from vk_api import VkApi

from core.utils.env import get_missing_env_vars
from core.contants import (
    REQUIRED_ENV_VARS,
    APPLICATION_TOKEN_VAR,
    COMMUNITY_TOKEN_VAR
)

from database.helpers import initialize_database_if_needed
from vk.bot.bot import VkBot


def main() -> None:
    env_loaded = dotenv.load_dotenv()
    if not env_loaded:
        print(
            'Ошибка: не удалось загрузить переменные окружения, '
            'проверьте, существует ли файл .env'
        )

    missing_env_vars = get_missing_env_vars(REQUIRED_ENV_VARS)
    if missing_env_vars:
        print('Ошибка: отсутствуют необходимые переменные окружения:')
        for var in missing_env_vars:
            print(f'- {var}')
        return

    initialize_database_if_needed()

    application_api = VkApi(token=os.getenv(APPLICATION_TOKEN_VAR))
    community_api = VkApi(token=os.getenv(COMMUNITY_TOKEN_VAR))
    bot = VkBot(community_api, application_api)

    bot.run()


if __name__ == '__main__':
    main()
