from fastapi.testclient import TestClient
from app.main import app
from app.db.models import User as UserModel
from fastapi import status
from datetime import date

client = TestClient(app)

def test_add_user_router(db_session):
    body= {
        'cpf' : 42876987911,
        'name' : 'Ana',
        'birth_date' : '1997-10-15',
    }
    response = client.post('/user/add', json=body)
    
    assert response.status_code == status.HTTP_201_CREATED

    user_on_db = db_session.query(UserModel).all()
    assert len(user_on_db) ==1
    db_session.delete(user_on_db[0])
    db_session.commit()

def test_list_user_router(user_on_db):
    response = client.get('/user/list')

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert len(data) == 4
    assert data[0] == {
        "name": user_on_db[0].name,
        "cpf": user_on_db[0].cpf,
        "birth_date": str(user_on_db[0].birth_date),
        "id": user_on_db[0].id

    }
    
def test_delete_user_router(db_session):
    user_model = UserModel(cpf = 42876987965, name = 'Joao', birth_date ='1997-10-25')
    db_session.add(user_model)
    db_session.commit()

    response = client.delete(f'/user/delete/{user_model.id}')

    assert response.status_code == status.HTTP_200_OK

    user_model = db_session.query(UserModel).first()

    assert user_model is None

def test_delete_user_routerinvalide_is():
    response = client.delete('/user/delete/1')

    assert response.status_code == status.HTTP_404_NOT_FOUND