import os
from pydub import AudioSegment
import whisper

carpeta_audio = "Mis_Audios"
archivo_webm = "Prueba3.webm"  
carpeta_salida = "Transcripciones"
os.makedirs(carpeta_salida, exist_ok=True)




ruta_webm = os.path.join(carpeta_audio, archivo_webm)
if not os.path.exists(ruta_webm) or not archivo_webm.lower().endswith(".webm"):
    print(f"El archivo {archivo_webm} no se encuentra en la carpeta {carpeta_audio} o no tiene la extensión .webm.")
    exit()

nombre_base = os.path.splitext(archivo_webm)[0]
ruta_wav = os.path.join(carpeta_audio, f"{nombre_base}.wav")

print(f"Convirtiendo {archivo_webm} a formato WAV...")
audio = AudioSegment.from_file(ruta_webm, format="webm")
audio.export(ruta_wav, format="wav")
print(f"Archivo convertido: {ruta_wav}")


print("Cargando modelo Whisper...")
model = whisper.load_model("medium") 


print("Transcribiendo con Whisper...")
result = model.transcribe(ruta_wav, language="es")


ruta_txt = os.path.join(carpeta_salida, f"{nombre_base}.txt")
with open(ruta_txt, "w", encoding="utf-8") as f:
    for segment in result["segments"]:
        f.write(segment["text"].strip() + "\n")

print(f"Transcripción guardada en {ruta_txt}")
