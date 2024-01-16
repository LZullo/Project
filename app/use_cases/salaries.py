import sys
sys.path.append('../')
from app.db.models import Salaries as SalariesModel
from app.db.models import User as UserModel
from app.schemas.salaries import Salaries, SalariesOutput
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi.exceptions import HTTPException
from fastapi import status

class SalariesUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_salaries(self,  salaries_cpf: int, salaries: Salaries):

        user = self.db_session.query(UserModel).filter_by(cpf=salaries_cpf).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No salarie found with cpf {salaries_cpf}')
        
        salaries_model=SalariesModel(**salaries.model_dump())
        salaries_model.cpf_id = user.cpf

        self.db_session.add(salaries_model)
        self.db_session.commit()

    def update_salaries(self, id : int, salaries : Salaries):
        salaries_on_db = self.db_session.query(SalariesModel).filter_by(id=id).first()

        if salaries_on_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=('No salarie was found with the given id'))
        
        salaries_on_db.salarie_date = salaries.salarie_date
        salaries_on_db.value_salarie = salaries.value_salarie
        salaries_on_db.discount = salaries.discount

        self.db_session.add(salaries_on_db)
        self.db_session.commit()

    def delete_salaries(self, id : int):
        salaries_on_db = self.db_session.query(SalariesModel).filter_by(id=id).first()

        if not salaries_on_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=('No salarie was found with the given id'))
        self.db_session.delete(salaries_on_db)
        self.db_session.commit()
    
    def list_salaries(self):
        salaries_on_db = self.db_session.query(SalariesModel).all()
        salaries = [ 
            self.serialize_salaries(salarie_on_db)
            for salarie_on_db in salaries_on_db
        ]
        return salaries

    def serialize_salaries(self, salaries_on_db: SalariesModel):
        salaries_dict = salaries_on_db.__dict__
        salaries_dict['cpf'] = salaries_on_db.cpf.__dict__
        return SalariesOutput(**salaries_dict)
    
    
    def list_salaries_info(self):
        values_salary=[]
        value_discounts=[]
        result=[]
        salaries_on_db = self.db_session.query(SalariesModel).all()
        salaries = [ 
            self.serialize_salaries(salarie_on_db)
            for salarie_on_db in salaries_on_db
        ]
        
        for value in salaries:
            values_salary.append(value.value_salarie)
            value_discounts.append(value.discount)
 
        if (len(values_salary) !=0 and len(value_discounts) !=0):
            result.append((sum(values_salary)/len(values_salary)))
            result.append(sum(value_discounts)/len(value_discounts))
            result.append(float(max(values_salary)))
            result.append(float(min(values_salary)))

        return result

