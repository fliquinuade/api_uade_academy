#!/bin/sh

#salga si hay error
set -e

echo "Inciando aplicacion AUDE-ACADEMY-API"


echo "Ejecutando migraciones de base de datos..."
python manage.py makemigrations
python manage.py migrate --noinput

echo "Recopilando archivos estaticos..."
python manage.py collectstatic --noinput --clear

echo "Aplicacion preparada exitosamente"

#Determino que comando ejecutar segun el argumento enviado
MODE=${1} #En la variable mode, cargue el primer argumento que recibe
if [ "$MODE" = "production" ]; then
    echo "Iniciando en modo PRODUCCION con GUNICORN..."
    exec gunicorn config.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 3 \
        --timeout 120 
else
    echo "Iniciando en modo DESARROLLO con runserver..."
    exec python manage.py runserver 0.0.0.0:8000
fi
