"""add user and salaries tables

Revision ID: 0128cee31523
Revises: 
Create Date: 2023-08-13 19:39:20.457464

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0128cee31523'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('cpf', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('birthdate', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cpf')
    )
    op.create_table('salaries',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('salariedate', sa.Date(), nullable=False),
    sa.Column('salarie', sa.Float(), nullable=True),
    sa.Column('discount', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('cpf_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['cpf_id'], ['users.cpf'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('salaries')
    op.drop_table('users')
    # ### end Alembic commands ###
