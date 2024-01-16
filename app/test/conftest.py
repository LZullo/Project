import sys
sys.path.append('../')
import pytest
from app.db.connection import Session
from app.db.models import User as UserModel
from app.db.models import Salaries as SalariesModels

@pytest.fixture()
def db_session():
    try:
        session = Session()
        yield session
    finally:
        session.close()

@pytest.fixture()
def user_on_db(db_session):
    
    users = [
        UserModel( cpf = 42876987965, name = 'Joao', birth_date ='1997-10-25'),
        UserModel( cpf = 42876987100, name = 'Aline Souza', birth_date ='2000-12-13'),
        UserModel( cpf = 42876987101, name = 'José Ferreira', birth_date ='1993-11-28'),
        UserModel( cpf = 42876987102, name = 'Abílio Mendes', birth_date ='1989-10-25'),
    ]

    for user in users:
        db_session.add(user)
    db_session.commit()

    for user in users:
        db_session.refresh(user)

    yield users

    for user in users:
        db_session.delete(user)
    db_session.commit()

@pytest.fixture()
def salaries_on_db(db_session):
    user = UserModel(cpf = 42876987965, name = 'Joao', birth_date ='1997-10-25')

    db_session.add(user)
    db_session.commit()

    salaries = SalariesModels(
        salarie_date ='1997-10-25', 
        value_salarie = 1000,
        discount =  100,
        cpf_id = user.cpf
        )
    db_session.add(salaries)
    db_session.commit()

    yield salaries

    db_session.delete(salaries)
    db_session.delete(user)
    db_session.commit()

@pytest.fixture()
def salaries_on_db_list(db_session):
    user= UserModel(cpf = 42876987965, name = 'Joao', birth_date ='1997-10-25')

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)


    salaries = [
        SalariesModels(salarie_date ='1997-10-25', value_salarie = 1000, discount =  100, cpf_id=user.cpf),
        SalariesModels(salarie_date ='1998-11-12', value_salarie = 100, discount =  10, cpf_id=user.cpf),
        SalariesModels(salarie_date ='2000-12-13', value_salarie = 1010, discount =  0, cpf_id=user.cpf),
        SalariesModels(salarie_date ='1999-9-17', value_salarie = 1080, discount =  5, cpf_id=user.cpf)
        
   ]

    for salarie in salaries:
        db_session.add(salarie)
    db_session.commit()

    for salarie in salaries:
        db_session.refresh(salarie)

    yield salaries

    for salarie in salaries:
        db_session.delete(salarie)
        
    db_session.delete(user)
    db_session.commit()