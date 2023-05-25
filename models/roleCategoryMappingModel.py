from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from config.db import meta, Base, engine


class RoleCategoryMapping(Base):
    __tablename__ = 'role_category_mapping'

    roleCategoryMappingId = Column(Integer, primary_key=True, autoincrement=True, index=True)
    roleId = Column(Integer, ForeignKey('roles.roleId'), index=True)
    categoryId = Column(Integer, ForeignKey('categories.categoryId'), index=True)

    role = relationship("Roles", backref="role_category_mappings")
    category = relationship("Categories", backref="role_category_mappings")


Base.metadata.create_all(bind=engine)
