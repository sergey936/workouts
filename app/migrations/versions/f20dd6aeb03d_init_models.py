"""init_models

Revision ID: f20dd6aeb03d
Revises: 
Create Date: 2024-09-03 19:12:57.715594

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f20dd6aeb03d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('surname', sa.String(), nullable=False),
    sa.Column('patronymic', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('telegram_id', sa.Integer(), nullable=True),
    sa.Column('role', sa.Enum('USER', 'TRAINER', name='role'), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('UTC', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('UTC', now())"), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('workouts',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('trainer_id', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('file_url', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('UTC', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('UTC', now())"), nullable=False),
    sa.ForeignKeyConstraint(['trainer_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comments',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('trainer_id', sa.String(), nullable=False),
    sa.Column('workout_id', sa.String(), nullable=False),
    sa.Column('visible', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('UTC', now())"), nullable=False),
    sa.ForeignKeyConstraint(['trainer_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['workout_id'], ['workouts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rating',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('workout_id', sa.String(), nullable=False),
    sa.Column('likes', sa.Integer(), nullable=False),
    sa.Column('dislikes', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('UTC', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('UTC', now())"), nullable=False),
    sa.ForeignKeyConstraint(['workout_id'], ['workouts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rating')
    op.drop_table('comments')
    op.drop_table('workouts')
    op.drop_table('users')
    # ### end Alembic commands ###