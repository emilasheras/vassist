import psutil
import platform
import os
import signal
from components.logger import logger

class SystemMonitor:
    def verificar_puerto(self, puerto):
        """
        Verifica si un puerto está en uso y devuelve información sobre el proceso que lo está utilizando.
        """
        try:
            puerto = int(puerto)
            conexiones = psutil.net_connections()
            for conn in conexiones:
                if conn.laddr.port == puerto:
                    pid = conn.pid
                    if pid:
                        nombre_proceso = psutil.Process(pid).name()
                        logger.info(f"Puerto {puerto} está en uso por {nombre_proceso} (PID {pid}).")
                        return f"El puerto {puerto} está en uso por el proceso {nombre_proceso} con PID {pid}."
                    else:
                        logger.info(f"Puerto {puerto} está en uso.")
                        return f"El puerto {puerto} está en uso."
            logger.info(f"Puerto {puerto} está disponible.")
            return f"El puerto {puerto} está disponible."
        except Exception as e:
            logger.error(f"No se pudo verificar el puerto {puerto}. Error: {e}")
            return f"No se pudo verificar el puerto {puerto}. Error: {str(e)}"
    
    def matar_proceso(self, pid):
        """
        Matar un proceso dado su PID.
        """
        try:
            pid = int(pid)
            os.kill(pid, signal.SIGTERM)
            logger.info(f"Proceso con PID {pid} ha sido terminado.")
            return f"El proceso con PID {pid} ha sido terminado."
        except Exception as e:
            logger.error(f"No se pudo terminar el proceso con PID {pid}. Error: {e}")
            return f"No se pudo terminar el proceso con PID {pid}. Error: {str(e)}"
    
    def revisar_memoria(self):
        """
        Revisa la memoria en uso y devuelve un resumen.
        """
        try:
            mem = psutil.virtual_memory()
            total = mem.total / (1024 ** 3)
            usado = mem.used / (1024 ** 3)
            porcentaje = mem.percent
            logger.info(f"Memoria total: {total:.2f} GB, usada: {usado:.2f} GB ({porcentaje}%).")
            return f"La memoria total es de {total:.2f} GB. La memoria en uso es de {usado:.2f} GB, lo que representa un {porcentaje}% del total."
        except Exception as e:
            logger.error(f"Error al revisar la memoria: {e}")
            return f"No se pudo revisar la memoria en uso. Error: {str(e)}"
    
    def obtener_version_os(self):
        """
        Obtiene la versión del sistema operativo.
        """
        try:
            version_os = platform.platform()
            logger.info(f"Versión del sistema operativo: {version_os}.")
            return f"Está utilizando {version_os}."
        except Exception as e:
            logger.error(f"Error al obtener la versión del sistema operativo: {e}")
            return f"No se pudo obtener la versión del sistema operativo. Error: {str(e)}"
    
    def listar_procesos(self):
        """
        Lista los procesos en ejecución.
        """
        try:
            procesos = []
            for proc in psutil.process_iter(['pid', 'name', 'status']):
                procesos.append(proc.info)
            logger.info(f"Listado de procesos obtenido. Total: {len(procesos)}.")
            return procesos
        except Exception as e:
            logger.error(f"Error al listar procesos: {e}")
            return []
