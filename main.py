from fastapi import FastAPI,Depends
from db import base,sessionlocal,engine
from models import Users
from typing import List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.responses import JSONResponse
base.metadata.create_all(bind=engine)

app = FastAPI()
def getdb():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

class user_get_response(BaseModel):
    name : str
    email : str
    class Config:
        orm_mode = True

class user_post_request(user_get_response):
    password :str

@app.get("/userget",response_model = List[user_get_response])
def get_user(db:Session=Depends(getdb)):
    return db.query(Users).all()

@app.post("/userpost",response_model=user_get_response)
def post_user(user:user_post_request,db:Session=Depends(getdb)):
    u = Users(name = user.name,email = user.email,password = user.password)
    db.add(u)
    db.commit()
    return u
@app.delete("/userdelete/{user_id}",response_class=JSONResponse)
def delete_user(user_id:int,db:Session=Depends(getdb)):
        d = db.query(Users).filter(Users.id == user_id).first()
        db.delete(d)
        db.commit()
        return(f"user of id {user_id} is deleted successfull")

@app.put("/userupdate/{user_id}",response_model=user_get_response)
def user_update(user_id:int,user:user_get_response,db:Session=Depends(getdb)):
    u = db.query(Users).filter(Users.id == user_id).first()
    u.name = user.name
    u.email = user.email
    db.add(u)
    db.commit()
    return u



