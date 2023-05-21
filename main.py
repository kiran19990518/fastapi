import uvicorn as uvicorn
from fastapi import FastAPI, Depends
from routes.role import roleRoutes

# Create the FastAPI app
app = FastAPI()

app.include_router(roleRoutes)


# Sample API route
@app.get("/")
def serverStatus():
    return {"message": "This is local server and it is UP!"}


# Run the FastAPI application with Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)