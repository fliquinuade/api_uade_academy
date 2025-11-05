#PASO 1
FROM python:3.12-slim

#Paso 2: Configuración extras de variables de entorno previas para la creacion del contenedor
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONNUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1  \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

#PASO 3: Instalar depedencias del sistema necesarioa para python - mysql - imagenes
#apt es el gestor de paquetes de slim Linux
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \ 
    libmariadb-dev \
    pkg-config \
    libjpeg-dev \
    zlib1g-dev \
    curl 


#PASO 4
COPY requirements.txt .

#PASO 5
RUN pip install --no-cache-dir -r requirements.txt

#PASO 6
COPY src/ .

#PASO 7: copiamos script entrypoint.sh a un directorio del contenedor
COPY deployments/entrypoint.sh /usr/local/bin/entrypoint.sh
#Se otorga permiso de ejeción al script
RUN chmod +x /usr/local/bin/entrypoint.sh

#PASO 8
RUN mkdir -p /app/media /app/logs /app/staticfiles

# #PASO 9
RUN useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /app

#PASO 10: Habilitamos el usuario creado
USER appuser

#PASO 11: Exponemos el puerto
EXPOSE 8000

#PASO 12: Indico cual es el script de inicio para el contenedor
ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]

#PASO 13: Envio parametro 'production' para ejecución entrypoint.sh
CMD ["production"]


