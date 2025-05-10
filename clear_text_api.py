import os
from openai import OpenAI

class LimpiezaTexto:
    def __init__(self, ruta_key_env, base_url="https://openrouter.ai/api/v1"):
        self.api_key = self.cargar_clave_api(ruta_key_env)
        self.client = OpenAI(api_key=self.api_key, base_url=base_url)

    def cargar_clave_api(self, ruta):
        if os.path.exists(ruta):
            with open(ruta, "r") as archivo:
                return archivo.read().strip()
        else:
            raise FileNotFoundError(f"El archivo {ruta} no existe.")
        
    def limpiar_muletillas(self, texto_org):
        chat = self.client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[
                {"role": "system", "content": "Eres un asistente experto en redacción en español."},
                {"role": "user", "content": f"Toma el siguiente texto y elimínale todas las muletillas. Después, reestructura el texto si es necesario para que mantenga el sentido natural, claro y coherente en español. Solo envíame el texto limpio.\n{texto_org}"}
            ]
        )
        return chat.choices[0].message.content