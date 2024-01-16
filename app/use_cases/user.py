from app.db.models import User as UserModel
from app.schemas.user import User, UserOutput
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from fastapi import status

class UserUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_user(self, user: User):
        user_model = UserModel(**user.model_dump())
        self.db_session.add(user_model)
        self.db_session.commit()
        
    def list_user(self):
        user_on_db = self.db_session.query(UserModel).all()
        user_output = [
            self.serialize_user(user_model)
            for user_model in user_on_db
        ]
        return user_output
    
    def delete_users(self, id : int):
        user_model = self.db_session.query(UserModel).filter_by(id=id).first()

        if not user_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=('User not found'))
        
        self.db_session.delete(user_model)
        self.db_session.commit()

    def serialize_user(self, user_model: UserModel):
        return UserOutput(**user_model.__dict__)