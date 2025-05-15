# app.py
import sys
import os
from dotenv import load_dotenv
import os
from ui import interfaz
# Agrega el path al paquete raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'translate_signal_hands')))
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path= env_path)  # Carga las variables de entorno desde el archivo .env
print("AAI_KEY:", os.environ.get("AAI_KEY"))
print("ROUTER_KEY:", os.environ.get("ROUTER_KEY"))
try:
    interfaz.main()    
except KeyboardInterrupt:
    print("Programa detenido por el usuario.")
except Exception as e:
    print(f"Error inesperado: {e}")
finally:
    print("Saliendo del programa...")
    sys.exit(0)