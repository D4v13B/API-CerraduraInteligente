from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from datetime import datetime
import models
import database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

class Login(BaseModel):
   password: str

class UserSign(BaseModel):
   name: str
   password: str
   
class AccesoResponse(BaseModel):
   acceso_id: int
   usuario_nombre: str
   created_at: datetime

   class Config:
        orm_mode = True
   
# Ejemplo de ruta para obtener todos los usuarios
@app.get("/usuarios/")
def leer_usuarios(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
   usuarios = db.query(models.Usuario).all()
   return usuarios

# Ejemplo de ruta para crear un usuario
@app.post("/usuarios/")
def crear_usuario(request: UserSign, db: Session = Depends(database.get_db)):
   usuario = models.Usuario(nombre=request.name, password=request.password)
   db.add(usuario)
   db.commit()
   db.refresh(usuario)
   return usuario

@app.post("/acceder/")
def autenticar_usuario(request: Login, db: Session = Depends(database.get_db)):
   usuario = db.query(models.Usuario).filter(models.Usuario.password == request.password).first()
    
   #  Verificamos si encontramos un usuario
   if not usuario:
      raise HTTPException(status_code=400, detail="Credenciales inválidas")
   
   # Vamos a insertar en la bitacora de acceso
   acceso = models.BitacoraAcceso(usuario_id=usuario.id)
   db.add(acceso)
   db.commit()
   db.refresh(acceso)
   return acceso

@app.get("/acceder/")
def mostrar_accesos(db: Session = Depends(database.get_db)) -> List[AccesoResponse]:
   # Consulta con el JOIN entre BitacoraAcceso y Usuario
   accesos = db.query(models.BitacoraAcceso, models.Usuario).join(
      models.Usuario, models.BitacoraAcceso.usuario_id == models.Usuario.id
   ).all()

   # Convertimos los resultados en el formato adecuado
   response = [
      AccesoResponse(
         acceso_id=acceso[0].id,    # Accedemos al modelo BitacoraAcceso en la tupla
         usuario_nombre=acceso[1].nombre,
         created_at=acceso[0].created_at,
      )
      for acceso in accesos
   ]
    
   return response