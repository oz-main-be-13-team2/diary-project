from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


# 공통 일기 속성
class DiaryBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="일기 제목")  # 제목 (필수, 1~200자)
    content: Optional[str] = Field(None, description="본문 내용")  # 본문 내용
    quotes: Optional[str] = Field(None, description="스크랩한 명언")  # 명언 (옵션)

# 일기 작성 요청 스키마
class DiaryCreate(DiaryBase):
    pass

# 일기 수정 요청 스키마
class DiaryUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)  # 제목 (옵션)
    content: Optional[str] = None  # 본문 (옵션)
    quotes: Optional[str] = None  # 명언 (옵션)

# 단일 일기 응답 스키마
class DiaryResponse(DiaryBase):
    diary_id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    is_deleted: bool  # 삭제 여부

    class Config:
        orm_mode = True  # SQLAlchemy 객체 직렬화 허용

# 일기 목록 응답 스키마
class DiaryListResponse(BaseModel):
    total: int  # 전체 개수
    items: List[DiaryResponse]  # 일기 리스트