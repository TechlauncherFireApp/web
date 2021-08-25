"""new UserType Root Admin

Revision ID: a82e602101f6
Revises: 9e60c4a25e61
Create Date: 2021-08-23 14:58:42.415543

"""
from alembic import op
import sqlalchemy as sa
from alembic import context
import sys
from sqlalchemy.dialects import mysql
from sqlalchemy.sql import text

sys.path = ['', '..'] + sys.path[1:]

# revision identifiers, used by Alembic.
revision = 'a82e602101f6'
down_revision = '9e60c4a25e61'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('user', 'user_type',
                    existing_type=mysql.ENUM('VOLUNTEER', 'ADMIN'),
                    nullable=False, type_=mysql.ENUM('ROOT_ADMIN', 'VOLUNTEER', 'ADMIN'), server_default='VOLUNTEER')


def downgrade():
    conn = op.get_bind()
    conn.execute(text("UPDATE user SET user_type = 'VOLUNTEER' WHERE user_type = 'ROOT_ADMIN'"))
    op.alter_column('user', 'user_type',
                    existing_type=mysql.ENUM('ROOT_ADMIN', 'VOLUNTEER', 'ADMIN'),
                    nullable=False, type_=mysql.ENUM('VOLUNTEER', 'ADMIN'), server_default='VOLUNTEER')
