from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import select, insert, update, delete
from config.db import conn
from models.roleModel import Roles
from schemas.roleSchema import RoleSchema, RoleResponseSchema

roleRoutes = APIRouter(prefix="/api/role")



@roleRoutes.get("/")
async def getRoles():
    try:
        roles = conn.execute(select(Roles)).fetchall() #This is a list of tuple type. ex: [(1, "Admin")]
        sorted_roles = sorted(roles, key=lambda role: role[0])  # Sort based on role_id
        return [RoleResponseSchema(roleId=role[0], roleName=role[1]) for role in sorted_roles]
    except Exception as e:
        print("Exception at getRoles", e)
        raise HTTPException(status_code=500, detail="Failed to fetch roles") from e


@roleRoutes.get("/{id}")
async def getRole(id: int):
    try:
        query = select(Roles).where(Roles.roleId == id)
        result = conn.execute(query)
        role = result.fetchone()

        if role:
            return RoleResponseSchema(roleId=role[0], roleName=role[1])  # Return the role as JSON response
        else:
            raise HTTPException(status_code=404, detail="Role not found")
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        print("Exception at getRole", e)
        raise HTTPException(status_code=500, detail=f"Failed to fetch role with id: {id}")


@roleRoutes.post("/")
async def addRoles(role: RoleSchema):
    query = insert(Roles).values(roleName=role.roleName)

    try:
        result = conn.execute(query)
        conn.commit()
        created_role_id = result.lastrowid

        # Fetch the created role using the ID
        select_query = select(Roles).where(Roles.roleId == created_role_id)
        created_role = conn.execute(select_query).fetchone()

        if created_role:
            return RoleResponseSchema(roleId=created_role[0], roleName=created_role[1])  # Convert role object to dictionary
        else:
            raise HTTPException(status_code=404, detail="Role not found")
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        conn.rollback()
        print("Exception at addRoles", e)
        raise HTTPException(status_code=500, detail="Failed to create role due to errorMessage: " + e.args[0]) from e


@roleRoutes.put("/{id}")
async def updateRole(id: int, role: RoleSchema):
    query = update(Roles).where(Roles.roleId == id).values(roleName=role.roleName)

    try:
        result = conn.execute(query)
        conn.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Role not found")
        else:
            # Fetch the created category using the ID
            select_query = select(Roles).where(Roles.roleName == role.roleName)
            updated_role = conn.execute(select_query).fetchone()

            if updated_role:
                return RoleResponseSchema(categoryId=updated_role[0], categoryName=updated_role[1], categoryDescription=updated_role[2], showUnderMenu=updated_role[3])  # Convert role object to dictionary
            else:
                raise HTTPException(status_code=404, detail="role not found")
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        conn.rollback()
        print("Exception at updateRole", e)
        raise HTTPException(status_code=500, detail="Failed to update role") from e


@roleRoutes.delete("/{id}")
async def deleteRole(id: int):
    query = delete(Roles).where(Roles.roleId == id)

    try:
        result = conn.execute(query)
        conn.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Role not found")
        else:
            return {"message": "Role deleted successfully"}
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        conn.rollback()
        print("Exception at deleteRole", e)
        raise HTTPException(status_code=500, detail="Failed to delete role") from e
