from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.diary import Diary
from app.repositories.diary_repo import DiaryRepository
from app.schemas.diary import DiaryCreate, DiaryUpdate

repo = DiaryRepository()

class DiaryService:
    # 일기 생성
    async def create_diary(self, db: AsyncSession, user_id: int, diary_data: DiaryCreate) -> Diary:
        diary = Diary(user_id=user_id, **diary_data.dict())
        return await repo.create_diary(db, diary)

    # 단일 조회
    async def get_diary(self, db: AsyncSession, diary_id: int) -> Diary:
        diary = await repo.get_diary(db, diary_id)
        if not diary:
            raise HTTPException(status_code=404, detail="일기를 찾을 수 없습니다.")
        return diary

    # 검색 + 페이징
    async def get_diaries(self, db: AsyncSession, skip: int, limit: int, search: str):
        return await repo.get_diaries(db, skip=skip, limit=limit, search=search)

    # 수정 (작성자 본인 확인)
    async def update_diary(self, db: AsyncSession, diary_id: int, user_id: int, diary_data: DiaryUpdate):
        diary = await repo.get_diary_by_user(db, diary_id, user_id)
        if not diary:
            raise HTTPException(status_code=403, detail="수정 권한이 없습니다.")
        for key, value in diary_data.dict(exclude_unset=True).items():
            setattr(diary, key, value)
        return await repo.update_diary(db, diary)

    # 삭제 (작성자 본인 확인)
    async def delete_diary(self, db: AsyncSession, diary_id: int, user_id: int):
        diary = await repo.get_diary_by_user(db, diary_id, user_id)
        if not diary:
            raise HTTPException(status_code=403, detail="삭제 권한이 없습니다.")
        await repo.soft_delete_diary(db, diary)

service = DiaryService()
