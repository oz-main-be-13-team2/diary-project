from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.db.session import get_db
from app.models.quote import Quote
from app.models.bookmark import Bookmark

router = APIRouter(tags=["bookmarks"])

@router.get("/bookmarks", response_model=List[Dict[str, Any]])
async def get_bookmarks(session: AsyncSession = Depends(get_db)):
    """
    북마크된 명언 목록을 반환합니다.
    """
    # Bookmark 테이블을 조회하고, 'quote' 관계를 통해 명언 정보도 함께 로드합니다.
    result = await session.execute(
        select(Bookmark).options(selectinload(Bookmark.quote))
    )
    bookmarks = result.scalars().all()

    # 조회된 Bookmark 객체에서 Quote 정보를 추출하여 리스트로 반환합니다.
    bookmarked_quotes = [
        {
            "id": bookmark.quote.id,
            "content": bookmark.quote.content,
            "author": bookmark.quote.author,
            "is_bookmarked": True
        }
        for bookmark in bookmarks
    ]

    return bookmarked_quotes