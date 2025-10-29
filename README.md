# EduImpact RAG

Aplicación web basada en Django con funcionalidad de chatbot utilizando RAG (Retrieval-Augmented Generation).

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

- **Python 3.8+** (recomendado Python 3.9 o superior)
- **pip** (gestor de paquetes de Python)
- **Git** (para clonar el repositorio)

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/CSV-Alex/eduimpact_rag.git
cd eduimpact_rag
```

### 2. Crear un entorno virtual

Es altamente recomendable usar un entorno virtual para mantener las dependencias del proyecto aisladas.

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**En Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar las dependencias

```bash
cd eduimpact_rag
pip install -r requirements.txt
```

**Dependencias principales:**
- Django >= 3.2.14
- requests

### 4. Configurar la base de datos

Ejecuta las migraciones para configurar la base de datos:

```bash
python manage.py migrate
```

### 5. Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

### 7. Acceder a la aplicación

Abre tu navegador web y ve a:

- **Aplicación principal:** http://127.0.0.1:8000/

## 📁 Estructura del Proyecto

```
eduimpact_rag/
├── eduimpact_rag/          # Directorio principal del proyecto
│   ├── chatbot/            # Aplicación del chatbot
│   ├── eduimpact_rag/      # Configuración del proyecto Django
│   │   ├── settings.py     # Configuración principal
│   │   └── urls.py         # Rutas URL
│   ├── manage.py           # Script de gestión de Django
│   ├── db.sqlite3          # Base de datos SQLite
│   └── requirements.txt    # Dependencias Python
```

## 🛠️ Tecnologías Utilizadas

- **Backend:** Django 3.2.14+
- **Base de datos:** SQLite (por defecto)
- **HTTP Client:** requests
- **Frontend:** HTML, CSS, JavaScript

## ⚙️ Configuración

El proyecto utiliza las siguientes configuraciones por defecto:

- **Base de datos:** SQLite3
- **DEBUG:** True (solo para desarrollo)
- **SECRET_KEY:** Incluida en settings.py (cambiar en producción)

## 📝 Comandos Útiles

```bash
# Ejecutar el servidor
python manage.py runserver

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Recopilar archivos estáticos
python manage.py collectstatic

# Ejecutar tests
python manage.py test
```

## 🐛 Solución de Problemas

### Error al instalar dependencias

Si encuentras errores durante la instalación:

```bash
# Actualizar pip
pip install --upgrade pip

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### Error de base de datos

Si hay problemas con la base de datos:

```bash
# Eliminar la base de datos (perderás los datos)
rm db.sqlite3

# Volver a ejecutar las migraciones
python manage.py migrate
```
