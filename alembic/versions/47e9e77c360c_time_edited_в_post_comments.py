"""time edited в post comments

Revision ID: 47e9e77c360c
Revises: 9364bbc5f4b2
Create Date: 2023-02-07 19:52:26.735989

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47e9e77c360c'
down_revision = '9364bbc5f4b2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts_comments', sa.Column('time_edited', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts_comments', 'time_edited')
    # ### end Alembic commands ###
