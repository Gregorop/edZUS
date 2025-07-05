import asyncio

from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context
from app.core.database import SQLALCHEMY_DATABASE_URL
from app.models.base import Base

config = context.config
config.set_main_option('sqlalchemy.url', SQLALCHEMY_DATABASE_URL)
target_metadata = Base.metadata

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    connectable = create_async_engine(SQLALCHEMY_DATABASE_URL)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def run_migrations_online():
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    connectable = context.config.attributes.get("connection", None)
    if connectable is None:
        from sqlalchemy import engine_from_config, pool
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()
else:
    run_migrations_online()
