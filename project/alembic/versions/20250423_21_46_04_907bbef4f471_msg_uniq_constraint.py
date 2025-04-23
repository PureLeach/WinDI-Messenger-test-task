"""msg_uniq_constraint

Revision ID: 907bbef4f471
Revises: 568c9476a2fa
Create Date: 2025-04-23 21:46:04.234827+00:00

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "907bbef4f471"
down_revision: str | None = "568c9476a2fa"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Add a constraint to avoid duplicate messages
    op.create_unique_constraint("uq_unique_message", "messages", ["chat_id", "sender_id", "text", "created_at"])


def downgrade() -> None:
    op.drop_constraint("uq_unique_message", "messages", type_="unique")
