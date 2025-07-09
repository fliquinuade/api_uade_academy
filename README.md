# 🏫 API UADE Academy

API-REST construida con **Django 5.2** y **Python 3.13** para la gestión académica de la institución UADE. Este proyecto sigue una arquitectura modular y está preparado para ambientes de desarrollo y producción.

---

## 🚀 Características principales

- API-RESTful con Django
- Separación clara de configuración (settings, urls, WSGI, ASGI)
- Uso de variables de entorno `.env`
- Proyecto estructurado para escalar fácilmente
- Preparado para despliegue en servicios como Render, Heroku, etc.

---

## 🧱 Estructura del proyecto

```bash
API_UADE_ACADEMY/
│
├── src/
│   ├── api/             # Módulo principal de la API (views, serializers, models, etc.)
│   ├── config/          # Configuración del proyecto Django
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── utils/           # Funciones y clases utilitarias
│   └── manage.py        # Comando principal de Django
│
├── .env                 # Variables de entorno (NO subir al repo)
├── .env.example         # Ejemplo base del .env
├── requirements.txt     # Dependencias del proyecto
├── README.md            # Este archivo 🙂
└── .gitignore           # Archivos y carpetas ignoradas por git
````

---

## 🔧 Requisitos

* Python **3.13**
* pip
* Entorno virtual (opcional pero recomendado)

---

## ⚙️ Instalación y configuración

```bash
# Clonar el repositorio
git clone https://github.com/fliquinuade/api_uade_academy

# Crear entorno virtual
python3.13 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Copiar y configurar archivo de entorno
cd API_UADE_ACADEMY/src
cp ../.env.example ../.env
# Editar ../.env con tus variables personalizadas

# Migraciones
python manage.py migrate

# Ejecutar servidor
python manage.py runserver
```

---

## 🧪 Comandos útiles

```bash
# Ejecutar tests
python manage.py test

# Crear superusuario
python manage.py createsuperuser
```

---

## 🛠️ Variables de entorno

Edita el archivo `.env` con tus propias credenciales. Ejemplo:

```env
SECRET_KEY=
#CREDENCIALES BASE DE DATOS
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

---

## 📚 Dependencias principales

* Django 5.2
* djangorestframework
* python-dotenv

*(ver `requirements.txt` para la lista completa)*

---

## 🤝 Contribuciones

¡Contribuciones son bienvenidas! Puedes hacer un fork del proyecto, crear una nueva rama y enviar un Pull Request.
