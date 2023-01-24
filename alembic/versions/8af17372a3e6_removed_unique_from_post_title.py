"""removed unique from post title

Revision ID: 8af17372a3e6
Revises: fac61c12ed9a
Create Date: 2023-01-24 18:35:58.541595

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8af17372a3e6'
down_revision = 'fac61c12ed9a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('posts_title_key', 'posts', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('posts_title_key', 'posts', ['title'])
    # ### end Alembic commands ###
