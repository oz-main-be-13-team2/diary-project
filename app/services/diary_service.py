from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.schemas.diary import DiaryCreate, DiaryUpdate
from app.models.diary import Diary
from app.repositories import diary_repo

# 일기 작성 서비스
def create_diary(db: Session, user_id:int, diary_data: DiaryCreate):
    diary = Diary(user_id=user_id, **diary_data.model_dump())
    return diary_repo.create_diary(db, diary)

# 일기 단일 조회 서비스
def get_diary_service(db: Session, diary_id: int):
    diary = diary_repo.get_diary(db, diary_id)
    if not diary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="일기를 찾을 수 없습니다.")
    return diary

# 일기 수정 서비스
def update_diary_service(db: Session, diary_id: int, user_id: int, diary_data: DiaryUpdate):
    diary = diary_repo.get_diary(db, diary_id)
    if not diary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="일기를 찾을 수 없습니다.")

    if diary.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="수정 권한이 없습니다.")
    return diary_repo.update_diary(db, diary, diary_data.model_dump(exclude_unset=True))

# 일기 삭제 서비스
def delete_diary_service(db: Session, diary_id: int, user_id: int):
    diary = diary_repo.get_diary(db, diary_id)
    if not diary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="일기를 찾을 수 없습니다.")
    if diary.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="삭제 권한이 없습니다.")
    return diary_repo.delete_diary(db, diary)

# 일기 목록 조회 서비스
def list_diary_service(db: Session, skip: int, limit: int, search: str, sort_by: str, desc: bool):
    diaries = diary_repo.get_diaries(db, skip, limit, search, sort_by, desc)
    return {"total": len(diaries), "items": diaries}