"""empty message

Revision ID: 454ee941eb57
Revises: c13ced84655c
Create Date: 2022-07-22 22:14:15.812689

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "454ee941eb57"
down_revision = "c13ced84655c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "acronym", "created_at", existing_type=postgresql.TIMESTAMP(), nullable=False
    )
    op.alter_column(
        "acronym", "last_modified_by", existing_type=sa.VARCHAR(), nullable=True
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "acronym", "last_modified_by", existing_type=sa.VARCHAR(), nullable=False
    )
    op.alter_column(
        "acronym", "created_at", existing_type=postgresql.TIMESTAMP(), nullable=True
    )
    # ### end Alembic commands ###
