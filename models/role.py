from sqlalchemy import Table, Column, Integer, String
from config.db import meta, Base, engine


class Roles(Base):
    __tablename__ = "roles"

    roleId = Column(Integer, primary_key=True, autoincrement=True, index=True)
    roleName = Column(String(255), unique=True, index=True)


Base.metadata.create_all(bind=engine)
