import logging
from backend.crud.crud_auth import AuthCRUD
from backend.crud.crud_user import UserCRUD
from backend.db.session import SessionLocal
from backend.schemas.schemas import UserRegister

logger = logging.getLogger(__name__)

FIRST_SUPERUSER = "admin"


def init_db() -> None:  # 1
    logger.info("Инициализация базы данных")
    if FIRST_SUPERUSER:
        session = SessionLocal()
        user_cruds = UserCRUD(session)
        user = user_cruds.get_user_by_username(FIRST_SUPERUSER)  # 2
        if not user:
            user_in = UserRegister(
                username=FIRST_SUPERUSER,
                first_name=FIRST_SUPERUSER,
                is_superuser=True,
                password="abobus123",
            )
            AuthCRUD(session).create_user(user_in)
            logger.info(f"Администратор {FIRST_SUPERUSER} создан")
        else:
            logger.warning(
                "Пропуск создания аккаунта администратора. Пользователь с юзернеймом "
                f"{FIRST_SUPERUSER} уже существует"
            )
    logger.info("Инициализация базы данных закончена")
