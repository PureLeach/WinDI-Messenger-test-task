# mypy: ignore-errors
# ruff: noqa
import importlib
import pkgutil
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from project import tables
from project.config.base import settings
from project.config.db import metadata


def load_models_from_package(package):
    """Recursively loads all modules in the specified folder"""
    package_path = package.__path__
    for _, module_name, is_pkg in pkgutil.iter_modules(package_path):
        full_module_name = f"{package.__name__}.{module_name}"
        if is_pkg:
            subpackage = importlib.import_module(full_module_name)
            load_models_from_package(subpackage)
        else:
            importlib.import_module(full_module_name)


# Loading all tables from the tables folder
load_models_from_package(tables)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)  # type: ignore[arg-type]

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

# FYI: configparser.BasicInterpolation.before_set tries to interpolate %(var)s patterns.
# We have to quote password string to pass special characters. This characters will be encoded by % prefix.
# Also we have to escape percent-sign for BasicInterpolation.
sync_url = settings.DB.DATABASE_DSN.replace("asyncpg", "psycopg2")
config.set_main_option("sqlalchemy.url", sync_url)
target_metadata = metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table" and object.info.get("skip_autogenerate", False):
        return False
    else:
        return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        include_object=include_object,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            include_object=include_object,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
