from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base

class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quote_id = Column(Integer, ForeignKey("quotes.id"), nullable=False)

    quote = relationship("Quote", back_populates="bookmarks")
    user = relationship("User", back_populates="bookmarks")

    __table_args__ = (UniqueConstraint('user_id', 'quote_id', name='_user_quote_uc'),)