from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

# 일기 작성 요청 스키마
class DiaryCreate(BaseModel):
    title: str = Field(..., max_length=200, description="일기 제목")
    content: Optional[str] = Field(None, description="본문 내용")
    quotes: Optional[str] = Field(None, description="스크랩한 명언")

# 일기 수정 요청 스키마
class DiaryUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200, description="일기 제목")
    content: Optional[str] = Field(None, description="본문 내용")
    quotes: Optional[str] = Field(None, description="스크랩한 명언")

# 일기 단건 조회 응답 스키마
class DiaryResponse(BaseModel):
    diary_id: int
    user_id: int
    title: str
    content: Optional[str]
    quotes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    is_deleted: bool

    class Config:
        orm_mode = True  # SQLAlchemy 모델과 호환

# 검색/정렬/페이징 응답 스키마
class DiaryListResponse(BaseModel):
    total: int  # 전체 일기 수
    items: List[DiaryResponse]  # 현재 페이지의 일기 목록
