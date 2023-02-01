from pydantic import AnyHttpUrl, BaseSettings, BaseModel
from typing import List, Literal, Optional, Tuple, get_args
from dotenv import dotenv_values


env_config = {**dotenv_values('.env'), **dotenv_values(".env.local"), }


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SERVER_LINK: str = 'http://localhost:3000'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ['http://localhost:4000']
    DATABASE_URI: Optional[str] = f"postgresql://{env_config['DB_USER']}:{env_config['DB_PASSWORD']}@{env_config['DB_HOST']}:{env_config['DB_PORT']}/{env_config['DB_NAME']}"
    TEST_DATABASE_URI: Optional[str] = f"{DATABASE_URI}_test"
    FIRST_SUPERUSER: str = "admin"
    ASSETS_FOLDER: str = 'assets/'
    IMAGES_FOLDER: str = ASSETS_FOLDER+'images'
    OTHER_FILES_FOLDER: str = ASSETS_FOLDER+'other'
    IMAGES_EXTENTION: str = '.png'
    UPLOADS_ROUTE: str = '/uploads'
    OTHER_FILES_ROUTE: str = '/other/'
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M"

    TEST_USER_USERNAME: str = "test_user"
    TEST_USER_USERNAME_2: str = "test_user_2"
    TEST_ADMIN_USERNAME: str = "test_admin"

    class Config:
        case_sensitive = True  # 4

    class JWTsettings(BaseModel):
        authjwt_secret_key: str = "secret"
        authjwt_token_location: set = {"cookies"}
        authjwt_cookie_csrf_protect: bool = False


settings = Settings()
