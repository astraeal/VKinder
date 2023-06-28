from database.models import Viewed
from database.models import database


def initialize_database_if_needed() -> None:
    database.create_tables([Viewed])
