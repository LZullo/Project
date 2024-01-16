import sys
sys.path.append('../')
from fastapi import APIRouter, Depends, Response, status
from app.schemas.salaries import Salaries, SalariesInput, SalariesOutput
from sqlalchemy.orm import Session
from app.router.deps import get_db_session
from app.use_cases.salaries import SalariesUseCases
from typing import List

router = APIRouter(prefix='/salaries', tags=['Salaries'])

@router.post('/add', status_code=status.HTTP_201_CREATED, description="Add new salarie")
def add_salaries(
    salaries_input : SalariesInput,
    db_session: Session = Depends(get_db_session)
):

    uc = SalariesUseCases(db_session=db_session)
    uc.add_salaries(
        salaries = salaries_input.salaries,
        salaries_cpf = salaries_input.cpf_id
    )

    return Response(status_code=status.HTTP_201_CREATED)

@router.put('/update/{id}', status_code=status.HTTP_201_CREATED, description="Update salarie")
def update_salaries(
    id : int,
    salaries: Salaries,
    db_session: Session = Depends(get_db_session)
):
    uc = SalariesUseCases(db_session=db_session)
    uc.update_salaries(id=id, salaries=salaries)
    
    return Response(status_code=status.HTTP_200_OK)

@router.delete('/delete/{id}', description="Delete salarie")
def delete_salaries(
    id : int,
    db_session: Session = Depends(get_db_session)
):
    uc = SalariesUseCases(db_session=db_session)
    uc.delete_salaries(id=id)
    
    return Response(status_code=status.HTTP_200_OK)

@router.get('/list', response_model= List[SalariesOutput], description='List user')
def list_salaries(
    db_session: Session = Depends(get_db_session)
):
    uc = SalariesUseCases(db_session=db_session)
    response = uc.list_salaries()
    return response

@router.get('/listinfo')
def list_salaries_info(
    db_session: Session = Depends(get_db_session)
):
    uc = SalariesUseCases(db_session=db_session)
    response = uc.list_salaries_info()
    return response