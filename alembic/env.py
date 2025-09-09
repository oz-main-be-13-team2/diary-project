import asyncio
from logging.config import fileConfig

from app.db.base import Base  # 🚨 실제 프로젝트 모델 Base로 바꿔주세요
from app.db.session import engine

from sqlalchemy.ext.asyncio import AsyncEngine

from alembic import context


# Alembic Config 객체 (alembic.ini 사용)
config = context.config

# Logging 설정
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# target_metadata: 자동으로 마이그레이션 생성 시 참조
target_metadata = Base.metadata


def do_run_migrations(connection: AsyncEngine):
    """
    실제 migration 실행 로직 (동기 방식)
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """
    비동기 DB 엔진 생성 후 migration 실행
    """
    connectable = engine

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if __name__ == "__main__":
    asyncio.run(run_migrations_online())
