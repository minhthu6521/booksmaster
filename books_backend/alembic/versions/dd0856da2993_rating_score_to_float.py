"""rating score to float

Revision ID: dd0856da2993
Revises: 3ed9794ef631
Create Date: 2021-10-27 00:21:09.106289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd0856da2993'
down_revision = '3ed9794ef631'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rating', 'score', existing_type=sa.Integer(), type_=sa.Float())
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rating', 'score', existing_type=sa.Float(), type_=sa.Integer())
    # ### end Alembic commands ###
