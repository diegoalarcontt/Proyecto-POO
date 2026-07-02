"""
Interfaz gráfica del Sistema de Reubicación de Gimnasios.
Se utiliza Tkinter, que viene incluido con Python.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from models import Usuario
from sistema import SistemaReubicacion


class AplicacionGimnasios:
    """Ventana principal de la aplicación."""

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Reubicación de Gimnasios")
        self.root.geometry("1280x760")
        self.root.minsize(1000, 620)

        self.sistema = SistemaReubicacion()
        self.usuario_actual = None
        self.resultados_actuales = []

        self.servicios_vars = {}
        self.crear_interfaz()

    def crear_interfaz(self):
        titulo = ttk.Label(
            self.root,
            text="Sistema de Reubicación de Usuarios Afectados por el Cierre de Gimnasios",
            font=("Arial", 16, "bold"),
        )
        titulo.pack(pady=10)

        contenedor = ttk.Frame(self.root, padding=10)
        contenedor.pack(fill="both", expand=True)
        contenedor.columnconfigure(1, weight=1)
        contenedor.rowconfigure(0, weight=1)

        # ------------------------------------------------------------------
        # Panel izquierdo con barra de desplazamiento.
        # Esto evita que se corten los botones cuando la pantalla es pequeña.
        # ------------------------------------------------------------------
        panel_formulario = ttk.LabelFrame(contenedor, text="Datos del usuario", padding=0)
        panel_formulario.grid(row=0, column=0, sticky="ns", padx=(0, 10))

        self.canvas_formulario = tk.Canvas(panel_formulario, width=340, highlightthickness=0)
        scrollbar_formulario = ttk.Scrollbar(
            panel_formulario,
            orient="vertical",
            command=self.canvas_formulario.yview,
        )
        self.canvas_formulario.configure(yscrollcommand=scrollbar_formulario.set)

        self.frame_formulario = ttk.Frame(self.canvas_formulario, padding=10)
        self.ventana_formulario = self.canvas_formulario.create_window(
            (0, 0),
            window=self.frame_formulario,
            anchor="nw",
        )

        self.canvas_formulario.pack(side="left", fill="both", expand=True)
        scrollbar_formulario.pack(side="right", fill="y")

        self.frame_formulario.bind(
            "<Configure>",
            lambda event: self.canvas_formulario.configure(
                scrollregion=self.canvas_formulario.bbox("all")
            ),
        )
        self.canvas_formulario.bind(
            "<Configure>",
            lambda event: self.canvas_formulario.itemconfigure(
                self.ventana_formulario,
                width=event.width,
            ),
        )

        panel_formulario.bind("<Enter>", self.activar_scroll_formulario)
        panel_formulario.bind("<Leave>", self.desactivar_scroll_formulario)

        # Campos del formulario
        ttk.Label(self.frame_formulario, text="Nombre:").pack(anchor="w")
        self.entry_nombre = ttk.Entry(self.frame_formulario, width=32)
        self.entry_nombre.pack(fill="x", pady=4)

        ttk.Label(self.frame_formulario, text="Comuna:").pack(anchor="w")
        self.combo_comuna = ttk.Combobox(
            self.frame_formulario,
            values=self.sistema.obtener_comunas(),
            state="readonly",
            width=29,
        )
        self.combo_comuna.pack(fill="x", pady=4)
        if "Santiago Centro" in self.sistema.obtener_comunas():
            self.combo_comuna.set("Santiago Centro")
        else:
            self.combo_comuna.current(0)

        ttk.Label(self.frame_formulario, text="Presupuesto máximo mensual ($):").pack(anchor="w")
        self.entry_presupuesto = ttk.Entry(self.frame_formulario, width=32)
        self.entry_presupuesto.pack(fill="x", pady=4)
        self.entry_presupuesto.insert(0, "40000")

        ttk.Label(self.frame_formulario, text="Tipo de membresía:").pack(anchor="w")
        self.combo_membresia = ttk.Combobox(
            self.frame_formulario,
            values=["Mensual", "Trimestral", "Semestral", "Anual"],
            state="readonly",
            width=29,
        )
        self.combo_membresia.pack(fill="x", pady=4)
        self.combo_membresia.set("Mensual")

        ttk.Label(self.frame_formulario, text="Servicios preferidos:").pack(anchor="w", pady=(10, 2))
        servicios = [
            "Máquinas",
            "Duchas",
            "Clases grupales",
            "Personal trainer",
            "Nutrición",
            "Estacionamiento",
            "24/7",
            "Piscina",
            "Spa",
            "Pilates",
            "Spinning",
            "Boxeo",
            "CrossFit",
            "Funcional",
            "App de entrenamiento",
            "Kinesiólogo",
            "Evaluación corporal",
        ]

        # Servicios en dos columnas para ocupar menos alto en la pantalla.
        frame_servicios = ttk.Frame(self.frame_formulario)
        frame_servicios.pack(fill="x")
        for indice, servicio in enumerate(servicios):
            var = tk.BooleanVar()
            check = ttk.Checkbutton(frame_servicios, text=servicio, variable=var)
            check.grid(row=indice // 2, column=indice % 2, sticky="w", padx=(0, 10), pady=1)
            self.servicios_vars[servicio] = var

        self.servicios_vars["Máquinas"].set(True)
        self.servicios_vars["Duchas"].set(True)
        self.servicios_vars["Clases grupales"].set(True)

        ttk.Button(
            self.frame_formulario,
            text="Buscar recomendación",
            command=self.buscar_recomendacion,
        ).pack(fill="x", pady=(15, 5))

        ttk.Button(
            self.frame_formulario,
            text="Crear solicitud con gimnasio seleccionado",
            command=self.crear_solicitud,
        ).pack(fill="x", pady=5)

        ttk.Button(
            self.frame_formulario,
            text="Mostrar todos los gimnasios",
            command=self.mostrar_todos_los_gimnasios,
        ).pack(fill="x", pady=5)

        ttk.Button(
            self.frame_formulario,
            text="Limpiar resultados",
            command=self.limpiar_resultados,
        ).pack(fill="x", pady=5)

        # ------------------------------------------------------------------
        # Panel derecho con resultados.
        # ------------------------------------------------------------------
        panel_resultados = ttk.LabelFrame(contenedor, text="Resultados", padding=10)
        panel_resultados.grid(row=0, column=1, sticky="nsew")
        panel_resultados.columnconfigure(0, weight=1)
        panel_resultados.rowconfigure(0, weight=1)
        panel_resultados.rowconfigure(2, weight=1)

        columnas = ("nombre", "comuna", "precio", "membresias", "puntaje")
        self.tabla = ttk.Treeview(panel_resultados, columns=columnas, show="headings", height=12)
        self.tabla.heading("nombre", text="Gimnasio")
        self.tabla.heading("comuna", text="Comuna")
        self.tabla.heading("precio", text="Precio mensual")
        self.tabla.heading("membresias", text="Membresías")
        self.tabla.heading("puntaje", text="Puntaje")

        self.tabla.column("nombre", width=240)
        self.tabla.column("comuna", width=140)
        self.tabla.column("precio", width=120)
        self.tabla.column("membresias", width=260)
        self.tabla.column("puntaje", width=80, anchor="center")

        scrollbar_tabla_y = ttk.Scrollbar(panel_resultados, orient="vertical", command=self.tabla.yview)
        scrollbar_tabla_x = ttk.Scrollbar(panel_resultados, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=scrollbar_tabla_y.set, xscrollcommand=scrollbar_tabla_x.set)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scrollbar_tabla_y.grid(row=0, column=1, sticky="ns")
        scrollbar_tabla_x.grid(row=1, column=0, sticky="ew")
        self.tabla.bind("<<TreeviewSelect>>", self.mostrar_detalle_seleccionado)

        ttk.Label(panel_resultados, text="Detalle / motivo de recomendación:").grid(
            row=2,
            column=0,
            sticky="sw",
            pady=(10, 2),
        )

        frame_detalle = ttk.Frame(panel_resultados)
        frame_detalle.grid(row=3, column=0, columnspan=2, sticky="nsew")
        frame_detalle.columnconfigure(0, weight=1)
        frame_detalle.rowconfigure(0, weight=1)

        self.texto_detalle = tk.Text(frame_detalle, height=10, wrap="word")
        scrollbar_detalle = ttk.Scrollbar(frame_detalle, orient="vertical", command=self.texto_detalle.yview)
        self.texto_detalle.configure(yscrollcommand=scrollbar_detalle.set)
        self.texto_detalle.grid(row=0, column=0, sticky="nsew")
        scrollbar_detalle.grid(row=0, column=1, sticky="ns")

        self.label_estado = ttk.Label(self.root, text="Listo para buscar recomendaciones.")
        self.label_estado.pack(pady=5)

    def activar_scroll_formulario(self, event=None):
        """Permite usar la rueda del mouse sobre el panel izquierdo."""
        self.root.bind_all("<MouseWheel>", self.scroll_formulario)
        self.root.bind_all("<Button-4>", self.scroll_formulario)
        self.root.bind_all("<Button-5>", self.scroll_formulario)

    def desactivar_scroll_formulario(self, event=None):
        """Desactiva el scroll del panel izquierdo al salir con el mouse."""
        self.root.unbind_all("<MouseWheel>")
        self.root.unbind_all("<Button-4>")
        self.root.unbind_all("<Button-5>")

    def scroll_formulario(self, event):
        """Mueve el formulario hacia arriba o abajo."""
        if event.num == 4:
            self.canvas_formulario.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas_formulario.yview_scroll(1, "units")
        else:
            self.canvas_formulario.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def obtener_servicios_seleccionados(self):
        return [servicio for servicio, var in self.servicios_vars.items() if var.get()]

    def validar_datos(self):
        nombre = self.entry_nombre.get().strip()
        comuna = self.combo_comuna.get().strip()
        membresia = self.combo_membresia.get().strip()
        servicios = self.obtener_servicios_seleccionados()

        if not nombre:
            messagebox.showerror("Error", "Debe ingresar el nombre del usuario.")
            return None

        try:
            presupuesto = int(self.entry_presupuesto.get().strip())
        except ValueError:
            messagebox.showerror("Error", "El presupuesto debe ser un número entero.")
            return None

        if presupuesto <= 0:
            messagebox.showerror("Error", "El presupuesto debe ser mayor a cero.")
            return None

        if not servicios:
            messagebox.showerror("Error", "Debe seleccionar al menos un servicio preferido.")
            return None

        return Usuario(nombre, comuna, presupuesto, membresia, servicios)

    def buscar_recomendacion(self):
        usuario = self.validar_datos()
        if usuario is None:
            return

        self.usuario_actual = usuario
        self.resultados_actuales = self.sistema.recomendar_gimnasios(usuario)
        self.cargar_resultados_en_tabla(self.resultados_actuales)

        self.texto_detalle.delete("1.0", tk.END)
        self.texto_detalle.insert(tk.END, usuario.obtener_descripcion() + "\n\n")
        self.texto_detalle.insert(
            tk.END,
            "Seleccione un gimnasio de la tabla para ver el motivo de recomendación.\n",
        )
        self.label_estado.config(text="Recomendaciones generadas correctamente.")

    def cargar_resultados_en_tabla(self, resultados):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for indice, (gimnasio, puntaje, motivo) in enumerate(resultados):
            self.tabla.insert(
                "",
                "end",
                iid=str(indice),
                values=(
                    gimnasio.nombre,
                    gimnasio.comuna,
                    f"${gimnasio.precio_mensual:,}".replace(",", "."),
                    ", ".join(gimnasio.tipos_membresia()),
                    puntaje,
                ),
            )

    def mostrar_detalle_seleccionado(self, event=None):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            return

        indice = int(seleccionado[0])

        if self.resultados_actuales:
            gimnasio, puntaje, motivo = self.resultados_actuales[indice]
        else:
            gimnasio = self.sistema.gimnasios[indice]
            puntaje = "-"
            motivo = "Gimnasio disponible dentro del sistema."

        self.texto_detalle.delete("1.0", tk.END)
        self.texto_detalle.insert(tk.END, f"Gimnasio: {gimnasio.nombre}\n")
        self.texto_detalle.insert(tk.END, f"Comuna: {gimnasio.comuna}\n")
        self.texto_detalle.insert(tk.END, f"Precio mensual: ${gimnasio.precio_mensual:,}\n".replace(",", "."))
        self.texto_detalle.insert(tk.END, f"Horario: {gimnasio.horario}\n")
        self.texto_detalle.insert(tk.END, f"Servicios: {', '.join(gimnasio.servicios)}\n")
        self.texto_detalle.insert(tk.END, f"Membresías: {', '.join(gimnasio.tipos_membresia())}\n")
        self.texto_detalle.insert(tk.END, f"Puntaje: {puntaje}\n\n")
        self.texto_detalle.insert(tk.END, "Motivo: " + motivo)

    def crear_solicitud(self):
        if self.usuario_actual is None:
            messagebox.showwarning("Atención", "Primero debe buscar una recomendación.")
            return

        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un gimnasio de la tabla.")
            return

        indice = int(seleccionado[0])
        gimnasio = self.resultados_actuales[indice][0]
        solicitud = self.sistema.crear_solicitud(self.usuario_actual, gimnasio)

        messagebox.showinfo(
            "Solicitud creada",
            solicitud.resumen(),
        )
        self.label_estado.config(text=f"Solicitud #{solicitud.id_solicitud} creada correctamente.")

    def mostrar_todos_los_gimnasios(self):
        self.resultados_actuales = []

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for indice, gimnasio in enumerate(self.sistema.gimnasios):
            self.tabla.insert(
                "",
                "end",
                iid=str(indice),
                values=(
                    gimnasio.nombre,
                    gimnasio.comuna,
                    f"${gimnasio.precio_mensual:,}".replace(",", "."),
                    ", ".join(gimnasio.tipos_membresia()),
                    "-",
                ),
            )

        self.texto_detalle.delete("1.0", tk.END)
        self.texto_detalle.insert(tk.END, "Listado de gimnasios disponibles.\n")
        self.label_estado.config(text="Mostrando todos los gimnasios disponibles.")

    def limpiar_resultados(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        self.texto_detalle.delete("1.0", tk.END)
        self.label_estado.config(text="Resultados limpiados.")
