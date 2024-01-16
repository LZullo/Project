import sys
sys.path.append('../')
from app.use_cases.user import UserUseCases
from app.db.models import User as UserModel
from app.schemas.user import User, UserOutput
from datetime import date
import pytest
from fastapi.exceptions import HTTPException

def test_add_user_uc(db_session):
    uc = UserUseCases(db_session)
    
    user = User(
        
        cpf=42876987955, 
        name='Joao', 
        birth_date='1997-10-15'
    )

    uc.add_user(user=user)

    user_on_db = db_session.query(UserModel).all()
    assert len(user_on_db) == 1
    assert user_on_db[0].cpf == 42876987955
    assert user_on_db[0].name == 'Joao'
    assert user_on_db[0].birth_date == date(1997,10,15)

    db_session.delete(user_on_db[0])
    db_session.commit()

def test_list_user(db_session, user_on_db):
    uc = UserUseCases(db_session=db_session)
    
    users = uc.list_user()

    assert len(users)==4
    assert type(users[0]) ==UserOutput
    assert users[0].id == user_on_db[0].id
    assert users[0].cpf == user_on_db[0].cpf
    assert users[0].name == user_on_db[0].name
    assert users[0].birth_date ==  user_on_db[0].birth_date

def test_delete_users(db_session):
    user_model = UserModel(cpf = 42876987965, name = 'Joao', birth_date ='1997-10-25')
    db_session.add(user_model)
    db_session.commit()

    uc = UserUseCases(db_session=db_session)
    uc.delete_users(id=user_model.id)

    user_model = db_session.query(UserModel).first()
    assert user_model is None

def test_delete_users_non_exist(db_session, salaries_on_db):
    uc = UserUseCases(db_session=db_session)
    with pytest.raises(HTTPException):
        uc.delete_users(id=1)

   