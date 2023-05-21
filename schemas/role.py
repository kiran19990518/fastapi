from pydantic import BaseModel

class RoleSchema(BaseModel):
    roleName: str

class RoleResponseSchema(BaseModel):
    roleId: int
    roleName: str
