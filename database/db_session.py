from database.db_connection import engine
from sqlalchemy.orm import sessionmaker, scoped_session

session = scoped_session(sessionmaker(bind=engine))
print("=======================MYSQL SESSION==================================")