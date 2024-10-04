import pyttsx3
import speech_recognition as sr
import psutil
import platform
import os
import signal
import datetime

# Opciones de voz / idioma
id1 = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0"
id2 = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"
id3 = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0"

# Función para transformar audio a texto
def transformar_audio_texto():
    r = sr.Recognizer()
    with sr.Microphone() as origen:
        r.pause_threshold = 0.8
        print("Ya puedes hablar")
        audio = r.listen(origen)

        try:
            pedido = r.recognize_google(audio, language="es-ES")
            print(f"Dijiste: {pedido}")
            return pedido
        except sr.UnknownValueError:
            print("No entendí lo que dijiste")
            return "sigo esperando"
        except sr.RequestError:
            print("No se pudo conectar al servicio de reconocimiento de voz")
            return "sigo esperando"
        except:
            print("Ocurrió un error inesperado")
            return "sigo esperando"

# Función para que el asistente hable
def hablar(mensaje):
    engine = pyttsx3.init()
    engine.setProperty("voice", id3)
    engine.say(mensaje)
    engine.runAndWait()

# Función para verificar si un puerto está en uso
def verificar_puerto(puerto):
    try:
        puerto = int(puerto)
        conexiones = psutil.net_connections()
        for conn in conexiones:
            if conn.laddr.port == puerto:
                pid = conn.pid
                if pid:
                    nombre_proceso = psutil.Process(pid).name()
                    return f"El puerto {puerto} está en uso por el proceso {nombre_proceso} con PID {pid}."
                else:
                    return f"El puerto {puerto} está en uso."
        return f"El puerto {puerto} está disponible."
    except Exception as e:
        return f"No se pudo verificar el puerto {puerto}. Error: {str(e)}"

# Función para matar un proceso según su PID
def matar_proceso(pid):
    try:
        pid = int(pid)
        os.kill(pid, signal.SIGTERM)
        return f"El proceso con PID {pid} ha sido terminado."
    except Exception as e:
        return f"No se pudo terminar el proceso con PID {pid}. Error: {str(e)}"

# Función para revisar la memoria en uso
def revisar_memoria():
    mem = psutil.virtual_memory()
    total = mem.total / (1024 ** 3)
    usado = mem.used / (1024 ** 3)
    porcentaje = mem.percent
    return f"La memoria total es de {total:.2f} GB. La memoria en uso es de {usado:.2f} GB, lo que representa un {porcentaje}% del total."

# Función para obtener la versión del sistema operativo
def obtener_version_os():
    version_os = platform.platform()
    return f"Está utilizando {version_os}."

# Función para listar los procesos en ejecución
def listar_procesos():
    procesos = []
    for proc in psutil.process_iter(['pid', 'name', 'status']):
        procesos.append(proc.info)
    return procesos

# Función de saludo inicial
def saludo_inicial():
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = "Buenas noches"
    elif 6 <= hora.hour < 13:
        momento = "Buen día"
    else:
        momento = "Buenas tardes"
    hablar(f"{momento}, soy tu asistente. ¿En qué puedo ayudarte?")

# Función principal del asistente
def centro_pedido():
    saludo_inicial()
    while True:
        pedido = transformar_audio_texto().lower()
        print(f"Comando recibido: {pedido}")

        if "verificar puerto" in pedido or "chequear puerto" in pedido:
            hablar("Por favor, indica el número del puerto que deseas verificar.")
            puerto_pedido = transformar_audio_texto()
            if puerto_pedido.isdigit():
                resultado = verificar_puerto(puerto_pedido)
                hablar(resultado)
            else:
                hablar("No entendí el número del puerto.")
            continue

        elif "matar proceso" in pedido:
            hablar("Por favor, indica el PID del proceso que deseas matar.")
            pid_pedido = transformar_audio_texto()
            if pid_pedido.isdigit():
                resultado = matar_proceso(pid_pedido)
                hablar(resultado)
            else:
                hablar("No entendí el número del PID.")
            continue

        elif "revisar memoria en uso" in pedido or "cuánta memoria está en uso" in pedido:
            info_memoria = revisar_memoria()
            hablar(info_memoria)
            continue

        elif "versión del sistema operativo" in pedido or "qué sistema operativo tengo" in pedido:
            version_os = obtener_version_os()
            hablar(version_os)
            continue

        elif "mostrar procesos en ejecución" in pedido or "listar procesos" in pedido:
            procesos = listar_procesos()
            hablar(f"Actualmente hay {len(procesos)} procesos en ejecución. Los primeros cinco son:")
            for proc in procesos[:5]:
                hablar(f"PID {proc['pid']}, nombre {proc['name']}, estado {proc['status']}.")
            continue

        elif "adiós" in pedido or "hasta luego" in pedido:
            hablar("Hasta luego, que tengas un buen día.")
            break

        else:
            hablar("No he entendido tu solicitud. Por favor, inténtalo de nuevo.")
            continue

# Iniciar el asistente
if __name__ == "__main__":
    centro_pedido()
