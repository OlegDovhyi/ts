"""Init

Revision ID: f325d44a2aa9
Revises: e7b4b216cd72
Create Date: 2023-11-20 23:55:51.182113

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f325d44a2aa9'
down_revision: Union[str, None] = 'e7b4b216cd72'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('photos', sa.Column('created_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('photos', 'created_at')
    # ### end Alembic commands ###
