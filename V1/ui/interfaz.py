import os
import vlc
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import threading
import time

from core.downloader import VideoDownloader
from core.transcriber import AudioTranscriber
from core.animator import Animator

class TraductorSenasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Handora")
        self.root.state("zoomed")
        self.root.configure(bg="#f0f4ff")

        # Carpetas con rutas relativas
        self.CARPETA_letras = os.path.normpath(r"Assets/Letras")
        self.CARPETA_Palabras = os.path.normpath(r"Assets/Palabras")

        self.CARPETA_AUDIO = os.path.normpath("Assets/Audio")
        self.CARPETA_VIDEO = os.path.normpath("Assets/Video")

        self.palabras_como_gif = {"HOLA", "ADIOS", "GRACIAS", "SI", "NO", "COMER", "DORMIR", "YO", "TU"}

        self.texto_transcrito = ""
        self.posiciones_palabras = []
        self.animacion_pausada = False

        self.vlc_instance = vlc.Instance()
        self.player = self.vlc_instance.media_player_new()

        self.crear_interfaz()

        self.animator = Animator(self.frame_animacion, self.frame_historial,
                                 self.CARPETA_letras, self.CARPETA_Palabras,
                                 self.palabras_como_gif)

    def crear_interfaz(self):
        tk.Label(self.root, text="Handora: Translate Live Transcript", font=("Segoe UI", 24, "bold"), bg="#f0f4ff", fg="#1a73e8").pack(pady=10)

        frame_url = tk.Frame(self.root, bg="#f0f4ff")
        frame_url.pack(pady=10)
        tk.Label(frame_url, text="URL del video:", font=("Segoe UI", 11), bg="#f0f4ff").pack(side=tk.LEFT)
        self.url_video = tk.Entry(frame_url, font=("Segoe UI", 11), width=60)
        self.url_video.pack(side=tk.LEFT, padx=10)
        tk.Button(frame_url, text="▶ Descargar y Reproducir", bg="#1a73e8", fg="white", command=self.descargar_y_reproducir).pack(side=tk.LEFT)

        self.frame_video_texto = tk.Frame(self.root, bg="#f0f4ff")
        self.frame_video_texto.pack(pady=10, fill=tk.X, expand=True)

        self.frame_video = tk.Frame(self.frame_video_texto, width=640, height=360, bg="black")
        self.frame_video.pack(side=tk.LEFT, padx=10)

        self.entrada = tk.Text(self.frame_video_texto, height=10, font=("Segoe UI", 12), width=60, wrap=tk.WORD)
        self.entrada.pack(side=tk.LEFT, padx=10)
        self.entrada.tag_config("resaltado", background="yellow")

        frame_controles = tk.Frame(self.root, bg="#f0f4ff")
        frame_controles.pack(pady=5)
        tk.Button(frame_controles, text="⏸ Pausar Video", command=self.pausar_video, bg="#fbbc04").pack(side=tk.LEFT, padx=5)
        tk.Button(frame_controles, text="▶ Reanudar Video", command=self.reanudar_video, bg="#34a853", fg="white").pack(side=tk.LEFT, padx=5)

        self.frame_visual = tk.Frame(self.root, bg="#fafafa")
        self.frame_visual.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.frame_animacion = tk.Frame(self.frame_visual, bg="#fafafa", width=700)
        self.frame_animacion.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.frame_historial = tk.Frame(self.frame_visual, bg="#ffffff", width=200, relief=tk.GROOVE, bd=2)
        self.frame_historial.pack(side=tk.RIGHT, fill=tk.Y)
        tk.Label(self.frame_historial, text="Historial", font=("Segoe UI", 14, "bold"), bg="white").pack(pady=5)

    def descargar_y_reproducir(self):
        url = self.url_video.get().strip()
        if not url:
            messagebox.showwarning("Advertencia", "Por favor ingresa una URL.")
            return
        threading.Thread(target=self._procesar_video, args=(url,)).start()

    def _procesar_video(self, url):
        try:
            ruta_video = os.path.join(self.CARPETA_VIDEO, "video_descargado.mp4")
            ruta_audio = os.path.join(self.CARPETA_AUDIO, "audio.wav")

            downloader = VideoDownloader(ruta_video, ruta_audio)
            downloader.download(url)
            downloader.extract_audio()

            transcriptor = AudioTranscriber()
            self.texto_transcrito, self.posiciones_palabras = transcriptor.transcribir_audio(ruta_audio)

            self.entrada.delete("1.0", tk.END)
            self.entrada.insert(tk.END, self.texto_transcrito)

            media = self.vlc_instance.media_new(ruta_video)
            self.player.set_media(media)
            self.player.set_hwnd(self.frame_video.winfo_id())
            self.player.play()

            threading.Thread(target=self.animacion_sincronizada).start()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar: {str(e)}")

    def animacion_sincronizada(self):
        for palabra, inicio, original, _ in self.posiciones_palabras:
            while self.animacion_pausada:
                time.sleep(0.1)
            while self.player.get_time() < inicio:
                time.sleep(0.05)
            self.resaltar_texto(original)
            self.animator.mostrar(original)

    def resaltar_texto(self, palabra_actual):
        texto = self.entrada.get("1.0", tk.END)
        self.entrada.tag_remove("resaltado", "1.0", tk.END)
        pos = texto.find(palabra_actual)
        if pos >= 0:
            start = f"1.0 + {pos} chars"
            end = f"1.0 + {pos + len(palabra_actual)} chars"
            self.entrada.tag_add("resaltado", start, end)
            self.entrada.see(start)

    def pausar_video(self):
        if self.player.is_playing():
            self.player.pause()

    def reanudar_video(self):
        self.player.play()

def main():
    import tkinter as tk
    root = tk.Tk()
    app = TraductorSenasApp(root)
    root.mainloop()

