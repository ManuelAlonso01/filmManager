# Proyecto Películas

[FilmManager.com](https://wramovies.up.railway.app/)

Este es un sistema de gestión de catálogos cinematográficos desarrollado con **Django**. La aplicación permite realizar operaciones CRUD (Crear, Leer, Actualizar) sobre una base de datos de películas y cuenta con una funcionalidad para generar resúmenes automáticos.

## 🚀 Características

* **Listado de Películas**: Visualización de todas las películas registradas en la base de datos.
* **Gestión de Contenido**: Formulario para subir nuevas películas incluyendo título, imagen de poster, duración, descripción y calificación.
* **Edición**: Capacidad para modificar los datos de películas ya existentes mediante su identificador único.
* **Resúmenes**: Integración de una herramienta para generar resúmenes de la información disponible.

## 🛠️ Stack Tecnológico

* **Framework**: Django 6.0.
* **Base de Datos**: Soporte para SQLite (local) y PostgreSQL (configurado para producción vía `dj-database-url`).
* **Servidor de Aplicaciones**: Gunicorn.
* **Manejo de Estáticos**: WhiteNoise.

## 📋 Requisitos Previos

Asegúrate de tener instalado Python en tu sistema. Las dependencias principales se encuentran en el archivo `requirements.txt`.

## 🔧 Instalación y Configuración

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/ManuelAlonso01/proyecto-peliculas.git
   cd proyecto-peliculas

2. **Instalar dependencias:**:
   ```bash
   pip install -r requirements.txt

3. **Configurar la base de datos**:
   Realiza las migraciones para preparar el esquema de la base de datos.
   ```bash
   python manage.py migrate

4. **Recolección de archivos estáticos**:
   ```bash
   python manage.py collectstatic

5. **Ejecutar el servidor de desarrollo**:
   ```bash
   python manage.py runserver

## 🗂️ Estructura del Modelo de Datos
El modelo principal ```Movies``` cuenta con los siguientes campos:

```title```: Título de la película (máx. 100 caracteres).

```poster```: URL o ruta de la imagen de portada.

```duration_minutes```: Duración expresada en minutos (Integer).

```descripcion```: Breve reseña de la obra.

```calificacion```: Nota numérica asignada.

## 🌐 Endpoints Principales
```/```: Página principal con el listado de películas.

```/subir/```: Formulario de creación.

```/editar/<id_pelicula>```: Interfaz de edición por ID.

```/resumen/```: Vista de generación de resúmenes.



