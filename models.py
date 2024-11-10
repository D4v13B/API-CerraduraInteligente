from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base  # Importar Base desde database
from pydantic import BaseModel
from datetime import datetime

class Usuario(Base):
   __tablename__ = "usuarios"

   id = Column(Integer, primary_key=True, index=True)
   nombre = Column(String, index=True)
   password = Column(String)
   
   # Relación inversa
   bitacoras_acceso = relationship("BitacoraAcceso", back_populates="usuario")
   
class BitacoraAcceso(Base):
   __tablename__ = "bitacora_accesos"
   
   id = Column(Integer, primary_key=True, index=True)
   usuario_id = Column(Integer, ForeignKey("usuarios.id"), index=True)
   created_at = Column(DateTime, default=datetime.now())
   
   # Relación con la tabla Usuario (opcional si quieres cargar el usuario relacionado)
   usuario = relationship("Usuario", back_populates="bitacoras_acceso")
   
