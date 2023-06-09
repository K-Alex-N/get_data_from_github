"""initial

Revision ID: a02a3826e6b9
Revises: 
Create Date: 2023-05-01 18:39:19.684841

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a02a3826e6b9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('parse_data', 'last_commit',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('parse_data', 'last_release',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('pull_request', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('pull_request', 'start_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.drop_column('pull_request', 'frequency')
    op.alter_column('user', 'username',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user', 'password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('user', 'is_email_confirmed')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_email_confirmed', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('user', 'password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('user', 'username',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.add_column('pull_request', sa.Column('frequency', sa.INTEGER(), autoincrement=False, nullable=True))
    op.alter_column('pull_request', 'start_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('pull_request', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('parse_data', 'last_release',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('parse_data', 'last_commit',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
