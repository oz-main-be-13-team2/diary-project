from fastapi import APIRouter
from typing import List

router = APIRouter(prefix="/bookmarks", tags=["bookmarks"])

@router.get("/")
async def get_bookmarks():
    # TODO: 북마크 목록을 반환하는 로직을 여기에 구현
    return {"message": "북마크 목록을 반환하는 엔드포인트입니다."}