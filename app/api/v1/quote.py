from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Literal

from app.db.session import get_db
from app.models.quote import Quote
from app.models.bookmark import Bookmark


router = APIRouter(prefix="/quotes", tags=["quotes"])

class BookmarkAction(BaseModel):
    action: Literal["bookmark", "unbookmark"]

@router.get("/random") # GET /quotes/random 엔드포인트: 데이터베이스에서 랜덤 명언을 하나 제공
async def get_random_quote(db: AsyncSession = Depends(get_db)):

    # 데이터베이스에 있는 전체 명언의 개수를 비동기적으로 조회
    count = await db.scalar(select(func.count(Quote.id)))
    # 명언이 하나도 없으면 HTTP 404 에러를 반환
    if count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="명언이 데이터베이스에 없습니다."
        )
    # 데이터베이스에서 명언을 무작위로 정렬 후, 첫번째 항목 가져온다.
    random_quote = await db.scalar(
        select(Quote).order_by(func.random()).limit(1)
    )
    # 조회된 명언 정보를 JSON 형식으로 반환
    return {
        "quote_id": random_quote.id,
        "content": random_quote.content,
        "author": random_quote.author,
    }

@router.post("/{quote_id}/bookmark") #POST /quotes/{quote_id}/bookmark 엔드포인트: 특정 명언을 북마크하거나 해제
async def bookmark_quote(
        quote_id: int, # URL 경로에서 명언 ID 받기
        request_body: BookmarkAction, # 요청 본문에서 action값 받는다.
        db: AsyncSession = Depends(get_db) # 의존성 주입을 통해 DB 세션 가져오기
):
    # 현재는 사용자 ID가 `1`로 고정되어 있습니다.
    # 실제 앱에서는 사용자 인증을 통해 로그인한 사용자의 ID를 가져와야 합니다.

    user_id = 1
    # 해당 사용자와 명언 ID를 기준으로 기존 북마크가 있는지 조회
    existing_bookmark = await db.scalar(
        select(Bookmark).filter_by(user_id=user_id, quote_id=quote_id)
    )
    # 요청 `action`이 "bookmark"일 경우
    if request_body.action == "bookmark":
        if existing_bookmark: # 이미 북마크가 존재하면 메시지를 반환하고 종료
            return {"message": "이미 북마크된 명언입니다."}

        # 새로운 북마크 객체를 생성하여 데이터베이스에 추가
        new_bookmark = Bookmark(user_id=user_id, quote_id=quote_id)
        db.add(new_bookmark)
        # 변경사항을 커밋하여 데이터베이스에 최종 반영
        await db.commit()
        return {"message": "명언이 북마크되었습니다."}

    # 요청 `action`이 "unbookmark"일 경우
    elif request_body.action == "unbookmark":
        # 북마크가 존재하지 않으면 메시지를 반환하고 종료
        if not existing_bookmark:
            return {"message": "북마크되지 않은 명언입니다."}

        # 기존 북마크 객체를 데이터베이스에서 삭제
        await db.delete(existing_bookmark)
        # 변경사항을 커밋
        await db.commit()
        return {"message": "명언 북마크가 해제되었습니다."}