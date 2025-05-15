import os
from PIL import Image, ImageTk
import tkinter as tk

class Animator:
    def __init__(self, frame_animacion, frame_historial, carpeta_letras, carpeta_palabras, palabras_gif):
        self.frame_animacion = frame_animacion
        self.frame_historial = frame_historial
        self.carpeta_letras = carpeta_letras
        self.carpeta_palabras = carpeta_palabras
        self.palabras_gif = palabras_gif
        self.frames_gif = []
        self.indice_gif = 0
        self.label_animacion = None

    def mostrar(self, palabra):
        # Limpiar animación e historial
        for widget in self.frame_animacion.winfo_children():
            widget.destroy()
        for widget in self.frame_historial.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("text") != "Historial":
                widget.destroy()

        # Mostrar en historial
        tk.Label(self.frame_historial, text=palabra, font=("Segoe UI", 12), bg="white", anchor="w").pack(fill=tk.X, padx=5)

        # Mostrar GIF si existe
        if palabra in self.palabras_gif:
            ruta = os.path.join(self.carpeta_palabras, f"{palabra}.gif")
            if os.path.exists(ruta):
                self.reproducir_gif(ruta)
                return

        # Mostrar letras una por una
        frame_contenedor = tk.Frame(self.frame_animacion, bg="#fafafa")
        frame_contenedor.pack()

        for letra in palabra:
            ruta_letra = os.path.join(self.carpeta_letras, f"{letra}.png")
            print(f"[DEBUG] Buscando imagen: {ruta_letra}")
            if os.path.exists(ruta_letra):
                try:
                    img = Image.open(ruta_letra).resize((60, 90))
                    img_tk = ImageTk.PhotoImage(img)
                    lbl = tk.Label(frame_contenedor, image=img_tk, bg="#fafafa")
                    lbl.image = img_tk  # Mantener referencia
                    lbl.pack(side=tk.LEFT, padx=2)
                except Exception as e:
                    print(f"[ERROR] Al cargar letra '{letra}': {e}")
            else:
                print(f"[AVISO] Imagen no encontrada: {ruta_letra}")

    def reproducir_gif(self, ruta):
        from PIL import Image
        gif = Image.open(ruta)
        self.frames_gif = []
        try:
            for frame in range(gif.n_frames):
                gif.seek(frame)
                img = gif.copy().convert("RGBA").resize((250, 170))
                self.frames_gif.append(ImageTk.PhotoImage(img))
        except Exception as e:
            print(f"[ERROR] Al leer gif: {e}")
        self.indice_gif = 0
        if self.label_animacion and self.label_animacion.winfo_exists():
            self.label_animacion.destroy()
        self.label_animacion = tk.Label(self.frame_animacion, bg="#fafafa")
        self.label_animacion.pack()
        self.mostrar_frame_gif()

    def mostrar_frame_gif(self):
        if not self.frames_gif:
            return
        if self.indice_gif >= len(self.frames_gif):
            self.indice_gif = 0  # Repetir el gif
        if not self.label_animacion or not self.label_animacion.winfo_exists():
            return
        frame = self.frames_gif[self.indice_gif]
        self.label_animacion.configure(image=frame)
        self.label_animacion.image = frame
        self.indice_gif += 1
        self.frame_animacion.after(100, self.mostrar_frame_gif)
