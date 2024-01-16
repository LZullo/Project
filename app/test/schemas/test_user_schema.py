import pytest
from app.schemas.user import User
from datetime import date


def test_user_schema():
    user = User(cpf = 42876987977, name = 'Joao', birth_date='1997-10-15')
   
    assert user.model_dump() == {
        'cpf' : 42876987977,
        'name' : 'Joao',
        'birth_date' : date(1997,10,15)
    }

