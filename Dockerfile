# Imagen base oficial de Python 3.12
FROM python:3.12-slim

# Directorio de trabajo
WORKDIR /app

#Dependencias de sistema
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && apt-get clean

# Archivos de requerimientos al contenedor
COPY requirements.txt /app/

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido del proyecto al directorio de trabajo
COPY . /app/

# Expone el puerto que usará la aplicación
EXPOSE 8000

# Define el comando por defecto para ejecutar la aplicación
CMD ["python", "manage.py", "runserver", "pytest", "0.0.0.0:8000"]