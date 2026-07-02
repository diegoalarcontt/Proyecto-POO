"""
Lógica principal del sistema.
Aquí se administran los gimnasios disponibles, usuarios y solicitudes.
"""

from models import Gimnasio, Membresia, SolicitudReubicacion


class SistemaReubicacion:
    """Clase que coordina las operaciones principales de la aplicación."""

    def __init__(self):
        self._gimnasios = []
        self._solicitudes = []
        self.cargar_gimnasios_demo()

    @property
    def gimnasios(self):
        return self._gimnasios

    @property
    def solicitudes(self):
        return self._solicitudes

    def cargar_gimnasios_demo(self):
        """
        Carga gimnasios de Santiago para la demostración.
        Los nombres, comunas y servicios se basan en información pública revisada.
        Los precios se usan como valores referenciales para probar el sistema,
        por lo que deben confirmarse directamente con cada gimnasio.
        """
        mensual = lambda precio: Membresia("Mensual", precio, 1)
        trimestral = lambda precio: Membresia("Trimestral", precio, 3)
        semestral = lambda precio: Membresia("Semestral", precio, 6)
        anual = lambda precio: Membresia("Anual", precio, 12)

        self._gimnasios = [
            # Smart Fit - sedes de Santiago
            Gimnasio(
                "Smart Fit Vivo El Centro",
                "Santiago Centro",
                27900,
                "Lunes a viernes 06:00 a 23:00 / fin de semana horario reducido",
                ["Máquinas", "Duchas", "Clases grupales", "App de entrenamiento"],
                [mensual(27900), anual(334800)],
            ),
            Gimnasio(
                "Smart Fit Catedral",
                "Santiago Centro",
                34900,
                "Lunes a viernes 06:00 a 23:00 / fin de semana horario reducido",
                ["Máquinas", "Duchas", "Clases grupales", "App de entrenamiento"],
                [mensual(34900), anual(418800)],
            ),
            Gimnasio(
                "Smart Fit Espacio M",
                "Santiago Centro",
                34900,
                "Lunes a viernes 06:00 a 23:00 / fin de semana horario reducido",
                ["Máquinas", "Duchas", "Clases grupales", "App de entrenamiento"],
                [mensual(34900), anual(418800)],
            ),
            Gimnasio(
                "Smart Fit Portugal",
                "Santiago Centro",
                31900,
                "Lunes a viernes 06:00 a 23:00 / fin de semana horario reducido",
                ["Máquinas", "Duchas", "Clases grupales", "App de entrenamiento"],
                [mensual(31900), anual(382800)],
            ),
            Gimnasio(
                "Smart Fit Portal Ñuñoa",
                "Ñuñoa",
                32900,
                "Lunes a viernes 06:00 a 23:00 / fin de semana horario reducido",
                ["Máquinas", "Duchas", "Clases grupales", "App de entrenamiento"],
                [mensual(32900), anual(394800)],
            ),
            Gimnasio(
                "Smart Fit Mall Barrio Independencia",
                "Independencia",
                31900,
                "Lunes a viernes 06:00 a 23:00 / fin de semana horario reducido",
                ["Máquinas", "Duchas", "Clases grupales", "App de entrenamiento"],
                [mensual(31900), anual(382800)],
            ),
            Gimnasio(
                "Smart Fit Espacio Urbano Las Rejas",
                "Estación Central",
                31900,
                "Lunes a viernes 06:00 a 23:00 / fin de semana horario reducido",
                ["Máquinas", "Duchas", "Clases grupales", "App de entrenamiento"],
                [mensual(31900), anual(382800)],
            ),
            Gimnasio(
                "Smart Fit La Florida",
                "La Florida",
                31900,
                "Lunes a viernes 06:00 a 23:00 / fin de semana horario reducido",
                ["Máquinas", "Duchas", "Clases grupales", "App de entrenamiento"],
                [mensual(31900), anual(382800)],
            ),

            # Sportlife - Región Metropolitana
            Gimnasio(
                "Sportlife Ñuñoa",
                "Ñuñoa",
                38900,
                "Lunes a viernes 06:00 a 23:00 / sábado horario reducido",
                ["Máquinas", "Duchas", "Clases grupales", "Piscina", "Spinning"],
                [mensual(38900), anual(411300)],
            ),
            Gimnasio(
                "Sportlife Vitacura",
                "Vitacura",
                39900,
                "Lunes a viernes 06:00 a 23:00 / sábado horario reducido",
                ["Máquinas", "Duchas", "Clases grupales", "Spinning", "Personal trainer"],
                [mensual(39900), anual(411300)],
            ),
            Gimnasio(
                "Sportlife Maipú",
                "Maipú",
                33900,
                "Lunes a viernes 06:00 a 23:00 / sábado horario reducido",
                ["Máquinas", "Duchas", "Clases grupales", "Spinning"],
                [mensual(33900), anual(411300)],
            ),
            Gimnasio(
                "Sportlife Peñalolén",
                "Peñalolén",
                33900,
                "Lunes a viernes 06:00 a 23:00 / sábado horario reducido",
                ["Máquinas", "Duchas", "Clases grupales", "Spinning", "Estacionamiento"],
                [mensual(33900), anual(411300)],
            ),
            Gimnasio(
                "Sportlife Quilicura",
                "Quilicura",
                33900,
                "Lunes a viernes 06:00 a 23:00 / sábado horario reducido",
                ["Máquinas", "Duchas", "Clases grupales", "Spinning"],
                [mensual(33900), anual(411300)],
            ),
            Gimnasio(
                "Sportlife San Miguel",
                "San Miguel",
                33900,
                "Lunes a viernes 06:00 a 23:00 / sábado horario reducido",
                ["Máquinas", "Duchas", "Clases grupales", "Spinning"],
                [mensual(33900), anual(411300)],
            ),
            Gimnasio(
                "Sportlife Chicureo",
                "Colina",
                39900,
                "Lunes a viernes 06:00 a 23:00 / sábado horario reducido",
                ["Máquinas", "Duchas", "Clases grupales", "Piscina", "Estacionamiento"],
                [mensual(39900), anual(411300)],
            ),

            # W Fitness - Santiago Oriente y alrededores
            Gimnasio(
                "W Fitness La Dehesa",
                "Lo Barnechea",
                39900,
                "Lunes a viernes 06:00 a 23:00 / sábado horario reducido",
                ["Máquinas", "Duchas", "Clases grupales", "Personal trainer", "Nutrición"],
                [mensual(39900), anual(358800)],
            ),
            Gimnasio(
                "W Fitness El Alba",
                "Las Condes",
                39900,
                "Lunes a viernes 06:00 a 23:00 / sábado horario reducido",
                ["Máquinas", "Duchas", "Clases grupales", "Personal trainer", "Nutrición"],
                [mensual(39900), anual(358800)],
            ),
            Gimnasio(
                "W Fitness Las Vizcachas",
                "Puente Alto",
                39900,
                "Lunes a viernes 06:00 a 23:00 / sábado horario reducido",
                ["Máquinas", "Duchas", "Clases grupales", "Personal trainer"],
                [mensual(39900), anual(358800)],
            ),
            Gimnasio(
                "W Fitness Padre Hurtado",
                "Padre Hurtado",
                39900,
                "Lunes a viernes 06:00 a 23:00 / sábado horario reducido",
                ["Máquinas", "Duchas", "Clases grupales", "Personal trainer"],
                [mensual(39900), anual(358800)],
            ),

            # Gimnasios boutique o locales
            Gimnasio(
                "Mega Fitness Nueva Providencia",
                "Providencia",
                39990,
                "Lunes a viernes 06:00 a 22:45 / sábado 09:00 a 18:00 / domingo 11:00 a 16:00",
                ["Máquinas", "Duchas", "Clases grupales", "Personal trainer", "Kinesiólogo", "Evaluación corporal"],
                [mensual(39990), trimestral(109990), anual(399900)],
            ),
            Gimnasio(
                "Mega Fitness Manuel Montt",
                "Providencia",
                39990,
                "Lunes a viernes 06:00 a 22:45 / sábado 09:00 a 18:00 / domingo 11:00 a 16:00",
                ["Máquinas", "Duchas", "Clases grupales", "Personal trainer", "Kinesiólogo", "Evaluación corporal"],
                [mensual(39990), trimestral(109990), anual(399900)],
            ),
            Gimnasio(
                "Youtopia Vitacura",
                "Vitacura",
                89900,
                "Lunes a domingo, horario extendido",
                ["Máquinas", "Duchas", "Clases grupales", "Piscina", "Spa", "Personal trainer", "Estacionamiento"],
                [mensual(89900), anual(899000)],
            ),
            Gimnasio(
                "Bio Ritmo El Golf",
                "Las Condes",
                69900,
                "Lunes a viernes 06:30 a 22:00 / fin de semana horario reducido",
                ["Máquinas", "Duchas", "Clases grupales", "Personal trainer", "Pilates", "Spinning", "Nutrición"],
                [mensual(69900), semestral(379900), anual(699900)],
            ),
            Gimnasio(
                "UFC Gym Plaza Oeste",
                "Cerrillos",
                33000,
                "Lunes a viernes horario extendido / fin de semana horario reducido",
                ["Máquinas", "Duchas", "Clases grupales", "Boxeo", "CrossFit", "Funcional", "Nutrición"],
                [mensual(33000), anual(396000)],
            ),
            Gimnasio(
                "Boxeo Desde Cero Santiago Centro",
                "Santiago Centro",
                30000,
                "Lunes a sábado, horario por clases",
                ["Boxeo", "Funcional", "Clases grupales", "Personal trainer"],
                [mensual(30000), trimestral(83000)],
            ),
            Gimnasio(
                "Vive Fitness Estación Central",
                "Estación Central",
                21000,
                "Lunes a sábado, horario extendido",
                ["Máquinas", "Duchas", "Funcional", "Clases grupales"],
                [mensual(21000), trimestral(57000), anual(199990)],
            ),
        ]

    def obtener_comunas(self):
        """Retorna las comunas disponibles sin repetir."""
        return sorted(set(g.comuna for g in self.gimnasios))

    def recomendar_gimnasios(self, usuario):
        """
        Recomienda gimnasios ordenados por puntaje.
        Retorna una lista de tuplas: (gimnasio, puntaje, motivo).
        """
        resultados = []

        for gimnasio in self.gimnasios:
            puntaje = gimnasio.calcular_puntaje(usuario)
            motivo = gimnasio.obtener_motivo_recomendacion(usuario)
            resultados.append((gimnasio, puntaje, motivo))

        resultados.sort(key=lambda item: (item[1], -item[0].precio_mensual), reverse=True)
        return resultados

    def crear_solicitud(self, usuario, gimnasio):
        """Crea una solicitud de reubicación para un usuario."""
        solicitud = SolicitudReubicacion(usuario, gimnasio)
        self._solicitudes.append(solicitud)
        return solicitud
