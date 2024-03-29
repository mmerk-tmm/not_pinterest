from typing import Any, List

from backend.db.base_class import Base


class CRUDBase:
    def __init__(self, db) -> None:
        self.db = db

    def get(self, id: Any, model):
        return self.db.query(model).filter(model.id == id).first()

    def get_multi(
            self, model, skip: int = 0, limit: int = 100, ) -> List:
        return self.db.query(model).offset(skip).limit(limit).all()  # 4

    def create(self,  model):
        self.db.add(model)
        self.db.commit()  # 5
        self.db.refresh(model)
        return model

    def delete(self, model):
        self.db.delete(model)
        self.db.commit()
    
    def update(self, model):
        self.db.refresh(model)
        self.db.commit()
        return model
