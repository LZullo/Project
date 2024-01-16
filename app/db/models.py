
from sqlalchemy import Column, Integer, String, DateTime, Float, BigInteger, ForeignKey, func, Date
from app.db.base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    id = Column ('id', Integer, primary_key=True, autoincrement=True)
    cpf = Column ('cpf', BigInteger, nullable=False, unique=True)
    name=Column('name', String, nullable=False)
    birth_date= Column ('birthdate', Date, nullable=True )
    salaries = relationship('Salaries', back_populates= 'cpf')
    
class Salaries(Base):
    __tablename__ = 'salaries'
    id = Column ('id', Integer, primary_key=True, autoincrement=True)
    salarie_date = Column ('salariedate', Date, nullable=False )
    value_salarie = Column ('salarie', Float)
    discount = Column ('discount', Float)
    created_at = Column ('created_at', DateTime, server_default = func.now()) 
    cpf_id = Column('cpf_id', ForeignKey('users.cpf'), nullable=False, unique = False)
    cpf = relationship('User', back_populates= 'salaries')