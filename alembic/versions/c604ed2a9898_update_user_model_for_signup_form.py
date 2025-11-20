"""update_user_model_for_signup_form

Revision ID: c604ed2a9898
Revises: 665048457008
Create Date: 2025-11-19 17:31:21.149914

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c604ed2a9898'
down_revision: Union[str, None] = '665048457008'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # SQLite doesn't support ALTER COLUMN, so we need to use batch operations
    with op.batch_alter_table('users', schema=None) as batch_op:
        # Add new columns
        batch_op.add_column(sa.Column('full_name', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('username', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('user_type', sa.String(), nullable=False))
        
        # Create index on username
        batch_op.create_index(batch_op.f('ix_users_username'), ['username'], unique=True)
        
        # Drop old columns and index (if they exist)
        try:
            batch_op.drop_index('ix_users_email')
        except:
            pass  # Index might not exist
        
        batch_op.drop_column('email')
        batch_op.drop_column('name')
        batch_op.drop_column('role')


def downgrade() -> None:
    # Add back old columns
    op.add_column('users', sa.Column('role', sa.String(), nullable=True))
    op.add_column('users', sa.Column('name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('email', sa.String(), nullable=True))
    
    # Create index on email
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    
    # Drop new columns
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_column('users', 'user_type')
    op.drop_column('users', 'username')
    op.drop_column('users', 'full_name')
    
    # Make old columns non-nullable
    op.alter_column('users', 'email', nullable=False)
    op.alter_column('users', 'name', nullable=False)
