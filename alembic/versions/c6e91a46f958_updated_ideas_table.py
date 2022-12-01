"""updated ideas table

Revision ID: c6e91a46f958
Revises: 057c87a4c8b9
Create Date: 2022-12-01 17:24:03.023682

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6e91a46f958'
down_revision = '057c87a4c8b9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ideas', sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.create_unique_constraint(None, 'ideas', ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'ideas', type_='unique')
    op.drop_column('ideas', 'time_created')
    # ### end Alembic commands ###
