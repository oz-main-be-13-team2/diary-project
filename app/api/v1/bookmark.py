from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db  # get_db 함수를 사용하도록 수정
from app.models.quote import Quote
from app.schemas.quote import Quote as QuoteSchema

router = APIRouter(prefix="/bookmarks", tags=["bookmarks"])

@router.get("/", response_model=List[QuoteSchema])
async def get_bookmarks(session: AsyncSession = Depends(get_db)):
    """
    북마크된 명언 목록을 반환합니다.
    """
    result = await session.execute(
        select(Quote).where(Quote.is_bookmarked == True)
    )
    return result.scalars().all()