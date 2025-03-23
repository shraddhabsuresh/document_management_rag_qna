from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision: str = "1ba40220d1fb"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Apply the initial migration - Create tables."""
    op.create_table(
        "documents",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
    )

    op.create_table(
        "embeddings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("document_id", sa.Integer(), sa.ForeignKey("documents.id")),
        sa.Column("vector", sa.Text()),
    )

def downgrade() -> None:
    """Rollback the initial migration - Drop tables."""
    op.drop_table("embeddings")
    op.drop_table("documents")
