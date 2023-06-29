from database.models import Viewed
from database.models import database


def initialize_database_if_needed() -> None:
    """Создает файл базы данных, а также таблицы в ней"""

    database.create_tables([Viewed])
