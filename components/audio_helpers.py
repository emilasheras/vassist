import pyttsx3
import speech_recognition as sr
from components.logger import logger

def initialize_tts_engine():
    """
    Inicializa el motor de texto a voz con el ID de voz especificado.
    """
    try:
        voice_id = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0"
        engine = pyttsx3.init()
        engine.setProperty("rate", engine.getProperty("rate") * 1.2)
        engine.setProperty("voice", voice_id)
        logger.info(f"Motor de TTS inicializado con la voz: {voice_id}")
        return engine
    except Exception as e:
        logger.error(f"Error al inicializar el motor de TTS: {e}")
        return None

def initialize_recognizer():
    """
    Inicializa y devuelve un objeto Recognizer de SpeechRecognition.
    """
    try:
        recognizer = sr.Recognizer()
        recognizer.pause_threshold = 1.0
        logger.info("Reconocedor de voz inicializado.")
        return recognizer
    except Exception as e:
        logger.error(f"Error al inicializar el reconocedor de voz: {e}")
        return None