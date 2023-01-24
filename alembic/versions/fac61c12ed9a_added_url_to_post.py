"""added url to post

Revision ID: fac61c12ed9a
Revises: 901632f61e47
Create Date: 2023-01-24 18:24:48.080368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fac61c12ed9a'
down_revision = '901632f61e47'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('url', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'url')
    # ### end Alembic commands ###
