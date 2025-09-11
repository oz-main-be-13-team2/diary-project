from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base


class Quote(Base): # 명언 테이블
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False, unique=True) # 명언 내용이 겹치지 않게 UNIQUE 제약 추가
    author = Column(String(100))

    is_bookmarked = Column(Boolean, default=False)
    # bookmarks = relationship("Bookmark", back_populates="quote_rel")
    # questions = relationship("Question", back_populates="quote_rel")

