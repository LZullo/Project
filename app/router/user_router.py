import sys
sys.path.append('../')
from fastapi import APIRouter, Depends, Response, status
from app.schemas.user import User, UserOutput
from sqlalchemy.orm import Session
from app.router.deps import get_db_session
from app.use_cases.user import UserUseCases
from typing import List

router = APIRouter(prefix='/user', tags=['User'])

@router.post('/add', status_code=status.HTTP_201_CREATED, description="Add new user")
def add_user(
    user: User,
    db_session: Session = Depends(get_db_session)
):
    uc = UserUseCases(db_session=db_session)
    uc.add_user(user=user)
    return Response(status_code=status.HTTP_201_CREATED)

@router.get('/list', response_model= List[UserOutput], description='List user')
def list_user(
    db_session: Session = Depends(get_db_session)
):
    uc = UserUseCases(db_session=db_session)
    response = uc.list_user()
    return response

@router.delete('/delete/{id}', description='Delete user')
def delete_users(
    id : int,
    db_session: Session = Depends(get_db_session)
):
    uc = UserUseCases(db_session=db_session)
    uc.delete_users(id=id)
    
    return Response(status_code=status.HTTP_200_OK)