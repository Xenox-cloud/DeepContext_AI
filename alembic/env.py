"""
Alembic environment configuration
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.sql import expression
from app.db.base import Base

# Read configuration from alembic.ini
config = config = config.Config()
config.set_main_option("sqlalchemy.url", os.environ.get("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/nlp_platform"))

# Configure logging
fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")

# Import after logging is configured
from alembic import context
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

# Get target metadata
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        echo=config.get_main_option("sqlalchemy.echo") == "true",
        poolclass=pool.NullPool,
        future=True,
    )

    context.configure(
        connection=connectable.connect(),
        target_metadata=target_metadata,
    )

    with connectable.connect() as connection:
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()