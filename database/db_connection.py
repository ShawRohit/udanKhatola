from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from config_env.conf_env import config

engine = create_engine(
    'mysql+pymysql://' + config.db_username + ':' + config.db_password + '@' + config.db_host +
    '/' + config.db_name + '?charset=utf8mb4', echo=False, pool_size=20, max_overflow=10, pool_pre_ping=True,
    pool_recycle=360)

Base = declarative_base()
print("=======================MYSQL CONNECT==================================")
