import sqlalchemy
import sqlalchemy.orm
from src.models.Database import engine
from sqlalchemy.orm import declarative_base, sessionmaker
Base = declarative_base()
Session = sessionmaker(bind=engine, expire_on_commit=False)
Base.metadata.create_all(bind=engine)