import os
import sys
import customtkinter as ctk
from dotenv import load_dotenv
from ui import interfaz
from ui import pantalla_inicio

env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

print("AAI_KEY:", os.environ.get("AAI_KEY"))
print("ROUTER_KEY:", os.environ.get("ROUTER_KEY"))

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Handora")
        self.configure(fg_color="#0f172a")

        # ✅ Tamaño deseado de la ventana
        window_width = 1280
        window_height = 720

        # ✅ Tamaño de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # ✅ Coordenadas para centrar
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)

        # ✅ Aplicar tamaño y posición
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Container que contendrá tus pantallas
        self.container = ctk.CTkFrame(self, fg_color="#0f172a")
        self.container.place(x=0, y=0, relwidth=1, relheight=1)

        self.frames = {}
        self.mostrar_pantalla(pantalla_inicio.PantallaInicio)


    def mostrar_pantalla(self, clase_pantalla):
        frame_actual = self.frames.get('pantalla')
        if frame_actual:
            frame_actual.destroy()

        nueva_pantalla = clase_pantalla(self.container, self)
        nueva_pantalla.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.frames['pantalla'] = nueva_pantalla

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = MainApp()
    app.mainloop()
    sys.exit(0)  # ✅ Aseguramos que el script termine correctamente