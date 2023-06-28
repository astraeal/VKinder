import dotenv

from core.contants import REQUIRED_ENV_VARS
from core.utils.env import get_missing_env_vars

from database.helpers import initialize_database_if_needed


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


if __name__ == '__main__':
    main()
