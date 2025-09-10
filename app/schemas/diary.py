from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# 요청 시 일기 작성용
class DiaryCreate(BaseModel):
    title: str = Field(..., max_length=200, description="일기 제목")
    content: Optional[str] = Field(None, description="일기 내용")
    quote: Optional[str] = Field(None, description="명언")


# 요청 시 일기 수정용
class DiaryUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200, description="일기 제목")
    content: Optional[str] = Field(None, description="일기 내용")
    quote: Optional[str] = Field(None, description="명언")


# 응답용 (조회 시)
class DiaryResponse(BaseModel):
    id: int
    title: str
    content: Optional[str]
    quote: Optional[str]
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        orm_mode = True  # SQLAlchemy 모델을 그대로 변환 가능하게