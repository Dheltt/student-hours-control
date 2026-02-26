# Usamos Python slim para que sea más ligero
FROM python:3.11-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiamos requirements y los instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código fuente y el .env
COPY ./app /app
COPY ./.env /app/.env

# Comando por defecto al iniciar el contenedor
CMD ["python", "-m", "app.main"]