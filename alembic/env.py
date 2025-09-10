# alembic/env.py
import os
import sys
import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import async_engine_from_config

# ------------------------
# 1) Alembic 기본 설정
# ------------------------
config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

# ------------------------
# 2) 프로젝트 경로 추가
# ------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# ------------------------
# 3) Base 및 모델 import
# ------------------------
from app.db.base import Base

# 모델 모듈 "자체"를 import 해서 클래스 정의가 실행되게 함
import app.models.user       # noqa: F401
import app.models.diary      # noqa: F401
import app.models.quote      # noqa: F401
import app.models.question   # noqa: F401
import app.models.bookmark   # noqa: F401

target_metadata = Base.metadata

# MySQL 연결 URL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://diary_user:qwer1234@localhost:3306/diary_db"

def run_migrations_offline():
    """오프라인 모드: SQL 스크립트 생성"""
    url = SQLALCHEMY_DATABASE_URL
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    """동기 컨텍스트에서 Alembic 환경 구성 및 실행"""
    # 디버그: Alembic이 인식한 테이블 이름 출력
    context.config.print_stdout(f"Loaded tables: {list(target_metadata.tables.keys())}")

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """온라인 모드 (DB 연결 후 실행)"""
    connectable = create_engine(
        SQLALCHEMY_DATABASE_URL,
        poolclass=pool.NullPool,
    )

def run_migrations_offline():
    """오프라인 모드: 연결 없이 autogenerate/SQL 출력 등"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """온라인 모드: 실제 DB에 연결해서 실행(autogenerate 포함)"""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        future=True,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


# ------------------------
# 4) 분기 "즉시" 실행 (중요!)
# ------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())