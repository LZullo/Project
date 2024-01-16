from app.schemas.salaries import Salaries, SalariesInput, SalariesOutput
from app.schemas.user import User
import pytest
from datetime import date

def test_salaries_schema():
    salaries = Salaries(
        salarie_date = '2020-10-10',
        value_salarie = 1000.00,
        discount = 100,    
    )

    assert salaries.model_dump() =={
        'salarie_date' : date(2020, 10, 10),
        'value_salarie' : 1000.00,
        'discount' : 100,   
    }

def test_salaries_schema_invalid_discount():
    with pytest.raises(ValueError):
        salaries = Salaries(
        salarie_date = (2020, 10, 10),
        value_salarie = 0,
        discount = 100,    
    )
        
    with pytest.raises(ValueError):
        salaries = Salaries(
        salarie_date = (2020, 10, 10),
        value_salarie = 1000,
        discount = 1050,    
    )

def test_salaries_input_schema():
    salaries = Salaries(
        salarie_date = '2020-10-10',
        value_salarie = 1000.00,
        discount = 100,
    )

    salaries_input = SalariesInput(
        cpf_id = 42876987955,
        salaries = salaries
    )

    assert salaries_input.model_dump() == {
        "cpf_id": 42876987955,
        "salaries": {
            'salarie_date' : date(2020, 10, 10),
            'value_salarie' : 1000.00,
            'discount' : 100
        }
    }

def test_salaries_output_schema():
    user = User(cpf = 42876987965, name = 'Joao', birth_date ='1997-10-25')
    salaries_output = SalariesOutput(
        id = 1,
        salarie_date = '2020-10-10',
        value_salarie = 1000.00,
        discount = 100,
        cpf=user
    )
    assert salaries_output.model_dump() == {
        'id' : 1,
        'salarie_date' : date(2020, 10, 10),
        'value_salarie' : 1000.00,
        'discount' : 100,
        'cpf':{
            'cpf' : 42876987965,
            'name' : 'Joao', 
            'birth_date' : date(1997,10,25)
        }
    }
        
    