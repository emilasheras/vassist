from models.system_monitor import SystemMonitor
from models.voice_interface import VoiceInterface
from components.logger import logger
import datetime

class VoiceAssistantController:
    def __init__(self):
        self.monitor = SystemMonitor()
        self.interface = VoiceInterface()
    
    def saludo_inicial(self):
        """
        Envía un saludo inicial basado en la hora del día.
        """
        hora = datetime.datetime.now()
        if hora.hour < 6 or hora.hour > 20:
            momento = "Buenas noches"
        elif 6 <= hora.hour < 13:
            momento = "Buen día"
        else:
            momento = "Buenas tardes"
        mensaje = f"{momento}, soy tu asistente. ¿En qué puedo ayudarte?"
        self.interface.hablar(mensaje)
        logger.info("Saludo inicial enviado.")
    
    def procesar_comando(self, comando):
        """
        Procesa el comando recibido y ejecuta la acción correspondiente.
        """
        logger.info(f"Comando recibido: {comando}")
        
        if "verificar puerto" in comando or "chequear puerto" in comando:
            self.interface.hablar("Por favor, indica el número del puerto que deseas verificar.")
            puerto_pedido = self.interface.transformar_audio_texto()
            if puerto_pedido.isdigit():
                resultado = self.monitor.verificar_puerto(puerto_pedido)
                self.interface.hablar(resultado)
            else:
                self.interface.hablar("No entendí el número del puerto.")
        
        elif "matar proceso" in comando:
            self.interface.hablar("Por favor, indica el PID del proceso que deseas matar.")
            pid_pedido = self.interface.transformar_audio_texto()
            if pid_pedido.isdigit():
                resultado = self.monitor.matar_proceso(pid_pedido)
                self.interface.hablar(resultado)
            else:
                self.interface.hablar("No entendí el número del PID.")
        
        elif "revisar memoria en uso" in comando or "cuánta memoria está en uso" in comando:
            info_memoria = self.monitor.revisar_memoria()
            self.interface.hablar(info_memoria)
        
        elif "versión del sistema operativo" in comando or "qué sistema operativo tengo" in comando:
            version_os = self.monitor.obtener_version_os()
            self.interface.hablar(version_os)
        
        elif "mostrar procesos en ejecución" in comando or "listar procesos" in comando:
            procesos = self.monitor.listar_procesos()
            mensaje = f"Actualmente hay {len(procesos)} procesos en ejecución. Los primeros cinco son:"
            for proc in procesos[:5]:
                mensaje += f" PID {proc['pid']}, nombre {proc['name']}, estado {proc['status']}."
            self.interface.hablar(mensaje)
        
        elif "adiós" in comando or "hasta luego" in comando:
            self.interface.hablar("Hasta luego, que tengas un buen día.")
            logger.info("Asistente finalizado por el usuario.")
            exit()
        
        else:
            self.interface.hablar("No he entendido tu solicitud. Por favor, inténtalo de nuevo.")
            logger.warning("Comando no reconocido.")
    
    def run(self):
        """
        Inicia el asistente virtual.
        """
        self.saludo_inicial()
        while True:
            comando = self.interface.transformar_audio_texto().lower()
            self.procesar_comando(comando)