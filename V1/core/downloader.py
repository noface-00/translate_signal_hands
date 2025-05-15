# core/downloader.py
import os
import yt_dlp
from pydub import AudioSegment

class VideoDownloader:
    def __init__(self, output_video_path, output_audio_path):
        self.video_path = output_video_path
        self.audio_path = output_audio_path

        # Asegurar que las carpetas existan
        os.makedirs(os.path.dirname(self.video_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.audio_path), exist_ok=True)

    def download(self, url):
        opciones = {
            'outtmpl': self.video_path.replace(".mp4", ".%(ext)s"),
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4'
        }
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url])

    def extract_audio(self):
        print(f"[DEBUG] Extrayendo audio desde: {self.video_path}")
        if not os.path.exists(self.video_path):
            raise FileNotFoundError(f"El video no existe: {self.video_path}")
    
        try:
            audio = AudioSegment.from_file(self.video_path)
            print(f"[DEBUG] Audio cargado, exportando a: {self.audio_path}")
            audio.export(self.audio_path, format="wav")
            print("[DEBUG] Exportación completa.")
        except Exception as e:
            print(f"[ERROR] Fallo en exportar audio: {e}")
            raise

