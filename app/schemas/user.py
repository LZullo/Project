from app.schemas.base import CustomBaseModel
from pydantic import field_validator
from datetime import date

class User(CustomBaseModel):
    cpf : int
    name : str
    birth_date : date 

    @field_validator('cpf')
    def validate_cpf(cls, value):
        if len(str(value)) != 11:
            raise ValueError('Invalid cpf')
        return value 

class UserOutput(User):
    id : int
    