from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# FastAPI DB 설정 불러오기
from app.db.base import Base  # Base 선언부
from app.db.session import SQLALCHEMY_DATABASE_URL  # DB URL
from app.models.diary import Diary  # Diary 모델

# Alembic Config 객체
config = context.config
fileConfig(config.config_file_name)

# Alembic이 추적할 메타데이터
target_metadata = Base.metadata

def run_migrations_offline():
    """오프라인 모드: SQL 스크립트 생성"""
    url = SQLALCHEMY_DATABASE_URL
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """온라인 모드: 실제 DB에 적용"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        url=SQLALCHEMY_DATABASE_URL,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
