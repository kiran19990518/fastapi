import uvicorn as uvicorn
from fastapi import FastAPI, Depends
from routes.roleRoutes import roleRoutes
from routes.categoryRoutes import categoryRoutes
from routes.roleCategoryMappingRoutes import RoleCategoryMappingRoutes

# Create the FastAPI app
app = FastAPI()

app.include_router(roleRoutes)

app.include_router(categoryRoutes)

app.include_router(RoleCategoryMappingRoutes)


# Sample API route
@app.get("/")
def serverStatus():
    return {"message": "This is local server and it is UP!"}


# Run the FastAPI application with Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)