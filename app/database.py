from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Define your database URL
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:caramelo555@localhost:5432/mayorista_db'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# 3. Create the SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create the Base class for models
Base = declarative_base()

def get_db(): # analogia: como una puerta a los datos de la pagina
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
