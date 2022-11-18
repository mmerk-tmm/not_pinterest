from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String,  ForeignKey
from sqlalchemy.orm import relationship


class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String)
    original_file_name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", foreign_keys=[user_id])
    type = Column(String, default='file')
