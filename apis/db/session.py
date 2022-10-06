import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from configs.config import config

db_info = config.databases["inner"]
dns = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(
    db_info["username"],
    db_info["password"],
    db_info["host"],
    db_info["port"],
    db_info["database"],
)
engine = create_engine(
    dns,
    echo=True,
    connect_args={
        "init_command": "SET SESSION time_zone='{}'".format(db_info["timezone"])
    },
)
DBSession = sessionmaker(bind=engine)


def get_db_session() -> Session:
    try:
        return DBSession()
    except Exception as e:
        logging.error("failed to connect db", e)
