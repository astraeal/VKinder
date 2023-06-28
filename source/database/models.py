from peewee import Model, SqliteDatabase
from peewee import (
    CompositeKey,
    IntegerField,
)

from core.contants import DATABASE_PATH


database = SqliteDatabase(DATABASE_PATH)


class BaseModel(Model):
    class Meta:
        database = database


class Viewed(BaseModel):
    current_user_id = IntegerField()
    profile_user_id = IntegerField()

    class Meta:
        primary_key = CompositeKey('current_user_id', 'profile_user_id')
