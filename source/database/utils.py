from database.models import Viewed


def add_view(current_user_id: int, profile_user_id: int) -> None:
    Viewed.create(
        current_user_id=current_user_id,
        profile_user_id=profile_user_id
    )


def get_views(current_used_id: int) -> set[int]:
    result = Viewed.select(Viewed.profile_user_id) \
                .where(Viewed.current_user_id == current_used_id) \
                .execute()
    return {v.profile_user_id for v in result}
