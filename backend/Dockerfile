# Usa una imagen base oficial de Python 3.12
FROM python:3.12

# Establece el directorio de trabajo
WORKDIR /app

# Copia y instala las dependencias
COPY requirements-linux.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos de la aplicación
COPY . .

# Excluye las carpetas grandes y venv en el contenedor
RUN rm -rf features images venv

# Expone el puerto para la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación con uvicorn
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]

