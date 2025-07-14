"""create initial tables"""

from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('username', sa.String, nullable=False, unique=True),
        sa.Column('hashed_password', sa.String, nullable=False),
        sa.Column('chips', sa.Integer, nullable=False, server_default='1000'),
        sa.Column('in_lobby', sa.Boolean, nullable=False, server_default=sa.text('false')),
    )
    op.create_table(
        'lobbies',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('max_players', sa.Integer, nullable=False),
        sa.Column('players', sa.ARRAY(sa.String), nullable=False, server_default=sa.text("'{}'")),
        sa.Column('status', sa.String, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('lobbies')
    op.drop_table('users')
