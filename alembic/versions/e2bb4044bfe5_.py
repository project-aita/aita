"""empty message

Revision ID: e2bb4044bfe5
Revises: d0d3ba6b4046
Create Date: 2024-07-24 14:21:08.769374

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e2bb4044bfe5"
down_revision: Union[str, None] = "d0d3ba6b4046"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("datasource", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("attributes", sqlmodel.sql.sqltypes.AutoString(), nullable=False)
        )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("datasource", schema=None) as batch_op:
        batch_op.drop_column("attributes")

    # ### end Alembic commands ###