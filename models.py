from db import base
from sqlalchemy import Integer,String,Column
class Users(base):
    __tablename__ = "usertable"
    id = Column(Integer,primary_key = True,index = True)
    name = Column(String(50))
    email = Column(String(70),unique=True)
    password = Column(String(50))