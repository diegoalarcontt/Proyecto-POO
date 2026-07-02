"""
Modelos principales del Sistema de Reubicación de Gimnasios.
Este archivo contiene las clases del dominio del problema.
"""


class Persona:
    """Clase base para representar una persona dentro del sistema."""

    def __init__(self, nombre, comuna):
        self._nombre = nombre
        self._comuna = comuna

    @property
    def nombre(self):
        return self._nombre

    @property
    def comuna(self):
        return self._comuna

    def obtener_descripcion(self):
        """Método que puede ser redefinido por las clases hijas."""
        return f"Persona: {self.nombre}, comuna: {self.comuna}"


class Usuario(Persona):
    """Representa a un usuario afectado por el cierre de un gimnasio."""

    def __init__(self, nombre, comuna, presupuesto, membresia_preferida, servicios_preferidos):
        super().__init__(nombre, comuna)
        self._presupuesto = presupuesto
        self._membresia_preferida = membresia_preferida
        self._servicios_preferidos = servicios_preferidos

    @property
    def presupuesto(self):
        return self._presupuesto

    @property
    def membresia_preferida(self):
        return self._membresia_preferida

    @property
    def servicios_preferidos(self):
        return self._servicios_preferidos

    def obtener_descripcion(self):
        return (
            f"Usuario: {self.nombre} | Comuna: {self.comuna} | "
            f"Presupuesto: ${self.presupuesto:,} | Membresía: {self.membresia_preferida}"
        ).replace(",", ".")


class Administrador(Persona):
    """Representa a un administrador que puede revisar solicitudes."""

    def __init__(self, nombre, comuna, cargo):
        super().__init__(nombre, comuna)
        self._cargo = cargo

    @property
    def cargo(self):
        return self._cargo

    def obtener_descripcion(self):
        return f"Administrador: {self.nombre} | Cargo: {self.cargo}"


class Membresia:
    """Representa un tipo de membresía ofrecida por un gimnasio."""

    def __init__(self, tipo, precio, duracion_meses):
        self._tipo = tipo
        self._precio = precio
        self._duracion_meses = duracion_meses

    @property
    def tipo(self):
        return self._tipo

    @property
    def precio(self):
        return self._precio

    @property
    def duracion_meses(self):
        return self._duracion_meses

    def __str__(self):
        return f"{self.tipo} (${self.precio:,})".replace(",", ".")


class Gimnasio:
    """Representa un gimnasio disponible para reubicar usuarios."""

    def __init__(self, nombre, comuna, precio_mensual, horario, servicios, membresias):
        self._nombre = nombre
        self._comuna = comuna
        self._precio_mensual = precio_mensual
        self._horario = horario
        self._servicios = servicios
        self._membresias = membresias

    @property
    def nombre(self):
        return self._nombre

    @property
    def comuna(self):
        return self._comuna

    @property
    def precio_mensual(self):
        return self._precio_mensual

    @property
    def horario(self):
        return self._horario

    @property
    def servicios(self):
        return self._servicios

    @property
    def membresias(self):
        return self._membresias

    def tipos_membresia(self):
        return [m.tipo for m in self.membresias]

    def calcular_puntaje(self, usuario):
        """
        Calcula un puntaje de recomendación.
        Mientras más alto el puntaje, mejor se ajusta el gimnasio al usuario.
        """
        puntaje = 0

        if self.comuna.lower() == usuario.comuna.lower():
            puntaje += 3

        if self.precio_mensual <= usuario.presupuesto:
            puntaje += 3
        else:
            diferencia = self.precio_mensual - usuario.presupuesto
            if diferencia <= 5000:
                puntaje += 1

        if usuario.membresia_preferida in self.tipos_membresia():
            puntaje += 2

        for servicio in usuario.servicios_preferidos:
            if servicio in self.servicios:
                puntaje += 1

        return puntaje

    def obtener_motivo_recomendacion(self, usuario):
        """Entrega una explicación breve del motivo de recomendación."""
        motivos = []

        if self.comuna.lower() == usuario.comuna.lower():
            motivos.append("está en la misma comuna")

        if self.precio_mensual <= usuario.presupuesto:
            motivos.append("se ajusta al presupuesto")
        else:
            motivos.append("supera un poco el presupuesto, pero puede ser una alternativa")

        servicios_encontrados = [s for s in usuario.servicios_preferidos if s in self.servicios]
        if servicios_encontrados:
            motivos.append("incluye servicios solicitados: " + ", ".join(servicios_encontrados))

        if usuario.membresia_preferida in self.tipos_membresia():
            motivos.append("ofrece la membresía solicitada")

        if not motivos:
            motivos.append("es una alternativa disponible dentro del sistema")

        return "; ".join(motivos).capitalize() + "."


class SolicitudReubicacion:
    """Representa una solicitud creada por un usuario para reubicarse en un gimnasio."""

    contador = 1

    def __init__(self, usuario, gimnasio):
        self._id_solicitud = SolicitudReubicacion.contador
        SolicitudReubicacion.contador += 1
        self._usuario = usuario
        self._gimnasio = gimnasio
        self._estado = "Pendiente"

    @property
    def id_solicitud(self):
        return self._id_solicitud

    @property
    def usuario(self):
        return self._usuario

    @property
    def gimnasio(self):
        return self._gimnasio

    @property
    def estado(self):
        return self._estado

    def aprobar(self):
        self._estado = "Aprobada"

    def rechazar(self):
        self._estado = "Rechazada"

    def resumen(self):
        return (
            f"Solicitud #{self.id_solicitud} | Usuario: {self.usuario.nombre} | "
            f"Gimnasio: {self.gimnasio.nombre} | Estado: {self.estado}"
        )
