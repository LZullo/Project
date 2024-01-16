import sys
sys.path.append('../')
from fastapi.testclient import TestClient
from fastapi import status
from app.db.models import Salaries as SalariesModel
from app.main import app
client = TestClient(app)

def test_add_salaries_router(db_session, user_on_db):
    body = {
        "cpf_id": user_on_db[0].cpf,
        "salaries": {
            "salarie_date":'2020-10-12', 
            "value_salarie": 1000,
            "discount": 10
        }
    }

    response = client.post('/salaries/add', json=body)

    assert response.status_code == status.HTTP_201_CREATED

    salaries_on_db = db_session.query(SalariesModel).all()

    assert len(salaries_on_db) == 1

    db_session.delete(salaries_on_db[0])
    db_session.commit()

def test_add_salaries_router_invalide_cpf(db_session):
    body = {
        "cpf_id": 00000000000,
        "salaries": {
            "salarie_date":'2020-10-12', 
            "value_salarie": 1000,
            "discount": 10
        }
    }

    response = client.post('/salaries/add', json=body)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    salaries_on_db = db_session.query(SalariesModel).all()
    
    assert len(salaries_on_db) == 0

def test_update_salaries_router(db_session, salaries_on_db):
    body = {
            "salarie_date":'2020-10-12', 
            "value_salarie": 1050,
            "discount": 10,
            "cpf_id" : 42876987965
        }
    
    response = client.put(f'/salaries/update/{salaries_on_db.id}', json=body)

    assert response.status_code == status.HTTP_200_OK

    db_session.refresh(salaries_on_db)

    salaries_on_db.salarie_date == '2020-10-12'
    salaries_on_db.value_salarie == 1050
    salaries_on_db.discount == 10
    salaries_on_db.cpf_id == 42876987965

def test_update_salaries_router_invalid_id():
    body = {
            "salarie_date":'2020-10-12', 
            "value_salarie": 1050,
            "discount": 10,
            "cpf_id" : 42876987965
        }
    
    response = client.put(f'/salaries/update/1', json=body)

    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_salaries_router(db_session, salaries_on_db):
    response = client.delete(f'/salaries/delete/{salaries_on_db.id}')

    assert response.status_code == status.HTTP_200_OK

    salaries_on_db = db_session.query(SalariesModel).all()

    assert len(salaries_on_db) == 0

def test_delete_salaries_router_invalide_id():
    response = client.delete('/salaries/delete/1')

    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_list_salaries_router(salaries_on_db_list):
    response = client.get('/salaries/list')

    assert response.status_code == status.HTTP_200_OK

    data= response.json()

    assert len(data) ==4
    assert data[0] == {
        'id' :  salaries_on_db_list[0].id,
        'salarie_date' :  str(salaries_on_db_list[0].salarie_date),
        'value_salarie' :  salaries_on_db_list[0].value_salarie,
        'discount' :  salaries_on_db_list[0].discount,
        'cpf' : {
            "name": salaries_on_db_list[0].cpf.name,
            "cpf": salaries_on_db_list[0].cpf.cpf,
            "birth_date": str(salaries_on_db_list[0].cpf.birth_date),
        }
    }


def test_list_salaries_info_router():
    response = client.get('/salaries/listinfo')

    assert response.status_code == status.HTTP_200_OK
    
    data= response.json()
    print (data)
    assert len(data) ==0
    
   