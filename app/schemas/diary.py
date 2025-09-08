from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


# 요청용 스키마
class DiaryCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    content: Optional[str] = None


class DiaryUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    content: Optional[str] = None


# 응답용 스키마
class DiaryResponse(BaseModel):
    id: int
    title: str
    content: Optional[str]
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        from_attributes = True  # SQLAlchemy 모델 → Pydantic 변환 허용