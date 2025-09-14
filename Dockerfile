# Imagen base con Python
FROM python:3.11-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar dependencias e instalarlas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Exponer el puerto que usará Flask
EXPOSE 5000

# Comando para iniciar la app
CMD ["python", "app.py"]
