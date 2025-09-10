from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.question import Question

router = APIRouter()

@router.get("/questions/daily") # GET /questions/daily 엔드포인트: 데이터베이스에서 랜덤 자기성찰 질문을 하나 제공
async def get_daily_question(db: AsyncSession = Depends(get_db)):

    # 1. 데이터베이스에 있는 전체 질문의 개수를 비동기적으로 조회
    count = await db.scalar(select(func.count(Question.id)))
    # 2. 만약 질문이 하나도 없다면 HTTP 404 에러를 반환
    if count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="질문이 데이터베이스에 없습니다."
        )
    # 3. 데이터베이스에서 질문들을 무작위로 정렬한 후, 첫 번째 항목을 가져온다
    random_question = await db.scalar(
        select(Question).order_by(func.random()).limit(1)
    )
    # 4. 조회된 질문 정보를 JSON 형식으로 반환
    return {
        "question_id": random_question.id,
        "question_text": random_question.question_text,
    }