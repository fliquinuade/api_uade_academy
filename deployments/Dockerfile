#PASO 1
FROM python:3.12-alpine

#PASO 2
WORKDIR /app

#PASO 3: Instalar depedencias del sistema necesarioa para python - mysql - imagenes
#apk es el gestor de paquetes de Alpine Linux
RUN apk add --no-cache \
    build-base \ 
    mariadb-dev \
    jpeg-dev \
    zlib-dev \
    openjpeg-dev \
    curl 

#PASO 4
COPY requirements.txt .

#PASO 5
RUN pip install --no-cache-dir -r requirements.txt

#PASO 6
COPY src/ .

#PASO 7
# RUN mkdir -p /app/media /app/logs /app/staticsfiles

# #PASO 8
# RUN adduser -D -s /bin/sh uadeuser

# #PASO 9 - Habilitarle permisos al usuario uadeuser
# RUN chown -R uadeuser:uadeuser /app
# RUN chmod -R 755 /app

#PASO 10
#USER uadeuser

#PASO 11
EXPOSE 8000

#PASO 12
CMD ["python","src/manage.py","runserver","0.0.0.0:8000"]


