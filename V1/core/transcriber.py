# core/transcriber.py
import assemblyai as aai
import unicodedata
from openai import OpenAI
import os
class AudioTranscriber:
    def __init__(self):
        api_key_aai = os.environ.get("AAI_KEY")
        api_key_deepseek = os.environ.get("ROUTER_KEY")

        if not api_key_aai or not api_key_deepseek:
            raise EnvironmentError("Faltan variables de entorno AAI_KEY o ROUTER_KEY")

        aai.settings.api_key = api_key_aai
        self.client = OpenAI(api_key=api_key_deepseek, base_url="https://openrouter.ai/api/v1")
    def transcribir_audio(self, ruta_audio):
        config = aai.TranscriptionConfig(
            language_code="es",
            punctuate=True,
            format_text=True
        )
        transcriber = aai.Transcriber(config=config)
        transcript = transcriber.transcribe(ruta_audio)
        print(f"Transcripción Completada!")
        # Texto limpio con IA de depuración
        texto_depurado = self.promp_depurar_texto(transcript.text)
        texto_final = self.quitar_acentos(texto_depurado.upper())
        print(f"Texto depurado!")
        # Palabras con timestamps
        palabras = [
            (
                self.quitar_acentos(w.text.upper()),
                w.start,
                self.quitar_acentos(w.text.upper()),
                w.end
            ) for w in transcript.words
        ]

        return texto_final, palabras

    def cargar_clave_env(self, ruta_archivo):
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            for linea in f:
                if "=" in linea:
                    _, valor = linea.strip().split("=", 1)
                    return valor.strip()
        raise ValueError(f"No se encontró una clave válida en {ruta_archivo}")

    def quitar_acentos(self, texto):
        return ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
        )

    def promp_depurar_texto(self, texto_org):
        chat = self.client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[
                {"role": "system", "content": "Eres un asistente experto en redacción en español."},
                {"role": "user", "content": f"Toma el siguiente texto y reestructúralo si es necesario para que mantenga el sentido natural, claro y coherente en español. Solo responde con el texto depurado.\n{texto_org}"}
            ]
        )
        return chat.choices[0].message.content

    def transcribir_desde_txt(self, ruta_txt):
        with open(ruta_txt, "r", encoding="utf-8") as archivo:
            texto_original = archivo.read()

        # Depurar usando la IA
        texto_depurado = self.promp_depurar_texto(texto_original)
        texto_final = self.quitar_acentos(texto_depurado.upper())

        return texto_final
