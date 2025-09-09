from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base


class Quote(Base): # 명언 테이블
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False, unique=True) # 명언 내용이 겹치지 않게 UNIQUE 제약 추가
    author = Column(String(100))

    bookmarks = relationship("Bookmark", backref="quote")

class Bookmark(Base): # 북마크 테이블
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quote_id = Column(Integer, ForeignKey("quotes.id"), nullable=False)

    quote = relationship("Quote", back_populates="bookmarks")
    user = relationship("User", back_populates="bookmarks")

    # 한 유저가 같은 명언을 여러 번 북마크하는 것을 방지
    __table_args__ = (UniqueConstraint('user_id', 'quote_id', name='_user_quote_uc'),)