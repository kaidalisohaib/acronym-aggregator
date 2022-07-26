"""empty message

Revision ID: 0abfbfff8217
Revises:
Create Date: 2022-07-19 22:57:21.518787

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0abfbfff8217"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "acronym",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("acronym", sa.String(), nullable=False),
        sa.Column("meaning", sa.String(), nullable=False),
        sa.Column("comment", sa.String(), nullable=True),
        sa.Column("company", sa.String(), nullable=False),
        sa.Column("created_when", sa.DateTime(), nullable=True),
        sa.Column("last_modified", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.String(), nullable=False),
        sa.Column("last_modified_by", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("acronym")
    # ### end Alembic commands ###
