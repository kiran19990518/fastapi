from typing import List, Dict, Union

from fastapi import APIRouter, HTTPException
from sqlalchemy import select, insert, update, delete
from config.db import conn
from models.roleCategoryMappingModel import RoleCategoryMapping
from schemas.roleCategoryMappingSchema import RoleCategoryMappingSchema, RoleCategoryMappingResponseSchema, \
    RoleCategoryMappingCreateSchema, RoleCategoryMappingUpdateSchema

RoleCategoryMappingRoutes = APIRouter(prefix="/api/roleCategoryMapping")

@RoleCategoryMappingRoutes.get("/", response_model=List[Dict[str, Union[int, List[int]]]])
async def getAllRoleCategoryMapping():
    try:
        # Retrieve the role vs categories mapping
        query_select = select(RoleCategoryMapping.roleId, RoleCategoryMapping.categoryId).order_by(
            RoleCategoryMapping.roleId)
        result = conn.execute(query_select).fetchall()

        # Group the categories by roleId
        role_categories = {}
        for row in result:
            roleId = row[0]
            categoryId = row[1]

            if roleId not in role_categories:
                role_categories[roleId] = []

            role_categories[roleId].append(categoryId)

        # Sort the role_categories dictionary by roleId
        role_categories = dict(sorted(role_categories.items(), key=lambda x: x[0]))

        # Convert the dictionary to a list of dictionaries
        response = [{"roleId": roleId, "categories": categoryIds} for roleId, categoryIds in role_categories.items()]

        return response

    except Exception as e:
        print("Exception at getAllRoleCategoryMapping: ", e)
        raise HTTPException(status_code=500, detail="Failed to fetch getAllRoleCategoryMapping") from e


@RoleCategoryMappingRoutes.get("/{roleId}")
async def getRoleCategoryMappingWithRoleId(roleId: int):
    try:
        # Retrieve the updated role vs categories response
        query_select = select(RoleCategoryMapping).where(RoleCategoryMapping.roleId == roleId)
        result = conn.execute(query_select).fetchall()

        if result:
            role_categories = {
                "roleId": roleId,
                "categories": [row[2] for row in result]
            }

            return role_categories
        else:
            raise HTTPException(status_code=404, detail=f"roleCategoryMapping not found with roleId: {roleId}")
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        print("Exception at getRoleCategoryMappingWithRoleId", e)
        raise HTTPException(status_code=500, detail=f"Failed to fetch getRoleCategoryMappingWithRoleId with id: {id}")


@RoleCategoryMappingRoutes.post("/")
async def addRoleCategoryMappingWithRoleId(mapping: RoleCategoryMappingCreateSchema):
    categoryIds = mapping.categoryIds
    print(categoryIds)
    try:
        # Create a new mapping for each category
        for categoryId in categoryIds:
            query_insert = insert(RoleCategoryMapping).values(roleId=mapping.roleId, categoryId=int(categoryId))
            result = conn.execute(query_insert)

        conn.commit()

        return {"message": "Category mappings created successfully."}
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        conn.rollback()
        print("Exception at addRoleCategoryMapping", e)
        raise HTTPException(status_code=500, detail="Failed to create addRoleCategoryMapping due to errorMessage: " + e.args[0]) from e


@RoleCategoryMappingRoutes.put("/{roleId}")
async def updateRoleCategoryMappingWithRoleId(roleId: int, update: RoleCategoryMappingUpdateSchema):
    categoryIds = update.categoryIds

    try:
        # Delete existing mappings for the role
        query_delete = delete(RoleCategoryMapping).where(RoleCategoryMapping.roleId == roleId)
        conn.execute(query_delete)

        # Create new mappings for the updated categories
        for categoryId in categoryIds:
            query_insert = insert(RoleCategoryMapping).values(roleId=roleId, categoryId=int(categoryId))
            result = conn.execute(query_insert)
        conn.commit()

        # Retrieve the updated role vs categories response
        query_select = select(RoleCategoryMapping).where(RoleCategoryMapping.roleId == roleId)
        result = conn.execute(query_select)

        if result:
            updated_role_categories = {
                "roleId": roleId,
                "categories": [row[2] for row in result]
            }

            return updated_role_categories
        else:
            raise HTTPException(status_code=404, detail=f"roleCategoryMapping not found with roleId: {roleId}")

    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        conn.rollback()
        print("Exception at updateRoleCategoryMapping", e)
        raise HTTPException(status_code=500, detail="Failed to create updateRoleCategoryMapping due to errorMessage: " + e.args[0]) from e


@RoleCategoryMappingRoutes.delete("/{roleId}")
async def deleteRoleCategoryMappingWithRoleId(roleId: int):

    try:
        # Delete mappings for the specified roleId
        query_delete = delete(RoleCategoryMapping).where(RoleCategoryMapping.roleId == roleId)
        result = conn.execute(query_delete)
        conn.commit()

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Role not found with roleId={roleId}")

        return {"message": f"AllRoleCategoryMapping for roleId={roleId} deleted successfully"}
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        conn.rollback()
        print("Exception at deleteRoleCategoryMappingWithRoleId", e)
        raise HTTPException(status_code=500, detail="Failed to delete RoleCategoryMappingWithRoleId") from e
