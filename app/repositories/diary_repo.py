from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from typing import List, Optional
from app.models.diary import Diary

class DiaryRepository:
    # 일기 생성
    async def create_diary(self, db: AsyncSession, diary: Diary) -> Diary:
        db.add(diary)
        await db.commit()
        await db.refresh(diary)
        return diary

    # 일기 ID로 조회
    async def get_diary(self, db: AsyncSession, diary_id: int) -> Optional[Diary]:
        result = await db.execute(select(Diary).where(Diary.id == diary_id, Diary.is_deleted == False))
        return result.scalars().first()

    # 작성자와 일기 ID로 조회 (권한 확인용)
    async def get_diary_by_user(self, db: AsyncSession, diary_id: int, user_id: int) -> Optional[Diary]:
        result = await db.execute(
            select(Diary).where(Diary.id == diary_id, Diary.user_id == user_id, Diary.is_deleted == False)
        )
        return result.scalars().first()

    # 검색 + 정렬 + 페이징
    async def get_diaries(
        self, db: AsyncSession, skip: int = 0, limit: int = 10, search: Optional[str] = None
    ) -> List[Diary]:
        query = select(Diary).where(Diary.is_deleted == False)
        if search:
            query = query.where(Diary.title.contains(search))
        query = query.order_by(desc(Diary.created_at)).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    # 일기 수정
    async def update_diary(self, db: AsyncSession, diary: Diary) -> Diary:
        await db.commit()
        await db.refresh(diary)
        return diary

    # 소프트 삭제
    async def soft_delete_diary(self, db: AsyncSession, diary: Diary):
        diary.is_deleted = True
        await db.commit()
