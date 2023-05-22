from sqlalchemy import Table, Column, Integer, String, Boolean
from config.db import meta, Base, engine


class Categories(Base):
    __tablename__ = "categories"

    categoryId = Column(Integer, primary_key=True, autoincrement=True, index=True)
    categoryName = Column(String(255), unique=True, index=True)
    categoryDescription = Column(String(255))
    showUnderMenu = Column(Boolean, default=False)


Base.metadata.create_all(bind=engine)
