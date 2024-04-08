"""Change of password column to password_hash

Revision ID: a939740d0e19
Revises: b900620061a7
Create Date: 2024-04-08 14:42:19.628561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a939740d0e19'
down_revision = 'b900620061a7'
branch_labels = None
depends_on = None


def upgrade():
       bind = op.get_bind()
       inspector = sa.inspect(bind)
       if "_alembic_tmp_user" in inspector.get_table_names():
              op.drop_table("_alembic_tmp_user")
              
    # ### commands auto generated by Alembic - please adjust! ###
       with op.batch_alter_table('user', schema=None) as batch_op:
              batch_op.add_column(sa.Column('password_hash', sa.String(length=64)))
              batch_op.alter_column('email',
                     existing_type=sa.VARCHAR(length=150),
                     type_=sa.String(length=64),
                     nullable=True)
              batch_op.alter_column('username',
                     existing_type=sa.VARCHAR(length=150),
                     type_=sa.String(length=128),
                     nullable=False)
              batch_op.drop_column('password')
   # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.VARCHAR(length=150), nullable=True))
        batch_op.alter_column('username',
               existing_type=sa.String(length=128),
               type_=sa.VARCHAR(length=150),
               nullable=True)
        batch_op.alter_column('email',
               existing_type=sa.String(length=64),
               type_=sa.VARCHAR(length=150),
               nullable=True)
        batch_op.drop_column('password_hash')

    # ### end Alembic commands ###
