from sqlalchemy.orm import Session
from app.models.diary import Diary
from typing import List, Optional

# 일기 생성
def create_diary(db: Session, diary: Diary):
    db.add(diary)
    db.commit()
    db.refresh(diary)  # 새로 생성된 데이터 반영
    return diary

# 특정 일기 조회
def get_diary(db: Session, diary_id: int) -> Optional[Diary]:
    return db.query(Diary).filter(Diary.diary_id == diary_id, Diary.is_deleted == False).first()

# 일기 목록 조회 (검색, 정렬, 페이징 지원)
def get_diaries(db: Session, skip: int = 0, limit: int = 10, search: Optional[str] = None, sort_by: str = "created_at", desc: bool = True) -> List[Diary]:
    query = db.query(Diary).filter(Diary.is_deleted == False)  # 삭제 안 된 데이터만
    if search:  # 검색 조건
        query = query.filter(Diary.title.contains(search) | Diary.content.contains(search))
    # 정렬 조건
    if desc:
        query = query.order_by(getattr(Diary, sort_by).desc())
    else:
        query = query.order_by(getattr(Diary, sort_by))
    return query.offset(skip).limit(limit).all()

# 일기 수정
def update_diary(db: Session, diary: Diary, updates: dict):
    for key, value in updates.items():
        setattr(diary, key, value)  # 속성 업데이트
    db.commit()
    db.refresh(diary)
    return diary

# 일기 삭제 (소프트 삭제)
def delete_diary(db: Session, diary: Diary):
    diary.is_deleted = True
    db.commit()
    return diary
