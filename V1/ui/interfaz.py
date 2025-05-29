import os
import vlc
import threading
import time
import gc
import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from core.downloader import VideoDownloader
from core.transcriber import AudioTranscriber
from core.animator import Animator

class TraductorSenasApp(ctk.CTkFrame):
    
    def __init__(self, root, parent, controller=None):
        super().__init__(parent, fg_color="#0f172a")
        self.controller = controller
        self.root = root
        self.configure(fg_color="#0f172a")
        self.CARPETA_letras = os.path.normpath("Assets/Letras")
        self.CARPETA_Palabras = os.path.normpath("Assets/Palabras")
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
        # TITULO
        ctk.CTkLabel(
            self,
            text="✨ Handora: Translate Live Transcript ✨", 
            font=("Segoe UI", 24, "bold"),
            text_color="#7c3aed"
        ).pack(pady=(0, 10))  # 0 arriba, 10 abajo
        # URL DEL VIDEO
        frame_url = ctk.CTkFrame(self, fg_color="#0f172a")
        frame_url.pack(pady=(0,10))
        ctk.CTkLabel(frame_url, text="🎥 URL del video:", font=("Segoe UI", 12), text_color="#f8fafc").pack(side="left", padx=5)
        self.url_video = ctk.CTkEntry(frame_url, width=450, font=("Segoe UI", 12), text_color="#f8fafc")
        self.url_video.pack(side="left", padx=10)
        ctk.CTkButton(
            frame_url,
            text="▶ Descargar y Reproducir",
            command=self.descargar_y_reproducir,
            fg_color="#7c3aed",
            hover_color="#a78bfa",
            text_color="white"
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            frame_url,
            text="♻ Transcribir nuevo video",
            command=self.reemplazar_video,
            fg_color="#d93025",
            hover_color="#c5221f",
            text_color="white"
        ).pack(side="left")
        # REPRODUCTOR DE VIDEO
        self.frame_video_texto = ctk.CTkFrame(self, fg_color="#0f172a")
        self.frame_video_texto.pack(pady=10, fill="both", expand=True)

        self.frame_video = ctk.CTkFrame(self.frame_video_texto, width=640, height=360, fg_color="black")
        self.frame_video.pack(side="left", padx=10, pady=5)

        self.entrada = ctk.CTkTextbox(
            self.frame_video_texto,
            width=480,
            height=240,
            font=("Segoe UI", 12),
            wrap="word",
            fg_color="#1e293b",
            text_color="#f8fafc"
        )
        self.entrada.pack(side="left", padx=10)
        self.entrada.tag_config("resaltado", background="#facc15")
        #self.entrada.configure(state="disabled")  # No editable

        frame_controles = ctk.CTkFrame(self, fg_color="#0f172a")
        frame_controles.pack(pady=5)
        ctk.CTkButton(
            frame_controles,
            text="⏸ Pausar Video",
            command=self.pausar_video,
            fg_color="#facc15",
            text_color="#000000"
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            frame_controles,
            text="▶ Reanudar Video",
            command=self.reanudar_video,
            fg_color="#22d3ee",
            text_color="#0f172a"
        ).pack(side="left", padx=5)

        self.frame_visual = ctk.CTkFrame(self, fg_color="#0f172a")
        self.frame_visual.pack(fill="both", expand=True, padx=20, pady=10)

        self.frame_animacion = ctk.CTkFrame(self.frame_visual, fg_color="#1e293b", width=700)
        self.frame_animacion.pack(side="left", fill="both", expand=True, padx=10)

        self.frame_historial = ctk.CTkFrame(self.frame_visual, fg_color="#1e293b", width=220, border_color="#334155", border_width=1)
        self.frame_historial.pack(side="right", fill="y")
        ctk.CTkLabel(
            self.frame_historial,
            text="Historial",
            font=("Segoe UI", 14, "bold"),
            text_color="#f8fafc"
        ).pack(pady=10)

    def descargar_y_reproducir(self):
        url = self.url_video.get().strip()
        if not url:
            messagebox.showwarning("Advertencia", "Por favor ingresa una URL.")
            return
        threading.Thread(target=self._procesar_video, args=(url,)).start()

    def reemplazar_video(self):
        ruta_video = os.path.join(self.CARPETA_VIDEO, "video_descargado.mp4")
        ruta_audio = os.path.join(self.CARPETA_AUDIO, "audio.wav")

        try:
            if self.player.is_playing():
                self.player.stop()
            time.sleep(0.5)
            self.player.release()
            self.vlc_instance = vlc.Instance()
            self.player = self.vlc_instance.media_player_new()
            gc.collect()

            if os.path.exists(ruta_video):
                os.remove(ruta_video)
            if os.path.exists(ruta_audio):
                os.remove(ruta_audio)
            self.entrada.delete("1.0", "end")
            messagebox.showinfo("Listo", "Archivos anteriores eliminados. Ingresa una nueva URL y presiona Descargar.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron eliminar los archivos: {str(e)}")

    def _procesar_video(self, url):
        try:
            ruta_video = os.path.join(self.CARPETA_VIDEO, "video_descargado.mp4")
            ruta_audio = os.path.join(self.CARPETA_AUDIO, "audio.wav")

            downloader = VideoDownloader(ruta_video, ruta_audio)
            downloader.download(url)
            downloader.extract_audio()

            transcriptor = AudioTranscriber()
            self.texto_transcrito, self.posiciones_palabras = transcriptor.transcribir_audio(ruta_audio)

            self.entrada.delete("1.0", "end")
            self.entrada.insert("end", self.texto_transcrito)

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

            timeout = 10
            start_wait = time.time()
            while (not self.player or not self.player.is_playing()) and (time.time() - start_wait < timeout):
                time.sleep(0.1)

            if not self.player:
                print("⚠ Reproductor no disponible.")
                return

            try:
                while self.player.get_time() < inicio:
                    time.sleep(0.05)
            except Exception as e:
                print(f"⚠ Error accediendo al tiempo del reproductor: {e}")
                return

            self.resaltar_texto(original)
            self.animator.mostrar(original)

    def resaltar_texto(self, palabra_actual):
        texto = self.entrada.get("1.0", "end")
        self.entrada.tag_remove("resaltado", "1.0", "end")
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
    root = ctk.CTk()
    app = TraductorSenasApp(root, root)

    def al_cerrar():
        try:
            ruta_video = os.path.join(app.CARPETA_VIDEO, "video_descargado.mp4")
            ruta_audio = os.path.join(app.CARPETA_AUDIO, "audio.wav")
            if os.path.exists(ruta_video):
                os.remove(ruta_video)
            if os.path.exists(ruta_audio):
                os.remove(ruta_audio)
            print("🧹 Archivos eliminados al cerrar.")
        except Exception as e:
            print(f"⚠ Error al eliminar archivos al cerrar: {e}")
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", al_cerrar)
    root.mainloop()
