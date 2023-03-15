"""added column price in advertisement

Revision ID: 12b44edb6ae8
Revises: 3afb266ec507
Create Date: 2023-03-15 19:01:31.035699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12b44edb6ae8'
down_revision = '3afb266ec507'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('advertisement_table', sa.Column('price', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('advertisement_table', 'price')
    # ### end Alembic commands ###