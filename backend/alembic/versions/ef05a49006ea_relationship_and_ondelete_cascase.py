"""relationship and ondelete cascase

Revision ID: ef05a49006ea
Revises: 672cb9fdb0d9
Create Date: 2024-06-03 07:41:52.876073

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ef05a49006ea"
down_revision: Union[str, None] = "672cb9fdb0d9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("tokens_user_id_fkey", "tokens", type_="foreignkey")
    op.create_foreign_key(
        None, "tokens", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )
    op.drop_constraint("users_role_id_fkey", "users", type_="foreignkey")
    op.create_foreign_key(
        None, "users", "roles", ["role_id"], ["id"], ondelete="CASCADE"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "users", type_="foreignkey")
    op.create_foreign_key(
        "users_role_id_fkey", "users", "roles", ["role_id"], ["id"], ondelete="SET NULL"
    )
    op.drop_constraint(None, "tokens", type_="foreignkey")
    op.create_foreign_key(
        "tokens_user_id_fkey",
        "tokens",
        "users",
        ["user_id"],
        ["id"],
        ondelete="SET NULL",
    )
    # ### end Alembic commands ###