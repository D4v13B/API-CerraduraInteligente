from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Reemplaza los datos de conexión con los tuyos
DATABASE_URL = "postgresql://dbusta0215:Monchillo24$@masterdev507.postgres.database.azure.com:5432/sist_cerradura"

# Crea el motor de conexión
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos de SQLAlchemy
Base = declarative_base()

# Dependencia para obtener la sesión de la base de datos
def get_db():
   db = SessionLocal()
   try:
      yield db
   finally:
      db.close()