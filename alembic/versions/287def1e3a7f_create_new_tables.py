"""Create new tables

Revision ID: 287def1e3a7f
Revises: 1ba40220d1fb
Create Date: 2025-03-22 01:00:40.699847

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '287def1e3a7f'
down_revision: Union[str, None] = '1ba40220d1fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'documents',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(255)),
        sa.Column('content', sa.Text())
    )
    op.create_table(
        'embeddings',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('document_id', sa.Integer(), sa.ForeignKey('documents.id')),
        sa.Column('vector', sa.Text())
    )


def downgrade() -> None:  # Fix indentation here!
    op.drop_table('embeddings')
    op.drop_table('documents')


