from pydantic import BaseModel

class Quote(BaseModel):
    id: int
    content: str
    author: str
    is_bookmarked: bool

    class Config:
        from_attributes = True