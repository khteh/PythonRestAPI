import sqlalchemy
import sqlalchemy.orm
from src.models.Database import engine
from sqlalchemy.orm import declarative_base
#from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
Base.metadata.create_all(bind=engine)