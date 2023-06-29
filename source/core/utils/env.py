import os


def get_missing_env_vars(variables: list[str]) -> list[str]:
    """Находит переменные окружения из списка, которые не были инициализированы

    Args:
        variables: Список названий переменных окружения

    Returns:
        Список неинициализированных переменных окружения
    """
    missing_vars = list()
    for var in variables:
        if os.getenv(var) is None:
            missing_vars.append(var)
    return missing_vars
