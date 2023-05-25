from pydantic import BaseModel

class CategorySchema(BaseModel):
    categoryName: str
    categoryDescription: str
    showUnderMenu: bool

class CategoryResponseSchema(BaseModel):
    categoryId: int
    categoryName: str
    categoryDescription: str
    showUnderMenu: bool
