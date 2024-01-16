import sys
sys.path.append('../')
from app.schemas.base import CustomBaseModel
from datetime import date
from pydantic import field_validator
from app.schemas.user import User

class Salaries(CustomBaseModel):
    salarie_date : date
    value_salarie : float
    discount : float

@field_validator('discount')
def validate_cpf(cls, value):
    if value <0:
        raise ValueError('Invalid discount value')
    return value 

@field_validator('value_salarie')
def validate_cpf(cls, value):
    if value <= 0:
        raise ValueError('Invalid salarie value')
    return value 

class SalariesInput(CustomBaseModel):
    cpf_id : int
    salaries : Salaries

class SalariesOutput(Salaries):
    id : int
    cpf : User