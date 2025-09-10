from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
import os
import sys

# 프로젝트 루트 경로 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Alembic config
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# SQLAlchemy Base & 모델 import
from app.db.base import Base  # Base.metadata
from app.models.user import User  # User 모델 import
from app.models.diary import Diary  # Diary 모델 import

target_metadata = Base.metadata

# MySQL 연결 URL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://diary_user:qwer1234@localhost:3306/diary_db"

def run_migrations_offline():
    """오프라인 모드 (SQL문만 생성)"""
    context.configure(
        url=SQLALCHEMY_DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """온라인 모드 (DB 연결 후 실행)"""
    connectable = create_engine(
        SQLALCHEMY_DATABASE_URL,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# 모드에 따라 실행
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
