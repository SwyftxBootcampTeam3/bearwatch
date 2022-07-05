"""create core tables

Revision ID: 66006fcba422
Revises: 
Create Date: 2022-06-29 14:13:12.546279

"""
import datetime
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import expression
from sqlalchemy.sql.schema import ForeignKey


# revision identifiers, used by Alembic.
revision = '66006fcba422'
down_revision = None
branch_labels = None
depends_on = None


def create_user_table() -> None:
    """
    Create User Table
    """
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("phone_number", sa.Text, unique=True, nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime,
                  server_default=sa.func.now(), onupdate=sa.func.now()),
    )


def create_assets_table() -> None:
    op.create_table(
        "assets",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, unique=True),
        sa.Column("code",  sa.Text, unique=True),
        sa.Column("price",  sa.Float, unique=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime,
                  server_default=sa.func.now(), onupdate=sa.func.now()),
    )


def create_alerts_table() -> None:
    op.create_table(
        "alerts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("asset_id", sa.Integer, sa.ForeignKey("assets.id")),
        sa.Column("price", sa.Float, nullable=True),
        sa.Column("alert_type", sa.Boolean, nullable=False),
        sa.Column("last_modified", sa.TIMESTAMP),
        sa.Column("soft_delete", sa.Boolean,
                  unique=False, nullable=False, server_default=expression.false()),
        sa.Column("active", sa.Boolean, nullable=False,
                  unique=False, server_default=expression.true()),
        sa.Column("triggered", sa.Boolean, nullable=False,
                  unique=False, server_default=expression.false()),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime,
                  server_default=sa.func.now(), onupdate=sa.func.now()),
    )


def upgrade() -> None:
    create_user_table()
    create_assets_table()
    create_alerts_table()


def downgrade() -> None:
    op.drop_table("alerts")
    op.drop_table("assets")
    op.drop_table("users")
