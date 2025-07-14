"""use association table for lobby players"""

from alembic import op
import sqlalchemy as sa

revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('lobbies', 'players')
    op.create_table(
        'lobby_players',
        sa.Column('lobby_id', sa.Integer, sa.ForeignKey('lobbies.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    )


def downgrade() -> None:
    op.drop_table('lobby_players')
    op.add_column('lobbies', sa.Column('players', sa.ARRAY(sa.String), nullable=False, server_default=sa.text("'{}'")))
