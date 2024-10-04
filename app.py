from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from controllers.main_controller import MainController
from components.logger import logger

app = FastAPI()
controller = MainController()

class Puerto(BaseModel):
    puerto: int

class PID(BaseModel):
    pid: int

@app.get("/")
def read_root():
    return {"message": "Asistente Virtual API"}

@app.post("/verificar_puerto")
def verificar_puerto(puerto: Puerto):
    resultado = controller.monitor.verificar_puerto(puerto.puerto)
    logger.info(f"Verificar puerto {puerto.puerto}: {resultado}")
    return {"resultado": resultado}

@app.post("/matar_proceso")
def matar_proceso(pid: PID):
    resultado = controller.monitor.matar_proceso(pid.pid)
    logger.info(f"Matar proceso {pid.pid}: {resultado}")
    return {"resultado": resultado}

@app.get("/revisar_memoria")
def revisar_memoria():
    resultado = controller.monitor.revisar_memoria()
    logger.info(f"Revisar memoria: {resultado}")
    return {"resultado": resultado}

@app.get("/version_os")
def version_os():
    resultado = controller.monitor.obtener_version_os()
    logger.info(f"Obtener versión OS: {resultado}")
    return {"resultado": resultado}

@app.get("/listar_procesos")
def listar_procesos():
    procesos = controller.monitor.listar_procesos()
    logger.info(f"Listar procesos: {len(procesos)} encontrados.")
    return {"procesos": procesos[:5]}  # Devuelve los primeros 5 procesos
