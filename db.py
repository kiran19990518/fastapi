from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
db_url = "mysql://root:@127.0.0.1:3306/fastapi_crud"

engine = create_engine(db_url)
base = declarative_base()
sessionlocal = sessionmaker(autocommit = False,bind=engine)

