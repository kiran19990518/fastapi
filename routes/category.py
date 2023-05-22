from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import select, insert, update, delete
from config.db import conn
from models.category import Categories
from schemas.category import CategorySchema, CategoryResponseSchema

categoryRoutes = APIRouter(prefix="/api/category")

@categoryRoutes.get("/")
async def getCategories():
    try:
        categories = conn.execute(select(Categories)).fetchall()
        sorted_categories = sorted(categories, key=lambda category: category[0])  # Sort based on category_id
        return [CategoryResponseSchema(categoryId=category[0], categoryName=category[1], categoryDescription=category[2], showUnderMenu=category[3]) for category in sorted_categories]
    except Exception as e:
        print("Exception at getCategories", e)
        raise HTTPException(status_code=500, detail="Failed to fetch categories") from e


@categoryRoutes.get("/{id}")
async def getCategory(id: int):
    try:
        query = select(Categories).where(Categories.categoryId == id)
        result = conn.execute(query)
        category = result.fetchone()

        if category:
            return CategoryResponseSchema(categoryId=category[0], categoryName=category[1], categoryDescription=category[2], showUnderMenu=category[3])  # Return the category as JSON response
        else:
            raise HTTPException(status_code=404, detail="category not found")
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        print("Exception at getCategory", e)
        raise HTTPException(status_code=500, detail=f"Failed to fetch category with id: {id}")


@categoryRoutes.post("/")
async def addCategory(category: CategorySchema):
    query = insert(Categories).values(categoryName=category.categoryName, categoryDescription=category.categoryDescription, showUnderMenu=category.showUnderMenu)

    try:
        result = conn.execute(query)
        conn.commit()
        created_category_id = result.lastrowid

        # Fetch the created category using the ID
        select_query = select(Categories).where(Categories.categoryId == created_category_id)
        created_category = conn.execute(select_query).fetchone()

        if created_category:
            return CategoryResponseSchema(categoryId=created_category[0], categoryName=created_category[1], categoryDescription=created_category[2], showUnderMenu=created_category[3])  # Convert category object to dictionary
        else:
            raise HTTPException(status_code=404, detail="Category not found")
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        conn.rollback()
        print("Exception at addCategory", e)
        raise HTTPException(status_code=500, detail="Failed to create Category due to errorMessage: " + e.args[0]) from e


@categoryRoutes.put("/{id}")
async def updateCategory(id: int, category: CategorySchema):
    query = update(Categories).where(Categories.categoryId == id).values(categoryName=category.categoryName, categoryDescription=category.categoryDescription, showUnderMenu=category.showUnderMenu)

    try:
        result = conn.execute(query)
        conn.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Category not found")
        else:
            # Fetch the created category using the ID
            select_query = select(Categories).where(Categories.categoryName == category.categoryName)
            updated_category = conn.execute(select_query).fetchone()

            if updated_category:
                return CategoryResponseSchema(categoryId=updated_category[0], categoryName=updated_category[1], categoryDescription=updated_category[2], showUnderMenu=updated_category[3])  # Convert category object to dictionary
            else:
                raise HTTPException(status_code=404, detail="Category not found")

    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        conn.rollback()
        print("Exception at updateCategory", e)
        raise HTTPException(status_code=500, detail="Failed to update Category") from e


@categoryRoutes.delete("/{id}")
async def deleteCategory(id: int):
    query = delete(Categories).where(Categories.categoryId == id)

    try:
        result = conn.execute(query)
        conn.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Category not found")
        else:
            return {"message": "Category deleted successfully"}
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        conn.rollback()
        print("Exception at deleteCategory", e)
        raise HTTPException(status_code=500, detail="Failed to delete Category") from e
