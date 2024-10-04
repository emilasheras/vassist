import pyttsx3
import speech_recognition as sr
from components.logger import logger
from components.audio_helpers import initialize_tts_engine, initialize_recognizer

class VoiceInterface:
    def __init__(self):
        """
        Inicializa el motor de TTS y el reconocedor de voz.
        """
        self.engine = initialize_tts_engine()
        self.recognizer = initialize_recognizer()
    
    def hablar(self, mensaje):
        """
        Convierte el texto a voz y lo reproduce.
        """
        try:
            if self.engine:
                self.engine.say(mensaje)
                self.engine.runAndWait()
                logger.info(f"Mensaje hablado: {mensaje}")
            else:
                logger.error("Motor de TTS no está inicializado.")
        except Exception as e:
            logger.error(f"Error al hablar: {e}")
    
    def transformar_audio_texto(self):
        """
        Escucha el micrófono y convierte el audio a texto.
        """
        if not self.recognizer:
            logger.error("Reconocedor de voz no está inicializado.")
            return "sigo esperando"
        
        with sr.Microphone() as origen:
            self.recognizer.pause_threshold = 0.8
            print("Ya puedes hablar")
            logger.info("Esperando comando de voz.")
            try:
                audio = self.recognizer.listen(origen, timeout=5)
                pedido = self.recognizer.recognize_google(audio, language="es-ES")
                print(f"Dijiste: {pedido}")
                logger.info(f"Comando de voz recibido: {pedido}")
                return pedido
            except sr.UnknownValueError:
                print("No entendí lo que dijiste")
                logger.warning("No se entendió el comando de voz.")
                return "sigo esperando"
            except sr.RequestError:
                print("No se pudo conectar al servicio de reconocimiento de voz")
                logger.error("Error de conexión con el servicio de reconocimiento de voz.")
                return "sigo esperando"
            except sr.WaitTimeoutError:
                print("Tiempo de espera agotado mientras se escuchaba el micrófono.")
                logger.warning("Tiempo de espera agotado para el comando de voz.")
                return "sigo esperando"
            except Exception as e:
                print("Ocurrió un error inesperado")
                logger.error(f"Error inesperado en reconocimiento de voz: {e}")
                return "sigo esperando"
