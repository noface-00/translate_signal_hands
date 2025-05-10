import os
from pydub import AudioSegment
import whisper
import torch

class AudioTranscriber:
    def __init__(self, nombre_archivo_webm, carpeta_audio="Mis_Audios", carpeta_salida="Transcripciones"):
        self.archivo_webm = nombre_archivo_webm
        self.carpeta_audio = carpeta_audio
        self.carpeta_salida = carpeta_salida
        self.ruta_webm = os.path.join(carpeta_audio, nombre_archivo_webm)
        self.nombre_base = os.path.splitext(nombre_archivo_webm)[0]
        self.ruta_wav = os.path.join(carpeta_audio, f"{self.nombre_base}.wav")
        self.ruta_txt = os.path.join(carpeta_salida, f"{self.nombre_base}.txt")

        # Crea la carpeta de transcripciones si no existe
        os.makedirs(self.carpeta_salida, exist_ok=True)

    def convertir_a_wav(self):
        if not os.path.exists(self.ruta_webm) or not self.archivo_webm.lower().endswith(".webm"):
            raise FileNotFoundError(f"El archivo {self.archivo_webm} no se encuentra o no es .webm")
        
        print(f"Convirtiendo {self.archivo_webm} a WAV...")
        audio = AudioSegment.from_file(self.ruta_webm, format="webm")
        audio.export(self.ruta_wav, format="wav")
        print(f"Archivo convertido: {self.ruta_wav}")
        return self.ruta_wav
    
    def transcribir_audio(self):
        print("Cargando modelo Whisper...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = whisper.load_model("medium", device=device)
        print("Transcribiendo...")
        result = model.transcribe(self.ruta_wav, language="es")

        with open(self.ruta_txt, "w", encoding="utf-8") as f:
            for segment in result["segments"]:
                f.write(segment["text"].strip() + "\n")
        
        print(f"Transcripción guardada en {self.ruta_txt}")
        print("Dispositivo usado:", model.device)
        return result["text"], self.ruta_txt
