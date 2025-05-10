import yt_dlp
import os

class URLAudioTranscriber:

    def __init__(self, url, carpeta = "Mis_Audios"):
        self.url = url
        self.carpeta = carpeta

    def descarga(self):
        try:
            if not os.path.exists(self.carpeta):
                os.makedirs(self.carpeta) 

            opciones = {
                'format': 'bestaudio/best',
                'outtmpl': f'{self.carpeta}/%(title)s.%(ext)s'
            }
            print("Descargando audio de YouTube......")
            with yt_dlp.YoutubeDL(opciones) as ydl:
                ydl.download([self.url])
            print("¡Descarga completada!")
        except Exception as e:
            print(f"Ocurrió un error: {e}")

    
