from customtkinter import *
import itertools

class PantallaInicio(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#0f172a")
        glow_colors = ["#a6d6f7", "#FFCC70", "#C850C0", "#FFFFFF"]
        self.color_cycle = itertools.cycle(glow_colors)

        title_label = CTkLabel(self, text="✨ H A N D O R A ✨", font=("Arial Rounded MT Bold", 32), text_color="#a6d6f7")
        title_label.place(relx=0.5, rely=0.15, anchor="center")

        def animate_title():
            title_label.configure(text_color=next(self.color_cycle))
            self.after(300, animate_title)
        animate_title()

        btn = CTkButton(
            self,
            text="🚀 Comenzar traducción",
            font=("Segoe UI", 16, "bold"),
            corner_radius=50,
            width=280,
            height=50,
            fg_color="#C850C0",
            hover_color="#FF69B4",
            border_color="#FFCC70",
            border_width=2,
            text_color="#ffffff",
            command=self.iniciar_traductor
        )
        btn.place(relx=0.5, rely=0.5, anchor="center")

        footer = CTkLabel(
            self,
            text="Lenguaje de Señas - powered by Handora - Hecho por Estudiantes de La Universidad Católica De Cuenca",
            font=("Arial", 12),
            text_color="#94a3b8"
        )
        footer.place(relx=0.5, rely=0.93, anchor="center")

    def iniciar_traductor(self):
        from ui import interfaz
        self.controller.mostrar_pantalla(interfaz.TraductorSenasApp)
