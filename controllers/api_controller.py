from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from controllers.voice_assistant_controller import VoiceAssistantController
from components.logger import logger

# puerto model used to validate input for verifying port requests
class Puerto(BaseModel):
    puerto: int

# pid model used to validate input for killing a process by pid
class PID(BaseModel):
    pid: int

class APIController:
    def __init__(self, app):
        self.router = APIRouter()
        self.controller = VoiceAssistantController()

        # Registering routes
        self.router.get("/")(self.action_read_root)
        self.router.post("/verificar_puerto")(self.action_verificar_puerto)
        self.router.post("/matar_proceso")(self.action_matar_proceso)
        self.router.get("/revisar_memoria")(self.action_revisar_memoria)
        self.router.get("/version_os")(self.action_version_os)
        self.router.get("/listar_procesos")(self.action_listar_procesos)

        # Include the router in the main app
        app.include_router(self.router)

    def action_read_root(self):
        return {"message": "Asistente Virtual API"}

    def action_verificar_puerto(self, puerto: Puerto):
        resultado = self.controller.monitor.verificar_puerto(puerto.puerto)
        logger.info(f"Verificar puerto {puerto.puerto}: {resultado}")
        return {"resultado": resultado}

    def action_matar_proceso(self, pid: PID):
        resultado = self.controller.monitor.matar_proceso(pid.pid)
        logger.info(f"Matar proceso {pid.pid}: {resultado}")
        return {"resultado": resultado}

    def action_revisar_memoria(self):
        resultado = self.controller.monitor.revisar_memoria()
        logger.info(f"Revisar memoria: {resultado}")
        return {"resultado": resultado}

    def action_version_os(self):
        resultado = self.controller.monitor.obtener_version_os()
        logger.info(f"Obtener versión OS: {resultado}")
        return {"resultado": resultado}

    def action_listar_procesos(self):
        procesos = self.controller.monitor.listar_procesos()
        logger.info(f"Listar procesos: {len(procesos)} encontrados.")
        return {"procesos": procesos[:5]}  # Devuelve los primeros 5 procesos