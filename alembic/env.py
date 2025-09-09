import os
import sys

# ⭐ 변경: 프로젝트의 루트 경로를 직접 시스템 경로에 추가합니다.
# 이렇게 하면 Alembic이 모든 폴더와 파일을 확실하게 찾을 수 있습니다.
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import AsyncEngine

from alembic import context

from app.db.base import Base
from app.db.session import engine

from app.models.user import User
from app.models.quote import Quote
from app.models.question import Question
from app.models.bookmark import Bookmark

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def do_run_migrations(connection: AsyncEngine):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        dialect_opts={"paramstyle": "named"}
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    connectable = engine
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

if __name__ == "__main__":
    asyncio.run(run_migrations_online())