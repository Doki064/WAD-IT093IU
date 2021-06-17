"""Init

Revision ID: 8c7218d09522
Revises: 
Create Date: 2021-06-17 11:25:50.736432

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlalchemy_utils.types.password

# revision identifiers, used by Alembic.
revision = '8c7218d09522'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categories_id'), 'categories', ['id'], unique=False)
    op.create_index(op.f('ix_categories_name'), 'categories', ['name'], unique=True)
    op.create_table('customers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customers_id'), 'customers', ['id'], unique=False)
    op.create_index(op.f('ix_customers_name'), 'customers', ['name'], unique=False)
    op.create_table('shops',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_shops_id'), 'shops', ['id'], unique=False)
    op.create_index(op.f('ix_shops_name'), 'shops', ['name'], unique=True)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('hashed_password', sqlalchemy_utils.types.password.PasswordType(max_length=4294967331), nullable=False),
    sa.Column('salt', sa.String(length=32), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_uuid'), 'users', ['uuid'], unique=True)
    op.create_table('importations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), server_default=sa.text('CURRENT_DATE'), nullable=False),
    sa.Column('shop_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['shop_id'], ['shops.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_importations_date'), 'importations', ['date'], unique=False)
    op.create_index(op.f('ix_importations_id'), 'importations', ['id'], unique=False)
    op.create_table('items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('shop_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['shop_id'], ['shops.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_items_id'), 'items', ['id'], unique=False)
    op.create_index(op.f('ix_items_name'), 'items', ['name'], unique=True)
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), server_default=sa.text('CURRENT_DATE'), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.Column('shop_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.ForeignKeyConstraint(['shop_id'], ['shops.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transactions_date'), 'transactions', ['date'], unique=False)
    op.create_index(op.f('ix_transactions_id'), 'transactions', ['id'], unique=False)
    op.create_table('importation_details',
    sa.Column('importation_id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('item_amount', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['importation_id'], ['importations.id'], ),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.PrimaryKeyConstraint('importation_id', 'item_id')
    )
    op.create_table('transaction_details',
    sa.Column('transaction_id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('item_price', sa.Float(), nullable=False),
    sa.Column('item_amount', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.ForeignKeyConstraint(['transaction_id'], ['transactions.id'], ),
    sa.PrimaryKeyConstraint('transaction_id', 'item_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction_details')
    op.drop_table('importation_details')
    op.drop_index(op.f('ix_transactions_id'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_date'), table_name='transactions')
    op.drop_table('transactions')
    op.drop_index(op.f('ix_items_name'), table_name='items')
    op.drop_index(op.f('ix_items_id'), table_name='items')
    op.drop_table('items')
    op.drop_index(op.f('ix_importations_id'), table_name='importations')
    op.drop_index(op.f('ix_importations_date'), table_name='importations')
    op.drop_table('importations')
    op.drop_index(op.f('ix_users_uuid'), table_name='users')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_shops_name'), table_name='shops')
    op.drop_index(op.f('ix_shops_id'), table_name='shops')
    op.drop_table('shops')
    op.drop_index(op.f('ix_customers_name'), table_name='customers')
    op.drop_index(op.f('ix_customers_id'), table_name='customers')
    op.drop_table('customers')
    op.drop_index(op.f('ix_categories_name'), table_name='categories')
    op.drop_index(op.f('ix_categories_id'), table_name='categories')
    op.drop_table('categories')
    # ### end Alembic commands ###
