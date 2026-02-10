# FilmManager

## 🌐 Demo en producción: [FilmManager.com](https://filmmanager.up.railway.app/)

**FilmManager** es una aplicación web desarrollada en **Django** para gestionar un catálogo personal de películas vistas durante el año y obtener estadísticas y resúmenes a partir de esos datos.

El objetivo del proyecto es practicar desarrollo backend realista, manejo de modelos, vistas, despliegue en producción y persistencia de datos.

Permite llevar un registro centralizado de las películas que vas viendo, con información relevante como duración, calificación y descripción, y luego generar un resumen general del contenido cargado.

Ideal para cinéfilos obsesivos, personas que quieren estadísticas simples de consumo, o como base para escalar a algo más grande.

## 🖼️ Capturas
- ### Pagina Principal
   <p align="center">
      <img src="capturas/captura1.png" width="600">
   </p>


- ### Resumen
   <p align="center">
      <img src="capturas/captura2.png" width="600">
   </p>


## 🚀 Características

* **Listado de Películas**: Visualización de todas las películas registradas en la base de datos.
* **Gestión de Contenido**: Formulario para subir nuevas películas incluyendo título, imagen de poster, duración, descripción y calificación.
* **Edición**: Capacidad para modificar los datos de películas ya existentes mediante su identificador único.
* **Resúmenes**: Integración de una herramienta para generar resúmenes de la información disponible.
* **Usuarios**: Registro e inicio de sesión para que cada usuario gestione su propio catálogo de películas.

## 🛠️ Stack Tecnológico

* **Framework**: Django.
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



