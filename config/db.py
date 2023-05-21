from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

meta = MetaData()

# Define SQLAlchemy database URL
database_url = "mysql+pymysql://cbw:cbw@localhost:3306/cbw_local"

# Create the SQLAlchemy engine
engine = create_engine(database_url)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for SQLAlchemy models
Base = declarative_base()

conn = engine.connect()