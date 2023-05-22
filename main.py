import uvicorn as uvicorn
from fastapi import FastAPI, Depends
from routes.role import roleRoutes
from routes.category import categoryRoutes

# Create the FastAPI app
app = FastAPI()

app.include_router(roleRoutes)

app.include_router(categoryRoutes)


# Sample API route
@app.get("/")
def serverStatus():
    return {"message": "This is local server and it is UP!"}


# Run the FastAPI application with Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)