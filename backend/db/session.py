from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from backend.db.base_class import Base
from backend.core.config import settings
from backend.models.user import *
from backend.models.files import *
from backend.models.idea import *
from backend.models.keywords import *


engine = create_engine(settings.DATABASE_URI)

if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # 4
