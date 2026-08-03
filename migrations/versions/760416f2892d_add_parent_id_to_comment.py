"""add parent_id to comment

Revision ID: 760416f2892d
Revises: 8058272c6837
Create Date: 2026-08-03 10:59:12.076811

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '760416f2892d'
down_revision: Union[str, Sequence[str], None] = '8058272c6837'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Sử dụng batch_alter_table rất tốt cho SQLite
    with op.batch_alter_table('comments', schema=None) as batch_op:
        # 1. Thêm cột parent_id
        batch_op.add_column(sa.Column('parent_id', sa.String(length=36), nullable=True))
        
        # 2. Xóa dòng drop_index (bỏ dòng này đi để không làm hỏng index của ID)
        # batch_op.drop_index(batch_op.f('ix_comments_id'))
        
        # 3. Tạo Foreign Key
        batch_op.create_foreign_key('fk_comments_parent_id', 'comments', ['parent_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    with op.batch_alter_table('comments', schema=None) as batch_op:
        # 1. SỬA LỖI None: Điền chính xác tên constraint đã tạo ở hàm upgrade
        batch_op.drop_constraint('fk_comments_parent_id', type_='foreignkey')
        
        # 2. Xóa dòng create_index vì ta đã không drop nó ở upgrade
        # batch_op.create_index(batch_op.f('ix_comments_id'), ['id'], unique=False)
        
        # 3. Xóa cột parent_id
        batch_op.drop_column('parent_id')