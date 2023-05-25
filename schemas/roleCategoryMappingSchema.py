from typing import List

from pydantic import BaseModel

class RoleCategoryMappingSchema(BaseModel):
    roleId: int
    categoryId: int

class RoleCategoryMappingResponseSchema(BaseModel):
    roleCategoryMappingId: int
    roleId: int
    categoryId: int

class RoleCategoryMappingCreateSchema(BaseModel):
    roleId: int
    categoryIds: List[int]

class RoleCategoryMappingUpdateSchema(BaseModel):
    categoryIds: List[int]
