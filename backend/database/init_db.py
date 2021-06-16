from sqlalchemy.orm import Session

from schemas.internal import UserCreate
from crud import user as _user
from core.config import settings


async def init_db(db: Session):
    user = await _user.get_by_username(db, username=settings.FIRST_SUPERUSER)
    if user is None:
        superuser = UserCreate(
            username=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_active=True,
            is_superuser=True
        )
        user = await _user.create(db, user=superuser)
