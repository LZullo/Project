import sys
sys.path.append('../')
from app.use_cases.salaries import SalariesUseCases
from app.db.models import Salaries as SalariesModel
from app.schemas.salaries import Salaries, SalariesOutput
from fastapi.exceptions import HTTPException
import pytest
from datetime import date
from functools import reduce

def test_add_salaries_uc(db_session, user_on_db):

    salaries = Salaries(
        salarie_date = date(2020,12,13),
        value_salarie = 1000.50,
        discount = 0.50,
    )
    uc = SalariesUseCases(db_session)

    uc.add_salaries(salaries=salaries, salaries_cpf= user_on_db[0].cpf)
    salarie_on_db = db_session.query(SalariesModel).first()

    assert salarie_on_db is not None
    assert salarie_on_db.salarie_date == salaries.salarie_date
    assert salarie_on_db.value_salarie == salaries.value_salarie
    assert salarie_on_db.discount == salaries.discount
    assert salarie_on_db.cpf_id == user_on_db[0].cpf

    db_session.delete(salarie_on_db)
    db_session.commit()

def test_add_salaries_uc_invalid_cpf(db_session):
    uc = SalariesUseCases(db_session)

    salaries = Salaries(
        salarie_date = date(2020,12,13),
        value_salarie = 1000.50,
        discount = 0.50
        
    )
    with pytest.raises(HTTPException):
        uc.add_salaries(salaries=salaries, salaries_cpf= 0000000000)

def test_update_salaries(db_session, salaries_on_db):
    salaries = Salaries(
        salarie_date = date(2020,12,13),
        value_salarie = 1000.50,
        discount = 0.50,
    )
    uc = SalariesUseCases(db_session=db_session)
    uc.update_salaries(id=salaries_on_db.id, salaries=salaries)

    salaries_update_on_db = db_session.query(SalariesModel).filter_by(id=salaries_on_db.id).first()

    assert salaries_update_on_db is not None
    assert salaries_update_on_db.salarie_date == salaries.salarie_date
    assert salaries_update_on_db.value_salarie == salaries.value_salarie
    assert salaries_update_on_db.discount == salaries.discount

def test_update_salaries_invalid_id(db_session):
    salaries = Salaries(
        salarie_date = date(2020,12,13),
        value_salarie = 1000.50,
        discount = 0.50,
    )
    uc = SalariesUseCases(db_session=db_session)
    with pytest.raises(HTTPException):
        uc.update_salaries(id=1, salaries=salaries)

def test_delete_salaries(db_session, salaries_on_db):
    uc = SalariesUseCases(db_session=db_session)
    uc.delete_salaries(id=salaries_on_db.id)

    salaries_on_db = db_session.query(SalariesModel).all()
    
    assert len(salaries_on_db) == 0

def test_delete_salaries_non_exist(db_session):
    uc = SalariesUseCases(db_session=db_session)

    with pytest.raises(HTTPException):
        uc.delete_salaries(id=1)

def test_list_salaries(db_session, salaries_on_db_list):
    uc = SalariesUseCases(db_session=db_session)
    salaries = uc.list_salaries()
    for salarie in salaries_on_db_list:
        db_session.refresh(salarie)

    assert len(salaries)==4
    assert type(salaries[0]) == SalariesOutput
    assert salaries[0].cpf.cpf == salaries_on_db_list[0].cpf_id
    assert salaries[0].value_salarie == salaries_on_db_list[0].value_salarie

# def test_list_salaries_with_search(db_session, salaries_on_db_list):
#     uc = SalariesUseCases(db_session=db_session)

#     salaries = uc.list_salaries_search(cpf_id=42876987965)

#     for salarie in salaries_on_db_list:
#         db_session.refresh(salarie)

#     assert len(salaries)==4
#     assert type(salaries[0]) == SalariesOutput
#     assert salaries[0].cpf.cpf == salaries_on_db_list[0].cpf_id
#     assert salaries[0].value_salarie == salaries_on_db_list[0].value_salarie

# def test_salaries_info(db_session, salaries_on_db_list):
#     uc = SalariesUseCases(db_session=db_session)
#     values=uc.list_salaries_info()

#     for salarie in salaries_on_db_list:
#         db_session.refresh(salarie)

#     assert values[0] == 797.5
#     assert values[1] == 28.75
#     assert values[2] == 1080
#     assert values[3] == 100