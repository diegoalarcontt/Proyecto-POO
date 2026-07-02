# Sistema de Reubicación de Usuarios Afectados por el Cierre de Gimnasios

## Descripción

Este proyecto consiste en una aplicación de escritorio que permite registrar las preferencias de un usuario afectado por el cierre de un gimnasio y recomendar gimnasios alternativos según comuna, presupuesto, tipo de membresía y servicios solicitados.

El sistema fue desarrollado aplicando Programación Orientada a Objetos mediante clases como `Usuario`, `Gimnasio`, `Membresia`, `SolicitudReubicacion` y `SistemaReubicacion`.

## Problema que resuelve

Cuando un gimnasio cierra repentinamente, muchos usuarios quedan sin acceso al servicio que habían contratado y sin una alternativa clara para continuar entrenando. Esta aplicación ayuda a organizar la búsqueda de nuevos gimnasios y entrega recomendaciones de acuerdo con las necesidades del usuario.

## Funcionalidades principales

- Registrar datos del usuario afectado.
- Ingresar presupuesto máximo mensual.
- Seleccionar comuna y tipo de membresía preferida.
- Seleccionar servicios preferidos, como máquinas, duchas, clases grupales, piscina, boxeo, pilates, spinning o entrenamiento funcional.
- Mostrar gimnasios disponibles.
- Recomendar gimnasios según puntaje de compatibilidad.
- Crear una solicitud de reubicación hacia un gimnasio seleccionado.

## Casos de uso considerados

### 1. Buscar recomendación de gimnasio

El usuario ingresa sus datos y preferencias. Luego el sistema compara esa información con los gimnasios disponibles y entrega una lista ordenada por puntaje de recomendación.

### 2. Mostrar gimnasios disponibles

El usuario puede revisar todos los gimnasios registrados en el sistema, junto con su comuna, precio mensual y membresías disponibles.

### 3. Crear solicitud de reubicación

Después de recibir recomendaciones, el usuario selecciona un gimnasio y el sistema crea una solicitud de reubicación con estado pendiente.

## Conceptos de POO utilizados

- **Encapsulación:** los atributos principales de las clases se manejan como atributos privados y se accede a ellos mediante propiedades.
- **Herencia:** `Usuario` y `Administrador` heredan de la clase base `Persona`.
- **Polimorfismo:** el método `obtener_descripcion()` se comporta distinto según si el objeto es una `Persona`, un `Usuario` o un `Administrador`.
- **Composición:** una clase `Gimnasio` contiene varias `Membresia`.
- **Asociación:** una `SolicitudReubicacion` relaciona un `Usuario` con un `Gimnasio`.

## Requisitos

- Python 3 instalado.
- Tkinter, que normalmente viene incluido con Python.

No se utilizan librerías externas.

## Cómo ejecutar

Desde la carpeta principal del proyecto, ejecutar:

```bash
python main.py
```

En algunos computadores puede ser necesario usar:

```bash
python3 main.py
```

## Estructura del proyecto

```text
Sistema_Reubicacion_Gimnasios/
│
├── main.py
├── Makefile
├── README.md
├── .gitignore
│
├── src/
│   ├── models.py
│   ├── sistema.py
│   └── gui.py
│
└── docs/
    ├── informe.html
    ├── DIAGRAMA_UML.md
    ├── DIAGRAMA_SECUENCIA.md
    └── img/
```

## Datos usados

La versión actual incluye 26 gimnasios o sedes de Santiago y alrededores. Los nombres, comunas y servicios se basan en información pública revisada en sitios oficiales o fichas públicas.

Los precios y horarios se usan como valores referenciales para la demostración del proyecto, ya que pueden cambiar según promociones, matrícula, sede, permanencia y contrato. Antes de usar la información fuera del proyecto, se deben confirmar directamente con cada gimnasio.

## Autores

- Diego Alarcón Tapia / 202430509-3
- Joaquin Cordero / 202430505-0
- Ivan Carlsson / 202430568-9

## Repositorio

https://github.com/diegoalarcontt/Proyecto-POO.git
