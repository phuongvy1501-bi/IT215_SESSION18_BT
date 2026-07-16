import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Default to MySQL, fallback to sqlite if testing
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mysql+pymysql://user:password@localhost:3306/baitap5_db"
)

# SQLite fallback needs connect_args check_same_thread
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
