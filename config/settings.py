from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Básico ---
SECRET_KEY = "cámbiame-por-un-valor-seguro"
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# --- Apps ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "nuam",  #  tu app
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        #  Asegúrate de tener la carpeta /templates al lado de manage.py
        "DIRS": [BASE_DIR /"nuam"/"templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# --- Base de datos (sqlite dev) ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --- Internacionalización ---
LANGUAGE_CODE = "es-cl"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

# --- Archivos estáticos ---
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]        # /static para desarrollo
STATIC_ROOT = BASE_DIR / "staticfiles"          # para collectstatic en prod (opcional)

# --- Media (si subes archivos) ---
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
