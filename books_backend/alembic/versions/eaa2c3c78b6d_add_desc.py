"""add desc

Revision ID: eaa2c3c78b6d
Revises: a212c3af1870
Create Date: 2021-10-27 23:49:18.675117

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eaa2c3c78b6d'
down_revision = 'a212c3af1870'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('description', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('books', 'description')
    # ### end Alembic commands ###
