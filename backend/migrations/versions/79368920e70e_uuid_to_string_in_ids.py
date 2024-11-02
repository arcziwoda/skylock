"""uuid to string in ids

Revision ID: 79368920e70e
Revises: 492f82801e43
Create Date: 2024-11-02 12:03:07.840650

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79368920e70e'
down_revision: Union[str, None] = '492f82801e43'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('files', schema=None) as batch_op:
        batch_op.alter_column('folder_id',
               existing_type=sa.CHAR(length=32),
               type_=sa.String(),
               existing_nullable=False)
        batch_op.alter_column('owner_id',
               existing_type=sa.CHAR(length=32),
               type_=sa.String(),
               existing_nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.CHAR(length=32),
               type_=sa.String(),
               existing_nullable=False)

    with op.batch_alter_table('folders', schema=None) as batch_op:
        batch_op.alter_column('parent_folder_id',
               existing_type=sa.CHAR(length=32),
               type_=sa.String(),
               existing_nullable=True)
        batch_op.alter_column('owner_id',
               existing_type=sa.CHAR(length=32),
               type_=sa.String(),
               existing_nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.CHAR(length=32),
               type_=sa.String(),
               existing_nullable=False)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.CHAR(length=32),
               type_=sa.String(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.String(),
               type_=sa.CHAR(length=32),
               existing_nullable=False)

    with op.batch_alter_table('folders', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.String(),
               type_=sa.CHAR(length=32),
               existing_nullable=False)
        batch_op.alter_column('owner_id',
               existing_type=sa.String(),
               type_=sa.CHAR(length=32),
               existing_nullable=False)
        batch_op.alter_column('parent_folder_id',
               existing_type=sa.String(),
               type_=sa.CHAR(length=32),
               existing_nullable=True)

    with op.batch_alter_table('files', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.String(),
               type_=sa.CHAR(length=32),
               existing_nullable=False)
        batch_op.alter_column('owner_id',
               existing_type=sa.String(),
               type_=sa.CHAR(length=32),
               existing_nullable=False)
        batch_op.alter_column('folder_id',
               existing_type=sa.String(),
               type_=sa.CHAR(length=32),
               existing_nullable=False)

    # ### end Alembic commands ###
