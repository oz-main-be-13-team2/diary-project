from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class DiaryBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="일기 제목")
    content: Optional[str] = Field(None, description="본문 내용")
    quotes: Optional[str] = Field(None, description="스크랩한 명언")

class DiaryCreate(DiaryBase):
    pass

class DiaryUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = None
    quotes: Optional[str] = None

class DiaryResponse(DiaryBase):
    diary_id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    is_deleted: bool

    class Config:
        orm_mode = True

class DiaryListResponse(BaseModel):
    total: int
    items: List[DiaryResponse]
