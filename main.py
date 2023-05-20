import uvicorn as uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create the FastAPI app
app = FastAPI()

# Define SQLAlchemy database URL
database_url = "mysql+pymysql://cbw:cbw@localhost:3306/cbw_local"

# Create the SQLAlchemy engine
engine = create_engine(database_url)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for SQLAlchemy models
Base = declarative_base()

# Sample API route
@app.get("/")
def hello_world():
    return {"message": "Hello, World!"}

# Run the FastAPI application with Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)