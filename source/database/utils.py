from database.models import Viewed


def add_view(current_user_id: int, profile_user_id: int) -> None:
    """Добавляет просмотр в базу данных

    Args:
        current_user_id: ID посмотревшего пользователя
        profile_user_id: ID просмотренного пользователя
    """

    Viewed.create(
        current_user_id=current_user_id,
        profile_user_id=profile_user_id
    )


def get_views(current_used_id: int) -> set[int]:
    """Возвращает ID пользователей, которых просмотрел current_user_id

    Args:
        current_used_id: ID пользователя

    Returns:
        Множество просмотренных ID пользователей
    """

    result = (
        Viewed.select(Viewed.profile_user_id)
        .where(Viewed.current_user_id == current_used_id)
        .execute()
    )
    return {v.profile_user_id for v in result}
