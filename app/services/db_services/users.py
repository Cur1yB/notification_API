from app.models.users import User

async def get_by_username(*, username: str) -> User | None:
    return await User.filter(username=username).first()


async def create_user(*, username: str, password_hash: str, avatar_url: str) -> User:
    return await User.create(username=username, password_hash=password_hash, avatar_url=avatar_url)
