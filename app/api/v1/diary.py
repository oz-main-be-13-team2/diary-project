from fastapi import APIRouter, Query
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.diary import DiaryCreate, DiaryUpdate, DiaryResponse
from app.services.diary_service import service
from app.db.session import get_db
from fastapi import Depends

router = APIRouter(prefix="/diaries", tags=["Diary"])

# 일기 작성
@router.post("/", response_model=DiaryResponse)
async def create_diary(diary_data: DiaryCreate, db: AsyncSession = Depends(get_db)):
    return await service.create_diary(db, diary_data)

# 일기 단일 조회
@router.get("/{diary_id}", response_model=DiaryResponse)
async def get_diary(diary_id: int, db: AsyncSession = Depends(get_db)):
    return await service.get_diary(db, diary_id)

# 일기 목록 조회 (검색 + 정렬 + 페이징)
@router.get("/", response_model=List[DiaryResponse])
async def get_diaries(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=50),
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    return await service.get_diaries(db, skip=skip, limit=limit, search=search)

# 일기 수정
@router.put("/{diary_id}", response_model=DiaryResponse)
async def update_diary(diary_id: int, diary_data: DiaryUpdate, db: AsyncSession = Depends(get_db)):
    return await service.update_diary(db, diary_id, diary_data)

# 일기 삭제
@router.delete("/{diary_id}")
async def delete_diary(diary_id: int, db: AsyncSession = Depends(get_db)):
    await service.delete_diary(db, diary_id)
    return {"message": "삭제되었습니다."}
